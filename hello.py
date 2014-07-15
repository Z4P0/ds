from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.moment import Moment

from datetime import datetime

from forms import NameForm, LoginForm, RegisterForm, ChangeEmailForm, ResetPasswordForm, CommentForm, FollowForm, SearchForm, ContactForm, ProfileForm, BookmarkForm, SubscribeForm, ChangePasswordForm



app = Flask(__name__)
app.config['SECRET_KEY'] = 'development sceret key fsd'

manager = Manager(app)
moment = Moment(app)




# forms debug page
@app.route('/forms/')
def debug_forms():
	name_form = NameForm()
	login_form = LoginForm()
	register_form = RegisterForm()
	changeemail_form = ChangeEmailForm()
	changepassword_form = ChangePasswordForm()
	resetpassword_form = ResetPasswordForm()
	comment_form = CommentForm()
	follow_form = FollowForm()
	search_form = SearchForm()
	contact_form = ContactForm()
	profile_form = ProfileForm()
	bookmark_form = BookmarkForm()
	subscribe_form = SubscribeForm()
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
		subscribe_form = subscribe_form
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