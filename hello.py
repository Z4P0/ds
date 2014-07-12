from flask import Flask, render_template
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)



@app.route('/')
def index():
	return render_template('ds/00-homepage.html',
		title = 'DS',
		description = 'Your source for the CONCACAF',
		page_id = 'homepage',
		data_page = 'homepage'
		)



# users
@app.route('/u/<user>')
def view_profile(user):
	return 'view profile: %s' % user






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












if __name__ == '__main__':
	manager.run()