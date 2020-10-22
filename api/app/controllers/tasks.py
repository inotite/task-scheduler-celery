from flask_restful import Resource, reqparse, abort
import json
from celery import Celery
from app.models import Task, tasks_schema, task_schema
from app.extensions import db

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('completed', type=bool)
parser.add_argument('machine')
parser.add_argument('schedule')

def abort_if_task_deosnt_exist(task_id):
    if Task.query.get(task_id) is None:
        abort(404, message="Task {} doesn't exist".format(task_id))

class TaskList(Resource):
    def get(self):
        tasks = Task.query.filter(Task.completed == False).all()
        return tasks_schema.dump(tasks)
    
    def post(self):
        args = parser.parse_args()
        new_task = Task(
            name = args['name'],
            machine = args['machine'],
            description = args['description'],
            completed = args['completed'],
            guide = '',
            hours = args['schedule']
        )
        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task), 201

class TaskApi(Resource):
    def get(self, task_id):
        abort_if_task_deosnt_exist(task_id)
        return task_schema.dump(Task.query.get(task_id))
    
    def put(self, task_id):
        abort_if_task_deosnt_exist(task_id)
        args = parser.parse_args()
        schedule = json.loads(args['schedule'].replace("\'", "\""))
        print(args)
        task = Task.query.get(task_id)
        task.hours = args['schedule']
        db.session.commit()
        return task_schema.dump(Task.query.get(task_id)), 201
    

def register_api(api):
    api.add_resource(TaskList, '/tasks')
    api.add_resource(TaskApi, '/tasks/<task_id>')
    