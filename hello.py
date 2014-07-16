from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager
from flask.ext.moment import Moment

from datetime import datetime

from forms import NameForm, LoginForm, RegisterForm, ChangeEmailForm, ResetPasswordForm, CommentForm, FollowForm, SearchForm, ContactForm, ProfileForm, BookmarkForm, SubscribeForm, ChangePasswordForm
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'development sceret key fsd'

csrf = CsrfProtect(app)
manager = Manager(app)
moment = Moment(app)



@csrf.error_handler
def csrf_error(reason):
		return render_template('csrf_error.html', reason=reason), 400

# forms debug page
@app.route('/forms-test/', methods=['GET', 'POST'])
def debug_name_form():
		# pretty much all the info we can store on people..
		name_form = NameForm()
		if name_form.validate_on_submit():
			session['name'] = name_form.name.data
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


@app.route('/')
def index():
		form = NameForm()

		return render_template('ds/00-homepage.html',
				title = 'DS',
				description = 'Your source for the CONCACAF',
				page_id = 'homepage',
				data_page = 'homepage',
				current_time = datetime.utcnow(),
				form = form
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





if __name__ == '__main__':
		manager.run()