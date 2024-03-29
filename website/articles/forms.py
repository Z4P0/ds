from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, FileField, SubmitField, BooleanField, SelectField, HiddenField
from wtforms.validators import Required, Email, EqualTo, Length, Optional, URL
from flask.ext.pagedown.fields import PageDownField
from ..models import Category

class ArticleForm(Form):
    """ For posting articles """
    title = StringField('Title', validators=[Required()])
    slug = StringField('Slug', validators=[Required()])
    body = PageDownField('Drafting Page', validators=[Required()])
    preview = PageDownField('Preview (paragraph to get people interested)', validators=[Required()])
    # category = SelectField('Category', choices=[('1','Club America')], validators=[Required()])
    category = SelectField('Category', coerce=int, validators=[Required()])
    submit = SubmitField('Submit')


# comment form
class CommentForm(Form):
    """ Make a comment on an article """
    body = TextAreaField(validators=[Required()])
    # email = StringField('Email', validators=[Required(), Email(), Length(1, 64)])
    follow_replies = BooleanField('Follow Replies', validators=[Optional()])
    submit = SubmitField('Comment')

class ReplyForm(Form):
    """ Comments replies """
    body = TextAreaField(validators=[Required()])
    comment_id = HiddenField()
    submit = SubmitField('Reply')



# bookmark form
class BookmarkForm(Form):
    """ Bookmark an article """
    bookmark = SubmitField('Bookmark')



# subscriptions
class SubscribeForm(Form):
    """ Subscribe to a category, or series """
    subscribe = SubmitField('Subscribe')
