# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime, timezone

import json

from flask import request
from flask_restx import Api, Resource, fields, abort
from flask_jwt_extended import JWTManager, jwt_required, get_jwt, create_access_token, get_jwt_identity

from .models import db, Users, JWTTokenBlocklist

rest_api = Api(version="1.0", title="Users API")
jwt = JWTManager()

"""
    Helper function for revoking JWT token
"""


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(JWTTokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


"""
    Flask-Restx models for api request and response data
"""

signup_model = rest_api.model('SignUpModel', {"username": fields.String(required=True, min_length=2, max_length=32),
                                              "email": fields.String(required=True, min_length=4, max_length=64),
                                              "password": fields.String(required=True, min_length=4, max_length=16)
                                              })

login_model = rest_api.model('LoginModel', {"email": fields.String(required=True, min_length=4, max_length=64),
                                            "password": fields.String(required=True, min_length=4, max_length=16)
                                            })

user_edit_model = rest_api.model('UserEditModel', {"userID": fields.String(required=True, min_length=1, max_length=32),
                                                   "username": fields.String(required=True, min_length=2, max_length=32),
                                                   "email": fields.String(required=True, min_length=4, max_length=64)
                                                   })

logout_model = rest_api.model('LogoutModel', {"token": fields.String(required=True)})


"""
    Flask-Restx routes
"""


@rest_api.route('/api/users/register')
class Register(Resource):
    """
       Creates a new user by taking 'signup_model' input
    """

    @rest_api.expect(signup_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _username = req_data.get("username")
        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)
        if user_exists:
            return {"success": False,
                    "msg": "Email already exists"}, 400

        new_user = Users(username=_username, email=_email)

        new_user.set_password(_password)
        new_user.save()

        return {"success": True,
                "userID" : new_user.id,
                "msg": "The user was successfully registered"}, 200


@rest_api.route('/api/users/login')
class Login(Resource):
    """
       Login user by taking 'login_model' input and return JWT token
    """

    @rest_api.expect(login_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)

        if not user_exists:
            return {"success": False,
                    "msg": "Sorry. This email does not exist."}, 400

        if not user_exists.check_password(_password):
            return {"success": False,
                    "msg": "Sorry. Wrong credentials."}, 400

        # create access token uwing JWT
        access_token = create_access_token(identity=_email)

        return {"success": True,
                "token": access_token,
                "user" : user_exists.toJSON() }, 200


@rest_api.route('/api/users/edit')
class EditUser(Resource):
    """
       Edits User's username or password or both using 'user_edit_model' input
    """

    @rest_api.expect(user_edit_model)
    @jwt_required()
    def post(self):

        user_email = get_jwt_identity()
        current_user = Users.get_by_email(user_email)

        if not current_user:
            return {"success": False,
                    "msg": "Sorry. Wrong auth token. This user does not exist."}, 400

        req_data = request.get_json()

        _new_username = req_data.get("username")
        _new_email = req_data.get("email")

        if _new_username:
            current_user.update_username(_new_username)

        if _new_email:
            current_user.update_email(_new_email)

        current_user.save()

        return {"success": True}, 200


@rest_api.route('/api/users/logout')
class LogoutUser(Resource):
    """
       Logs out User using 'logout_model' input
    """

    @rest_api.expect(logout_model, validate=True)
    @jwt_required()
    def post(self):

        user_email = get_jwt_identity()
        current_user = Users.get_by_email(user_email)

        if not current_user:
            return {"success": False,
                    "msg": "Sorry. Wrong auth token"}, 400

        jwt_block = JWTTokenBlocklist(jti=get_jwt()["jti"], created_at=datetime.now(timezone.utc))
        jwt_block.save()

        return {"success": True,
                "msg": "JWT Token revoked successfully"}, 200
