release: mkdir users/migrations
release: touch users/migrations/__init__.py
release: mkdir job/migrations
release: touch job/migrations/__init__.py
release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn freelancing_backend.wsgi --log-file -
