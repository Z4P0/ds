from flask import render_template, redirect, url_for, flash
from flask.ext.login import current_user, login_required
from ..models import Permission, Article, Category, Tag, Topic, Comment
from .. import db
from . import articles
from .forms import ArticleForm, CommentForm, ReplyForm



@articles.route('/')
def articles_index():
    # all the categories - what we had before
    # list of all the posts
    topics = Topic.query.order_by(Topic.id.desc()).all()
    posts = Article.query.order_by(Article.post_date.desc()).limit(20)
    return render_template('articles/index.html',
        title='Articles',
        topics=topics,
        posts=posts
        )







@articles.route('/<slug>', methods=['GET','POST'])
def read_article(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()
    # get the latest article
    # we have to account for article.ids that have been deleted
    # we have gaps between some ids
    index = 1
    next_article = Article.query.filter_by(id=article.id + index).first()
    while next_article is None:
        index = index + 1
        next_article = Article.query.filter_by(id=article.id + index).first()
        if next_article is not None:
            break
        else:
            next_article = Article.query.filter_by(id=article.id - index).first()

    # get related articles
    article_category = Category.query.filter_by(id=article.category_id).first()
    related_articles = article_category.posts.order_by(Article.post_date.desc()).limit(3)

    # comment shit
    comment_form = CommentForm(prefix='comment')
    if comment_form.validate_on_submit() and comment_form.submit.data:
        if current_user.can(Permission.COMMENT):
            comment = Comment(
                body=comment_form.body.data,
                author=current_user._get_current_object(),
                article=article
                )
            db.session.add(comment)
            flash('Your comment has been posted!')
            return redirect(url_for('articles.read_article', slug=article.slug))
        # elif comment_form.email.data:
        #     flash('an email was entered')
        else:
            flash('please login to comment')

    comments = article.comments.filter_by(reply_to=None).order_by(Comment.timestamp.desc()).limit(20)

    reply_form = ReplyForm(prefix='reply')
    if reply_form.validate_on_submit() and reply_form.submit.data:
        if current_user.can(Permission.COMMENT):
            og_comment = Comment.query.filter_by(id=reply_form.comment_id.data).first()
            reply = Comment(
                body=reply_form.body.data,
                author=current_user._get_current_object(),
                article=article,
                reply_to=og_comment
                )
            db.session.add(reply)
            flash('hey you posted a reply!')
            return redirect(url_for('articles.read_article', slug=article.slug))
        else:
            flash('you must login in order to reply')
    return render_template('articles/view.html', article=article,
        next_article=next_article, related_articles=related_articles,
        comment_form=comment_form, comments=comments,
        reply_form=reply_form)



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






@articles.route('/category/')
def category_index():
    return redirect(url_for('articles.articles_index'))


@articles.route('/category/<slug>')
def view_category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    posts = category.posts.order_by(Article.post_date.desc()).limit(20)
    total_posts = category.posts.count()
    latest_2 = posts[0:2]
    more_recent = posts[2:5]
    the_rest = posts[5:9]
    # posts = Article.query.order_by(Article.post_date.desc()).limit(2)
    return render_template('articles/category-single.html',
        title=category.name,
        posts=posts,
        latest_2=latest_2,
        more_recent=more_recent,
        the_rest=the_rest,
        total_posts=total_posts,
        category=category)








@articles.route('/new', methods=['GET', 'POST'])
@login_required
def article_form():
    form = ArticleForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by('name')]

    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).first()
        article = Article(
            title=form.title.data,
            slug=form.slug.data,
            category=category,
            content=form.body.data,
            preview=form.preview.data,
            author=current_user._get_current_object()
            )
        db.session.add(article)
        return redirect(url_for('articles.read_article', slug=form.slug.data))
    return render_template('articles/new.html', title='New Article',form=form)
