from flask import *
from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin
from flask_user import roles_required
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField
from wtforms import validators, ValidationError
from wtforms import Form, BooleanField, StringField, PasswordField, validators


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    location = db.Column(db.String(255))
    gender = db.Column(db.Integer)
    age = db.Column(db.Integer)
    preferred_min_age = db.Column(db.Integer)
    preferred_max_age = db.Column(db.Integer)
    preferred_gender = db.Column(db.String(255))

    def __init__(self, name, email, password, location, gender, age, preferred_min_age, preferred_max_age,
                 preferred_gender):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.location = location
        self.gender = gender
        self.age = age
        self.preferred_min_age = preferred_min_age
        self.preferred_max_age = preferred_max_age
        self.preferred_gender = preferred_gender

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'location': self.location,
            'gender': self.gender,
            'age': self.age,
            'preferred_min_age': self.preferred_min_age,
            'preferred_max_age': self.preferred_max_age,
            'preferred_gender': self.preferred_gender
        }

    def __repr__(self):
        return "User<%d> %s" % (self.id, self.name)


class RegistrationForm(Form):
    FirstName = StringField('FirstName',
                            [validators.Length(min=4, max=25, message="First Name must be betwen 4 & 25 characters")])
    LastName = StringField("LastName",
                           [validators.Length(min=4, max=8, message="Last Name must be betwen 4 & 35 characters")])
    Username = StringField('Username',
                           [validators.Length(min=4, max=25, message="Username must be betwen 4 & 25 characters")])
    Email = StringField('Email', [validators.Length(min=4, max=35, message="E-mail must be betwen 4 & 35 characters")])
    Password = PasswordField('Password',
                             [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('RePassword')
    submit = SubmitField("SignUp")
    recaptcha = RecaptchaField()

    def __repr__(self):
        return "User { Name: %r }" % (self.Username)


db.create_all()
