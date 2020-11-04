from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Optional, Length, Required, InputRequired
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField('Email',
                       render_kw={
                           'style': 'opacity: unset; position: relative;'},
                       validators=[
                           DataRequired(message="Email is required"),
                           Email(message="Please enter your email address.")
                       ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(message="Password is required")
                             ])
    token = PasswordField('Token',
                             validators=[
                                 Optional()
                             ])
    tos = BooleanField('Accept ToS of Wealthsimple Trade and Wsimple',
                       default=False,
                       render_kw={
                           'style': 'opacity: unset; position: relative;', "autocomplete": "off"},
                       validators=[
                           DataRequired(message="ToS is required")
                       ])
