# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app         import db

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
