from celery import Celery
from flask import Flask

def make_celery(app=None):
    app = app or Flask(__name__)
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['RESULT_BACKEND'] 
    )
    celery.conf.update(app.config)
    print(app.config['RESULT_BACKEND'])

    return celery

# Create the Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Celery initilization
celery = make_celery(app)
