from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Optional, Length, Required
from wtforms.fields.html5 import EmailField

class LoginForm(FlaskForm):
    email = EmailField('Email',
                        render_kw={'style': 'opacity: unset; position: relative;'},
                        validators=[
                            DataRequired(message="Email is required"),
                            Email(message="Please enter your email address.") 
                        ])
    password = PasswordField('Password',
                            validators=[
                                DataRequired(message="Password is required")
                            ])
    tos = BooleanField('Accept Terms of Service of Wealthsimple Trade, Crypto and Wsimple', 
                        default=False,
                        render_kw={'style': 'opacity: unset; position: relative;', "autocomplete": "off"},
                        validators=[
                            DataRequired(message="Password is required")
                        ])