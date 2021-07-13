# -*- encoding: utf-8 -*-

"""
Copyright (c) 2019 - present AppSeed.us
"""

import pytest
import json

from api import app


"""
   Sample test data
"""

DUMMY_NAME = "apple"
DUMMY_EMAIL = "apple@apple.com"
DUMMY_PASS = "newpassword"


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_user_signup(client):
    """
       Tests /users/signup API
    """
    response = client.post(
        "/users/signup",
        data=json.dumps(
            {
                "name": DUMMY_NAME,
                "email": DUMMY_EMAIL,
                "password": DUMMY_PASS
            }
        ),
        content_type="application/json")

    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert "User with (%s, %s) created successfully!" % (DUMMY_NAME, DUMMY_EMAIL) in data["message"]


def test_user_signup_invalid_data(client):
    """
       Tests /users/signup API: invalid data like email field empty
    """
    response = client.post(
        "/users/signup",
        data=json.dumps(
            {
                "name": DUMMY_NAME,
                "email": "",
                "password": DUMMY_PASS
            }
        ),
        content_type="application/json")

    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_user_login_correct(client):
    """
       Tests /users/signup API: Correct credentials
    """
    response = client.post(
        "/users/login",
        data=json.dumps(
            {
                "email": DUMMY_EMAIL,
                "password": DUMMY_PASS
            }
        ),
        content_type="application/json")

    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data["access_token"] != ""


def test_user_login_error(client):
    """
       Tests /users/signup API: Wrong credentials
    """
    response = client.post(
        "/users/login",
        data=json.dumps(
            {
                "email": DUMMY_EMAIL,
                "password": DUMMY_EMAIL
            }
        ),
        content_type="application/json")

    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Sorry. Wrong credentials." in data["message"]
