from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, FileField, SubmitField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length, Optional, URL



class NameForm(Form):
    """What is your name?"""
    name = StringField(validators=[Required()])
    submit = SubmitField('Submit')



# login form
class LoginForm(Form):
    """ logging in """
    email = StringField(validators=[Email(), Required()])
    password = PasswordField(validators=[Required()])
    remember_me = BooleanField(validators=[Optional()])
    submit = SubmitField('Login')



# register form
class RegisterForm(Form):
    """ Register a new account """
    username = StringField(validators=[Required(), Length(3,30)])
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required(), Length(6, 28)])
    password2 = PasswordField('Confirm', validators=[Required(), EqualTo('password')])
    agree_to_terms = BooleanField(validators=[Required()])
    submit = SubmitField('Register')



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


    
# comment form
class CommentForm(Form):
    """ Make a comment on an article """
    body = TextAreaField(validators=[Required()])
    follow_replies = BooleanField('Follow Replies', validators=[Optional()])
    submit = SubmitField('Comment')



# # upvote/downvote
# class CommentVote(Form):
#       """ Upvote/Downvote """
#       upvote = BooleanField(validators=[Optional()])
#       downvote = BooleanField(validators=[Optional()])



# follow form
class FollowForm(Form):
    """ Follow a user, team, or cup """
    submit = SubmitField('Follow')



# search form
class SearchForm(Form):
    """ Search the site yo """
    text = StringField(validators=[Required()])
    submit = SubmitField('Search')



# contact us form
class ContactForm(Form):
    """ Contact DS """
    message = TextAreaField(validators=[Required()])
    name = StringField(validators=[Required()])
    email = StringField(validators=[Required(), Email()])
    send = SubmitField('Send')


# profile form
class ProfileForm(Form):
    """ Various things for your profile """
    fullname = StringField(validators=[Optional()])
    twitter = StringField(validators=[Optional()])
    instagram = StringField(validators=[Optional()])
    bio = TextAreaField(validators=[Optional()])
    picture = FileField('Profile Picture', validators=[Optional()])
    # email
    # password
    save = SubmitField('Save')



# bookmark form
class BookmarkForm(Form):
    """ Bookmark an article """
    bookmark = SubmitField('Bookmark')



# subscriptions
class SubscribeForm(Form):
    """ Subscribe to a category, or series """
    subscribe = SubmitField('Subscribe')
