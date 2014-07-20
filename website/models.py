from flask import current_app
from . import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as  Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Article(db.Model):
    """ Articles """
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    slug = db.Column(db.String(256), unique=True)
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    post_date = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime, nullable=True)
    # tags - an article can have many tags
    # comments - an article can have many comments


class Category(db.Model):
    """ Articles categories """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    slug = db.Column(db.String(128), unique=True)
    posts = db.relationship('Article', backref='category', lazy='dynamic')


class Tag(db.Model):
    """ Articles tags """
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)
    # posts = db.relationship('Article', backref='tags', lazy='dynamic')




class Role(db.Model):
    """ Users can be admins, guests-posts, or regular """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    """ User information """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(30), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128), nullable=True)
    twitter = db.Column(db.String(128), unique=True, nullable=True)
    instagram = db.Column(db.String(128), unique=True, nullable=True)
    # bio = db.Column(db.Text, nullable=True)
    # profile_pic = db.Column(db.String(256))
    # date_joined = db.Column(db.Date)
    # comments
    # following
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<User %r>' % self.username

# cups
class Cup(db.Model):
    """ Cup tournaments """
    __tablename__ = 'cups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    abbreviation = db.Column(db.String(16), unique=True, nullable=True)
    slug = db.Column(db.String(128), unique=True, nullable=True)
    twitter = db.Column(db.String(128), unique=True, nullable=True)
    overview = db.Column(db.Text, nullable=True)
    # current_winner
    # past_winners
    # year

    def __repr__(self):
        return '<Cup %r>' % self.name


# leagues
class League(db.Model):
    """ Leagues in the CONCACAF """
    __tablename__ = 'leagues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    abbreviation = db.Column(db.String(16), unique=True, nullable=True)
    slug = db.Column(db.String(128), unique=True, nullable=True)
    twitter = db.Column(db.String(128), unique=True, nullable=True)
    teams = db.relationship('Team', backref='league', lazy='dynamic')

    def __repr__(self):
        return '<League %r>' % self.name


# teams
class Team(db.Model):
    """ Teams that play in the CONCACAF """
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    abbreviation = db.Column(db.String(16), unique=True, nullable=True)
    nickname = db.Column(db.String(64), nullable=True)
    slug = db.Column(db.String(128), unique=True, nullable=True)
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'))
    # other_leagues =
    twitter = db.Column(db.String(128), unique=True, nullable=True)
    # players - a team has many players
    # manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))

    def __repr__(self):
        return '<Team %r>' % self.name


class Player(db.Model):
    """ players """
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(64))
    fullname = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    # team - current team
    # has many past teams
    bio = db.Column(db.Text)
    born = db.Column(db.Date)
    # nationality_id = db.Column(db.Integer, db.ForeignKey('countries.id'))

    def __repr__(self):
        return '<Player %r>' % self.common_name


class Manager(db.Model):
    """ Managers in the CONCACAF """
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    # is working?
    active = db.Column(db.Boolean)
    # team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    def __repr__(self):
        return '<Manager %r>' % self.name


class Association(db.Model):
    """ Associations in the CONCACAF """
    __tablename__ = 'associations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    # belong to one country..?
    # country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))

    def __repr__(self):
        return '<Association %r>' % self.name



class Country(db.Model):
    """ A Country - a footballing nation """
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)
    # one governing body
    # fa_id = db.Column(db.Integer, db.ForeignKey('associations.id'))
    # many leagues in the country, but the FA is in charge of that

    def __repr__(self):
        return '<Country %r>' % self.name
