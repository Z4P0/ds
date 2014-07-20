To run the site locally:
$ python manage.py runserver

On a WiFi network:
python hello.py runserver --host 0.0.0.0



Dev setup:
export MAIL_USERNAME=yourusername@gmail.com
export MAIL_PASSWORD=password
export DS_ADMIN=other@gmail.com
# optional
export SECRET_KEY='secret_keyLOLOL'
export FLASK_CONFIG='development'

Initial setup:

- Create user roles
$ ./manage.py shell
>>> Role.insert_roles()

