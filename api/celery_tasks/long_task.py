from celery.signals import task_postrun
from celery.utils.log import get_task_logger

from ..extensions import db, celery
from ..models import Task

logger = get_task_logger(__name__)


@celery.task
def reset_completed_tasks():
    Task.query.all().update({ Task.completed: False })
    db.session.commit()

@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.session.remove()
