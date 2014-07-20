from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, FileField, SubmitField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length, Optional, URL, Regexp
from  wtforms import ValidationError
from ..models import User



# login form
class LoginForm(Form):
    """ logging in """
    email = StringField(validators=[Email(), Required(), Length(1, 64)])
    password = PasswordField(validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')



# register form
class RegisterForm(Form):
    """ Register a new account """
    email = StringField(validators=[Required(), Email(), Length(1, 64)])
    username = StringField(validators=[Required(), Length(3,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
        'Usernames must have only letters, numbers, dots, or underscores')])
    password = PasswordField(validators=[Required()])
    password2 = PasswordField('Confirm', validators=[Required(), EqualTo('password', message='Passwords must match.')])
    agree_to_terms = BooleanField(validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')

# change email
class ChangeEmailForm(Form):
    """ Changing your email """
    email = StringField(validators=[Required(), Email()])
    submit = SubmitField('Send email')



# change password
class ChangePasswordForm(Form):
    """ Change password """
    current_password = PasswordField('Current Password', validators=[Required()])
    new_password = PasswordField('New Password', validators=[Required(), Length(6, 28)])
    new_password2 = PasswordField('Confirm', validators=[Required(), EqualTo('new_password')])
    submit = SubmitField('Change')



# reset password
class ResetPasswordForm(Form):
    """ Reset password """
    email = StringField(validators=[Required(), Email()])
    submit = SubmitField('Send email')
