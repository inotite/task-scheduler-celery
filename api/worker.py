from celery import Celery
from celery.schedules import crontab

from api.app import create_worker_app
from api.celery_tasks.long_task import reset_completed_tasks


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

    celery.Task = ContextTask
    return celery


flask_app = create_worker_app()
celery = create_celery(flask_app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls reverse_messages every 10 seconds.
    # sender.add_periodic_task(10.0, reverse_messages, name="reverse every 10")

    # Calls log('Logging Stuff') every 30 seconds
    # sender.add_periodic_task(30.0, log.s(("Logging Stuff")), name="Log every 30")

    # Executes every Monday morning at 6:00 a.m.
    sender.add_periodic_task(
        crontab(hour='6,14,22', minute=0, day_of_week='mon-fri'), reset_completed_tasks, name="Reset Tasks"
    )
