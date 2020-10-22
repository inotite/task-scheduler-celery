from flask import Flask, send_from_directory, request, jsonify
import os
from flask_restful import Api

from app.config import config
from app.extensions import register_extensions, db
from app.controllers import register_apis
from app.models import Task
from app.services import reset_all_tasks
from celery import Celery
from celery.schedules import crontab
from celery.signals import task_postrun
from celery.utils.log import get_task_logger

flask_app = Flask(__name__)
flask_app.config.from_object(config)
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.url_map.strict_slashes = False

api = Api(flask_app)

@flask_app.route('/guides/<path>', methods=['GET'])
def send_guide(path):
    return send_from_directory('storage', path)

@flask_app.route('/tasks/complete', methods=['POST'])
def complete_tasks():
    ids = request.json['ids']
    print(ids)
    for id in ids:
        task = Task.query.filter(Task.id==id).one()
        task.completed = True
    db.session.commit()
    return jsonify({ 'status': True, 'message': 'Success' }), 201

register_extensions(flask_app)
register_apis(api)

flask_app.app_context().push()

def create_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["BROKER_URL"],
    )
    # celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

        def after_return(self, status, retval, task_id, args, kwargs, einfo):
            if app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']:
                if not isinstance(retval, Exception):
                    db.session.commit()
            if not celery.conf.ALWAYS_EAGER:
                db.session.remove()

    celery.Task = ContextTask
    return celery

celery = create_celery(flask_app)

logger = get_task_logger(__name__)

@celery.task
def reset_completed_tasks():
    print("Task called")
    reset_all_tasks()

@task_postrun.connect
def close_session(*args, **kwargs):
    db.session.remove()

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls reverse_messages every 10 seconds.
    # sender.add_periodic_task(10.0, reverse_messages, name="reverse every 10")

    # Calls log('Logging Stuff') every 30 seconds
    # sender.add_periodic_task(30.0, log.s(("Logging Stuff")), name="Log every 30")

    # Executes every Monday morning at 6:00 a.m.
    sender.add_periodic_task(
        crontab(hour='*', minute='19', day_of_week='mon-fri'), reset_completed_tasks, name="Reset Tasks"
    )
