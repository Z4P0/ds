import os
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager, Shell
from flask.ext.moment import Moment
from forms import NameForm, LoginForm, RegisterForm, ChangeEmailForm, ResetPasswordForm, CommentForm, FollowForm, SearchForm, ContactForm, ProfileForm, BookmarkForm, SubscribeForm, ChangePasswordForm
from flask_wtf.csrf import CsrfProtect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail, Message


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development sceret key fsd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '(DS)'
app.config['FLASKY_MAIL_SENDER'] = 'DS Admin <ds.admin@dohertysoccer.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('ADMIN')

manager = Manager(app)
moment = Moment(app)
csrf = CsrfProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)





class Role(db.Model):
    """ Users can be admins, guests-posts, or regular """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    """ User information """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    fullname = db.Column(db.String(128), nullable=True)
    twitter = db.Column(db.String(128), unique=True, nullable=True)
    instagram = db.Column(db.String(128), unique=True, nullable=True)
    # email = db.Column(db.String(128), unique=True)
    # bio = db.Column(db.Text, nullable=True)
    # profile_pic = db.Column(db.String(256))
    # date_joined = db.Column(db.Date)
    # password = 
    # validated
    # comments
    # following
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username





def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)



@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                    'email/new-user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))

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



@csrf.error_handler
def csrf_error(reason):
    return render_template('csrf_error.html', reason=reason), 400

# forms debug page
@app.route('/forms-test/', methods=['GET', 'POST'])
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
@app.route('/forms/', methods=['GET', 'POST'])
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


# users
@app.route('/u/<user>')
def view_profile(user):
    return render_template('ds/03-profile.html',
        title = user,
        description = 'Profile for user',
        data_page = 'profile',
        username = user
        )






# articles
@app.route('/articles/')
def articles_index():
    return 'all articles'

@app.route('/articles/<slug>')
def read_article(slug):
    return 'article: %s' % slug




# cups
@app.route('/cups/')
def cups_index():
    return 'all cups in the CONCACAF'

@app.route('/cups/<cup>')
def show_cup(cup):
    return 'all about the %s' % cup




# leagues
@app.route('/leagues/')
@app.route('/ligas/')
def leagues_index():
    return 'all leagues in the CONCACAF'

@app.route('/leagues/<league>')
@app.route('/ligas/<league>')
def show_league(league):
    return 'all about %s' % league




# teams
@app.route('/teams/')
def teams_index():
    return 'all teams in the CONCACAF'

@app.route('/teams/<team>')
def show_team(team):
    return 'all about %s' % team




# players
@app.route('/players/')
def players_index():
    return 'all players in the CONCACAF'

@app.route('/players/<player>')
def show_player(player):
    return 'all about %s' % player




# managers
@app.route('/managers/')
def managers_index():
    return 'all managers in the CONCACAF'

@app.route('/managers/<manager>')
def show_manager(manager):
    return 'all about %s' % manager




# settings
@app.route('/settings/')
def change_settings():
    return 'cahnge site settings for user'




# search
@app.route('/search/')
def search_ds():
    return 'Search'



# about
@app.route('/about/')
def about_ds():
    return 'Started in edgars room 4 years ago now'




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500




def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()