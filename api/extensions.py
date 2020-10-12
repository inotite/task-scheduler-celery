from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
celery = Celery('backend')

def register_extensions(app, worker=False):
    db.init_app(app)
    ma.init_app(app)
    
    CORS(app)

    # load celery config
    celery.config_from_object(app.config)

    if not worker:
        # register celery irrelevant extensions
        pass
