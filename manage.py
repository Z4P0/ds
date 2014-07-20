#!/Users/sumo/.virtualenvs/ds-site/bin/python
import os
from website import create_app, db
from website.models import User, Role, Cup, League, Team, Article, Category, Tag, Player, Manager, Association, Country
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,
        db=db,
        User=User,
        Role=Role,
        Cup=Cup,
        League=League,
        Team=Team,
        Article=Article,
        Category=Category,
        Tag=Tag,
        Player=Player,
        Manager=Manager,
        Association=Association,
        Country=Country
        )
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """ run the unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
