from datetime import datetime
import hashlib
from flask import current_app, request
from . import db, login_manager
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach




class Permission:
    """ Various permissions for site users """
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    # UPDATE_STATS = 0x0f
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    """ Users can be admins, guests-posts, or regular """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        # roles = {
        #     'User': (Permission.FOLLOW |
        #              Permission.COMMENT, True),
        #     'Moderator': (Permission.FOLLOW |
        #                   Permission.COMMENT |
        #                   Permission.MODERATE_COMMENTS, False),
        #     'Contributor': (Permission.FOLLOW |
        #                     Permission.COMMENT |
        #                     Permission.WRITE_ARTICLES, False),
        #                     # Permission.UPDATE_STATS, False),
        #     'Writer': (Permission.WRITE_ARTICLES |
        #                Permission.COMMENT |
        #                Permission.FOLLOW, False),
        #     # 'Stats': (Permission.)
        #     'Administrator': (0xff, False)
        # }
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name




class User(UserMixin, db.Model):
    """ User information """
    __tablename__ = 'users'
    __searchable__ = ['username', 'twitter', 'instagram']
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(30), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128), nullable=True)
    twitter = db.Column(db.String(128), unique=True, nullable=True)
    instagram = db.Column(db.String(128), unique=True, nullable=True)
    location = db.Column(db.String(64))
    bio = db.Column(db.Text, nullable=True)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # profile_pic = db.Column(db.String(256))
    gravatar_hash = db.Column(db.String(64))
    # following
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Article', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['DS_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.gravatar_hash is None:
            self.gravatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    def change_email(self, token):
        self.email = new_email
        self.gravatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True


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

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon',rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://secure.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)



    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    """docstring for AnonymousUser"""
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






class Article(db.Model):
    """ Articles """
    __tablename__ = 'articles'
    __searchable__ = ['title', 'content', 'content_html', 'preview', 'preview_html']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    slug = db.Column(db.String(256), unique=True)
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    preview = db.Column(db.Text)
    preview_html = db.Column(db.Text)
    # leadin = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    post_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # tags - an article can have many tags
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'img', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    @staticmethod
    def on_changed_preview(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'img', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.preview_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Article %r>' % self.title

db.event.listen(Article.content, 'set', Article.on_changed_content)
db.event.listen(Article.preview, 'set', Article.on_changed_preview)


class Comment(db.Model):
    """ Article comments """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    edited = db.Column(db.Boolean)
    edit_timestamp = db.Column(db.DateTime, nullable=True)
    enabled = db.Column(db.Boolean, default=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    score = db.Column(db.Integer, default=1)
    reply_to_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    reply_to = db.relation('Comment', remote_side=[id], order_by='desc(Comment.timestamp)', backref='replies')
    # reply_to = db.relation('Comment', remote_side=[id], backref='replies')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote',
                        'em', 'i', 'img', 'li', 'ol', 'strong', 'ul',
                        'h1', 'h2', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
        target.edited = True
        edit_timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Comment %r>' % self.body

db.event.listen(Comment.body, 'set', Comment.on_changed_body)



class Topic(db.Model):
    """ Site Topics """
    __tablename__ = 'topics'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    slug = db.Column(db.String(128), unique=True)
    categories = db.relationship('Category', backref='topic', lazy='dynamic')
    default = db.Column(db.Boolean, default=False, index=True)

    @staticmethod
    def create_topics():
        topics = {
            'Clubs': ('clubs', False),
            'US': ('us', False),
            'MX': ('mx', False),
            'Series': ('series', False),
            'Other': ('other', True)
        }
        for t in topics:
            topic = Topic.query.filter_by(name=t).first()
            if topic is None:
                topic = Topic(name=t)
            topic.slug = topics[t][0]
            topic.default = topics[t][1]
            db.session.add(topic)
        db.session.commit()



    def __repr__(self):
        return '<Topic %r>' % self.name


class Category(db.Model):
    """ Articles categories """
    __tablename__ = 'categories'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    slug = db.Column(db.String(128), unique=True)
    posts = db.relationship('Article', backref='category', lazy='dynamic')
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    default = db.Column(db.Boolean, default=False, index=True)


    @staticmethod
    def create_categories():
        categories = {
            'Club America': ('club-america', 'clubs', False),
            'FC Buffalo': ('fc-buffalo', 'clubs', False),
            'New York Red Bulls': ('new-york-red-bulls', 'clubs', False),
            'Rochester Rhinos': ('rochester-rhinos', 'clubs', False),
            'Tottenham Hotspur': ('tottenham-hotspur', 'clubs', False),
            'MLS': ('mls','us', False),
            'NASL': ('nasl','us', False),
            'U.S. Open Cup': ('us-open-cup','us', False),
            'USL-Pro': ('usl-pro','us', False),
            'USMNT': ('usmnt','us', False),
            'Ascenso MX': ('ascenso-mx','mx',False),
            'Liga MX': ('liga-mx','mx',False),
            'El Tri': ('el-tri','mx',False),
            'College Soccer': ('college-soccer','series', False),
            'Cuba!': ('cuba','series', False),
            'Soccer In America': ('soccer-in-america','series', False),
            'Match Highlights': ('match-highlights','other',False),
            'Match Preview': ('match-preview','other',False),
            'Match Report': ('match-report','other',False),
            'Weekly Wrap-Up': ('weekly-wrap-up','other',False),
            'Attendances': ('attendances','other',False),
            'Important Other Stuff': ('important-other-stuff','other',True),
        }
        for c in categories:
            topic = Topic.query.filter_by(slug=categories[c][1]).first()
            category = Category.query.filter_by(name=c).first()
            if category is None:
                category = Category(name=c)
            category.slug = categories[c][0]
            category.default = categories[c][2]
            category.topic = topic
            db.session.add(topic)
        db.session.commit()

    def __repr__(self):
        return '<Category %r>' % self.name


class Tag(db.Model):
    """ Articles tags """
    __tablename__ = 'tags'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)
    # posts = db.relationship('Article', backref='tags', lazy='dynamic')
    def __repr__(self):
        return '<Tag %r>' % self.name







# cups
class Cup(db.Model):
    """ Cup tournaments """
    __tablename__ = 'cups'
    __searchable__ = ['name', 'abbreviation', 'overview']
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
    __searchable__ = ['name', 'abbreviation']
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
    __searchable__ = ['name', 'abbreviation', 'nickname']
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
    __searchable__ = ['common_name', 'fullname', 'bio']
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
    __searchable__ = ['name']
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
    __searchable__ = ['name']
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
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)
    # one governing body
    # fa_id = db.Column(db.Integer, db.ForeignKey('associations.id'))
    # many leagues in the country, but the FA is in charge of that

    def __repr__(self):
        return '<Country %r>' % self.name

