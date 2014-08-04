import os
from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash, request, send_from_directory, g
from flask.ext.login import login_required, current_user
from werkzeug.utils import secure_filename
from .. import db
from ..models import User, Article
from ..email import send_email
from . import main
from .forms import ProfileForm, UploadForm, SearchForm


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@main.route('/uploads/<filename>')
def view_uploaded_media(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename=filename)

@main.route('/media/<filename>')
def media(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename=filename)


@main.route('/upload', methods=['GET','POST'])
@login_required
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        uploaded_file = request.files['media']
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main.view_uploaded_media', filename=filename))
    return render_template('ds/uploads.html', form=form)


@main.route('/', methods=['GET', 'POST'])
def index():
    articles = Article.query.order_by(Article.post_date.desc())
    latest_post = articles.first()
    recent_posts = articles[1:5]

    return render_template('ds/index.html',
        title = 'DS',
        description = 'Your source for the CONCACAF',
        page_id = 'homepage',
        data_page = 'homepage',
        latest_post=latest_post,
        recent_posts=recent_posts
        )


# about
@main.route('/about')
def about_ds():
    return render_template('ds/about.html')


# privacy
@main.route('/privacy-policy')
def privacy_policy():
    return 'DS privacy policy'



# settings
@main.route('/settings')
def change_settings():
    return 'cahnge site settings for user'

# search
@main.route('/search', methods=['GET', 'POST'])
def search():
    query = None
    search_results = None
    search_form = SearchForm()
    if search_form.validate_on_submit():
        query = search_form.text.data
        search_results = Article.query.whoosh_search(query, current_app.config['MAX_SEARCH_RESULTS']).all()
    if g.search_form.validate_on_submit():
        query = g.search_form.text.data
        search_results = Article.query.whoosh_search(query, current_app.config['MAX_SEARCH_RESULTS']).all()
    return render_template('ds/search.html',
        search_form=search_form,
        query=query, search_results=search_results)



@main.route('/u/<username>', methods=['GET','POST'])
def view_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.fullname = form.fullname.data
        current_user.twitter = form.twitter.data
        current_user.instagram = form.instagram.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user)
        flash('Your profile has been updated!')
        return redirect(url_for('.view_profile', username=current_user.username))
    form.fullname.data = current_user.fullname
    form.twitter.data = current_user.twitter
    form.instagram.data = current_user.instagram
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    form.fullname.data = current_user.fullname

    return render_template('ds/profile.html', user=user, form=form)


@main.route('/u/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.fullname = form.fullname.data
        current_user.twitter = form.twitter.data
        current_user.instagram = form.instagram.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user)
        flash('Your profile has been updated!')
        return redirect(url_for('.view_profile', username=current_user.username))
    form.fullname.data = current_user.fullname
    form.twitter.data = current_user.twitter
    form.instagram.data = current_user.instagram
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    form.fullname.data = current_user.fullname
