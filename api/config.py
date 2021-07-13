# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   decouple import config
from   datetime import datetime, timedelta, timezone

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    CSRF_ENABLED = True
	
    # Set up the SECRET_KEY(s)
    SECRET_KEY     = config('SECRET_KEY', default='S#perS3crEt_007')
    JWT_SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_API')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
