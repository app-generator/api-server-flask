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


app = Flask(__name__)

app.config.from_object('api.config.Config')

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)
