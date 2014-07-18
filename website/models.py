from . import db

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
