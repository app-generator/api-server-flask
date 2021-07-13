# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import re
from datetime import datetime, timedelta, timezone

from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, get_jwt, create_access_token, get_jwt_identity
from flask_restx import Api, Resource, marshal, fields, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

@api.route('/users/signup')
class Register(Resource):
    """
       Creates a new user by taking 'signup_model' input
    """

    @api.expect(signup_model, validate=True)
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


@api.route('/users/login')
class Login(Resource):
    """
       Login user by taking 'login_model' input and return JWT token
    """

    @api.expect(login_model, validate=True)
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


@api.route('/users/edit')
class EditUser(Resource):
    """
       Edits User's name or password or both using 'user_edit_model' input
    """

    @api.expect(user_edit_model)
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


@api.route('/users/logout')
class LogoutUser(Resource):
    """
       Edits User's name or password or both using 'user_edit_model' input
    """

    @api.expect(user_edit_model)
    @jwt_required()
    def delete(self):

        user_email = get_jwt_identity()
        current_user = Users.get_by_email(user_email)
        
        if not current_user:
            abort(400, "Sorry. Wrong auth token")

        jwt_block = JWTTokenBlocklist(jti=get_jwt()["jti"], created_at=datetime.now(timezone.utc))
        jwt_block.save()

        return {"message": "JWT Token revoked successfully!"}, 200


