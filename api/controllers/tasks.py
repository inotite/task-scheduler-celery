from flask_restful import Resource, reqparse
from ..models import Task, tasks_schema, task_schema
from ..extensions import db

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('completed', type=bool)
parser.add_argument('machine')

class TaskListSchema(Resource):
    def get(self):
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)
    
    def post(self):
        args = parser.parse_args()
        new_task = Task(
            name = args['name'],
            machine = args['machine'],
            description = args['description'],
            completed = args['completed'],
            guide = ''
        )
        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task), 201

def register_api(api):
    api.add_resource(TaskListSchema, '/tasks')