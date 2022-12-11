# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class BaseConfig():

    SQLALCHEMY_DATABASE_URI        = 'sqlite:///' + os.path.join(BASE_DIR, 'apidata.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY           = os.getenv('SECRET_KEY'    , 'S#perS3crEt_913' )
    JWT_SECRET_KEY       = os.getenv('JWT_SECRET_KEY', 'S#perS3crEt_JWT' )
    GITHUB_CLIENT_ID     = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_SECRET_KEY')
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
