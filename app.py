import os
import re
from datetime import datetime, timedelta, timezone

from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, get_jwt, create_access_token, get_jwt_identity
from flask_restx import Api, Resource, marshal, fields, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(BASE_DIR, 'apidata.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'flask-app-secret-key-change-it'
app.config["JWT_SECRET_KEY"] = "jwt-app-secret-key-change-it"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)


# Database Model
class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.Text())
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"User {self.name}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_name(self, new_name):
        self.name = new_name

    def reset_active_session(self, end_session):
        if end_session == True:
            self.active_session = False

    def update_email(self, new_email):
        self.email = new_email

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class JWTTokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f"JTI {self.jti}"

    def save(self):
        db.session.add(self)
        db.session.commit()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(JWTTokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


# Flask-Restx models for api request and response data


signup_model = api.model('SignUpModel', {"name": fields.String(required=True, min_length=2, max_length=32),
                                         "email": fields.String(required=True, min_length=4, max_length=64),
                                         "password": fields.String(required=True, min_length=6, max_length=16)
                                        })

login_model = api.model('LoginModel', {"email": fields.String(required=True, min_length=4, max_length=64),
                                       "password": fields.String(required=True, min_length=6, max_length=16)
                                      })

user_edit_model = api.model('UserEditModel', {"name": fields.String(required=True, min_length=2, max_length=32),
                                              "password": fields.String(required=True, min_length=6, max_length=16)
                                             })


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


@app.shell_context_processor
def make_shell_context():
    return {
        "app": app,
        "db": db,
        "Users": Users,
        "api": api
    }

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
