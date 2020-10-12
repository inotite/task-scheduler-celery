from flask import Flask, send_from_directory
import os
from flask_restful import Api

from .config import config
from .extensions import register_extensions
from .controllers import register_apis

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False
    
    api = Api(app)
    
    @app.route('/guides/<path>', methods=['GET'])
    def send_guide(path):
        return send_from_directory('storage', path)
    
    register_extensions(app)
    register_apis(api)

    return app

def create_worker_app():
    """Minimal App without routes for celery worker."""
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    register_extensions(app, worker=True)

    return app
