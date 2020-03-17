# start.sh

# RUN IN Flask WSGI SERVER
# export FLASK_APP=wsgi.py
# export FLASK_DEBUG=1
# export APP_CONFIG_FILE=config.ini
# flask run

# RUN IN GUNICORN SERVER
gunicorn wsgi:app
