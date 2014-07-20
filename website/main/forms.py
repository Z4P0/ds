from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, FileField, SubmitField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length, Optional, URL

#
# SPACES SHOULD NOT BED ALLOWED IN USERNAMES
# UNDERSCORES AND HYPENS ARE OK
#

class NameForm(Form):
    """What is your name?"""
    name = StringField(validators=[Required()])
    submit = SubmitField('Submit')


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
