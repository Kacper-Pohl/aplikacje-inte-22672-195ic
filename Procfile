release: python manage.py migrate
web: gunicorn mysite.wsgi:application --preload --workers 1
