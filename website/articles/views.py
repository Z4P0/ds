from flask import render_template, redirect, url_for, flash
from flask.ext.login import current_user, login_required
from ..models import Permission, Article, Category, Tag
from .. import db
from . import articles
from .forms import ArticleForm

@articles.route('/')
def articles_index():
    # all the categories - what we had before
    # list of all the posts
    categories = Category.query.all()
    posts = Article.query.all()
    return render_template('articles/index.html',
        title='Articles',
        categories=categories,
        posts=posts)


@articles.route('/<slug>')
def read_article(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()
    # next_article =
    return render_template('articles/view.html', article=article)


@articles.route('/category/<slug>')
def view_category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    posts = category.posts.all()
    total_posts = category.posts.count()
    # latest_2
    return render_template('articles/category-single.html',
        title=category.name,
        posts=posts,
        total_posts=total_posts,
        category=category)



@articles.route('/new', methods=['GET', 'POST'])
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
    return render_template('articles/new.html', form=form)
