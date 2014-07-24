from flask import render_template, redirect, url_for, flash
from flask.ext.login import current_user, login_required
from ..models import Permission, Article
from .. import db
from . import articles
from .forms import ArticleForm

@articles.route('/')
def articles_index():
  return 'all articles'

@articles.route('/<slug>')
def read_article(slug):
    return 'article: %s' % slug

@articles.route('/drafts', methods=['GET', 'POST'])
@login_required
def article_form():
    form = ArticleForm()
    flash('see the form?')
    # if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
    if form.validate_on_submit():
        flash('we got this far')
        article = Article(content=form.body.data, author=current_user._get_current_object())
        db.session.add(article)
        return redirect(url_for('main.index'))
    return render_template('ds/drafts.html', form=form)
