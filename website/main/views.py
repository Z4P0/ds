from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm, LoginForm, RegisterForm, ChangeEmailForm, ResetPasswordForm, CommentForm, FollowForm, SearchForm, ContactForm, ProfileForm, BookmarkForm, SubscribeForm, ChangePasswordForm



@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['DS_ADMIN']:
                send_email(current_app.config['DS_ADMIN'], 'New User',
                    'email/new-user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))

    return render_template('ds/00-homepage.html',
        title = 'DS',
        description = 'Your source for the CONCACAF',
        page_id = 'homepage',
        data_page = 'homepage',
        current_time = datetime.utcnow(),
        form = form,
        name = session.get('name'),
        known = session.get('known', False)
        )




# about
@main.route('/about/')
def about_ds():
    return 'Started in edgars room 4 years ago now'







# forms debug page
@main.route('/forms-test/', methods=['GET', 'POST'])
def debug_name_form():
    # pretty much all the info we can store on people..
    name_form = NameForm()
    if name_form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('changed your name huh? you still a bitch')
        session['name'] = name_form.name.data
        name_form.name.data = ''
        return redirect(url_for('debug_name_form'))

    return render_template('debug/forms-name.html',
        name_form = name_form,
        name = session.get('name')
        )


# forms debug page
@main.route('/forms/', methods=['GET', 'POST'])
def debug_forms():

    name_form = NameForm()
    if name_form.validate_on_submit():
        session['name'] = name_form.name.data
        return redirect(url_for('debug_forms'))


    login_form = LoginForm()
    if login_form.validate_on_submit():
        session['email'] = login_form.email.data
        session['password'] = login_form.password.data
        session['remember_me'] = login_form.remember_me.data
        return redirect(url_for('debug_forms'))


    register_form = RegisterForm()
    if register_form.validate_on_submit():
        session['username'] = register_form.username.data
        session['email'] = register_form.email.data
        session['password'] = register_form.password.data
        session['agree_to_terms'] = register_form.agree_to_terms.data
        return redirect(url_for('debug_forms'))


    changeemail_form = ChangeEmailForm()
    if changeemail_form.validate_on_submit():
        session['email'] = changeemail_form.email.data
        return redirect(url_for('debug_forms'))


    changepassword_form = ChangePasswordForm()
    if changepassword_form.validate_on_submit():
        session['current_password'] = changepassword_form.current_password.data
        session['new_password'] = changepassword_form.new_password.data
        return redirect(url_for('debug_forms'))


    resetpassword_form = ResetPasswordForm()
    if resetpassword_form.validate_on_submit():
        session['email'] = resetpassword_form.email.data
        return redirect(url_for('debug_forms'))


    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        session['body'] = comment_form.body.data
        session['follow_replies'] = comment_form.follow_replies.data
        return redirect(url_for('debug_forms'))


    follow_form = FollowForm()
    if follow_form.validate_on_submit():
        # session['#'] do something
        return redirect(url_for('debug_forms'))


    search_form = SearchForm()
    if search_form.validate_on_submit():
        session['text'] = search_form.text.data
        return redirect(url_for('debug_forms'))


    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        session['message'] = contact_form.message.data
        session['name'] = contact_form.name.data
        session['email'] = contact_form.email.data
        return redirect(url_for('debug_forms'))



    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        session['fullname'] = profile_form.fullname.data
        session['twitter'] = profile_form.twitter.data
        session['instagram'] = profile_form.instagram.data
        session['bio'] = profile_form.bio.data
        session['picture'] = profile_form.picture.data
        return redirect(url_for('debug_forms'))


    bookmark_form = BookmarkForm()
    if bookmark_form.validate_on_submit():
        # session['#'] do something
        return redirect(url_for('debug_forms'))


    subscribe_form = SubscribeForm()
    if subscribe_form.validate_on_submit():
        # session['#'] do something
        return redirect(url_for('debug_forms'))


    return render_template('debug/forms.html',
        name_form = name_form,
        login_form = login_form,
        register_form = register_form,
        changeemail_form = changeemail_form,
        changepassword_form = changepassword_form,
        resetpassword_form = resetpassword_form,
        comment_form = comment_form,
        follow_form = follow_form,
        search_form = search_form,
        contact_form = contact_form,
        profile_form = profile_form,
        bookmark_form = bookmark_form,
        subscribe_form = subscribe_form,
        name = session.get('name'),
        email = session.get('email'),
        password = session.get('password'),
        password2 = session.get('password2'),
        remember_me = session.get('remember_me'),
        username = session.get('username'),
        agree_to_terms = session.get('agree_to_terms'),
        text_body = session.get('text_body'),
        follow_replies = session.get('follow_replies'),
        search_text = session.get('search_text'),
        message = session.get('message'),
        fullname = session.get('fullname'),
        twitter = session.get('twitter'),
        instagram = session.get('instagram'),
        bio = session.get('bio'),
        picture = session.get('picture')
        )
