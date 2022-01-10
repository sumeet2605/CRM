python3 manage.py collectstatic --no-input

python manage.py migrate

gunicorn --worker-tmp-dir /dev/shm rizcrm.wsgi