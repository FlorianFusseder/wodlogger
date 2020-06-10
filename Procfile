web: gunicorn wodlogger.wsgi --log-file -
release: python manage.py migrate
release: python manage.py test