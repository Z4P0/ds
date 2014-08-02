from flask import render_template, redirect, url_for, flash
from flask.ext.login import current_user, login_required
from ..models import Permission, Article, Category, Tag, Topic
from .. import db
from . import articles
from .forms import ArticleForm



@articles.route('/')
def articles_index():
    # all the categories - what we had before
    # list of all the posts
    topics = Topic.query.order_by(Topic.id.desc()).all()
    posts = Article.query.all()
    return render_template('articles/index.html',
        title='Articles',
        topics=topics,
        posts=posts)



@articles.route('/<slug>')
def read_article(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()
    # next_article =
    return render_template('articles/view.html', article=article)

@articles.route('/<slug>/edit', methods=['GET','POST'])
@login_required
def edit_article(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()
    if current_user != article.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.slug = form.slug.data
        article.content = form.body.data
        article.preview = form.preview.data
        db.session.add(article)
        flash('Article has been updated')
        return redirect(url_for('articles.read_article', slug=article.slug))
    form.title.data = article.title
    form.slug.data = article.slug
    form.body.data = article.content
    form.preview.data = article.preview
    return render_template('articles/edit.html', form=form)




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
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by('name')]

    # if current_user.can(Permission.WRITE_ARTICLES):
    #     flash('permission to write sir')
    # flash('turn down for what')
    # flash(form.category.data)
    # if form.category.data is not None:
    #     category = Category.query.filter_by(id=form.category.data).first()
    #     flash(category)
    if form.validate_on_submit():
        flash('we got this far')
        category = Category.query.filter_by(id=form.category.data).first()
        # category = Category.query.filter_by(id=form.category.data).first()
        article = Article(
            title=form.title.data,
            slug=form.slug.data,
            category=category,
            content=form.body.data,
            preview=form.preview.data,
            author=current_user._get_current_object()
            )
        db.session.add(article)
        return redirect(url_for('main.index'))
    return render_template('articles/new.html', form=form)
