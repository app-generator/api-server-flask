# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime, timezone

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

signup_model = rest_api.model('SignUpModel', {"name": fields.String(required=True, min_length=2, max_length=32),
                                              "email": fields.String(required=True, min_length=4, max_length=64),
                                              "password": fields.String(required=True, min_length=6, max_length=16)
                                              })

login_model = rest_api.model('LoginModel', {"email": fields.String(required=True, min_length=4, max_length=64),
                                            "password": fields.String(required=True, min_length=6, max_length=16)
                                            })

user_edit_model = rest_api.model('UserEditModel', {"name": fields.String(required=True, min_length=2, max_length=32),
                                                   "password": fields.String(required=True, min_length=6, max_length=16)
                                                   })

"""
    Flask-Restx routes
"""


@rest_api.route('/api/users/signup')
class Register(Resource):
    """
       Creates a new user by taking 'signup_model' input
    """

    @rest_api.expect(signup_model, validate=True)
    def post(self):

        req_data = request.get_json()

        _name = req_data.get("name")
        _email = req_data.get("email")
        _password = req_data.get("password")

        user_exists = Users.get_by_email(_email)
        if user_exists:
            abort(400, "Sorry. This email already exists.")

        new_user = Users(name=_name, email=_email)

        new_user.set_password(_password)
        new_user.save()

        return {'message': 'User with (%s, %s) created successfully!' % (_name, _email)}, 201


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
            abort(400, "Sorry. This email does not exist.")

        if not user_exists.check_password(_password):
            abort(400, "Sorry. Wrong credentials.")

        # create access token uwing JWT
        access_token = create_access_token(identity=_email)

        return {"access_token": access_token}, 200


@rest_api.route('/api/users/edit')
class EditUser(Resource):
    """
       Edits User's name or password or both using 'user_edit_model' input
    """

    @rest_api.expect(user_edit_model)
    @jwt_required()
    def post(self):

        user_email = get_jwt_identity()
        current_user = Users.get_by_email(user_email)

        if not current_user:
            abort(400, "Sorry. Wrong auth token. This user does not exist.")

        req_data = request.get_json()

        _new_name = req_data.get("name")
        _new_password = req_data.get("password")

        if _new_name:
            current_user.update_name(_new_name)

        if _new_password:
            current_user.set_password(_new_password)

        current_user.save()

        return {"message": 'User details updated successfully!'}, 200


@rest_api.route('/api/users/logout')
class LogoutUser(Resource):
    """
       Edits User's name or password or both using 'user_edit_model' input
    """

    @rest_api.expect(user_edit_model)
    @jwt_required()
    def delete(self):

        user_email = get_jwt_identity()
        current_user = Users.get_by_email(user_email)

        if not current_user:
            abort(400, "Sorry. Wrong auth token")

        jwt_block = JWTTokenBlocklist(jti=get_jwt()["jti"], created_at=datetime.now(timezone.utc))
        jwt_block.save()

        return {"message": "JWT Token revoked successfully!"}, 200
