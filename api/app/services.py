from app.models import Task
from app.extensions import db
from app.db import db_session
import json
import datetime as dt

def reset_all_tasks():
  today = dt.datetime.today()
  weekday = today.weekday()
  month = today.month
  hour = today.hour
  for task in db_session.query(Task).all():
    if not task.hours:
      continue
    schedule = json.loads(task.hours.replace("\'", "\""))
    if not (schedule['month_of_year'] == '*' or month in set([int(mnt) for mnt in schedule['month_of_year'].split(',')])):
      continue
    if not (schedule['day_of_week'] == '*' or weekday in set([int(week) for week in schedule['day_of_week'].split(',')])):
      continue
    hours = set([int(hr) for hr in schedule['hour'].split(',')])
    if not hour in hours:
      continue
    print(task)
    task.completed = False
  db_session.flush()
  db_session.commit()
  