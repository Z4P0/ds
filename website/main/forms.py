from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, SelectField, FileField, SubmitField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length, Optional, URL, Regexp


class UploadForm(Form):
    """ test form for uploading things to the server """
    media = FileField('Add file to upload')
    submit = SubmitField('Upload')


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
    location = StringField(validators=[Optional(), Length(0, 64)])
    bio = TextAreaField(validators=[Optional()])
    picture = FileField('Profile Picture', validators=[Optional()])
    # email
    # password
    save = SubmitField('Save')

class ProfileFormAdmin(Form):
    """ Administers have more options """
    email = StringField('Email', validators=[Required(), Length(1,64),Email()])
    username = StringField('Username', validators=[Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
        'Usernames must have only letters, numbers, dots, or underscores')])
    confirmed = BooleanField('confirmed')
    role = SelectField('Role', coerce=int)
    fullname = StringField('Fullname', validators=[Length(0,64)])
    bio = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(ProfileFormAdmin, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user


    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email alread in use')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('That usernmae is already in use')









