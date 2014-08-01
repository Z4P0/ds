from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, FileField, SubmitField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length, Optional, URL
from flask.ext.pagedown.fields import PageDownField


class ArticleForm(Form):
    """ For posting articles """
    title = StringField('Title', validators=[Required()])
    slug = StringField('Slug', validators=[Required()])
    body = PageDownField('Drafting Page', validators=[Required()])
    preview = PageDownField('Preview (paragraph to get people interested)', validators=[Required()])
    # body = TextAreaField('Drafting Page', validators=[Required()])
    # preview = TextAreaField('Preview (paragraph to get people interested)', validators=[Required()])
    submit = SubmitField('Submit')


# comment form
class CommentForm(Form):
    """ Make a comment on an article """
    body = TextAreaField(validators=[Required()])
    follow_replies = BooleanField('Follow Replies', validators=[Optional()])
    submit = SubmitField('Comment')



# bookmark form
class BookmarkForm(Form):
    """ Bookmark an article """
    bookmark = SubmitField('Bookmark')



# subscriptions
class SubscribeForm(Form):
    """ Subscribe to a category, or series """
    subscribe = SubmitField('Subscribe')
