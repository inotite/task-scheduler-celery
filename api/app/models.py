from app.extensions import db, ma

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    machine = db.Column(db.String())
    completed = db.Column(db.Boolean)
    name = db.Column(db.String())
    guide = db.Column(db.String())
    description = db.Column(db.String())
    hours = db.Column(db.String())
    
    def __init__(self, machine, completed, name, guide, description, hours):
        self.machine = machine
        self.completed = completed
        self.name = name
        self.guide = guide
        self.description = description
        self.hours = hours
    
    def __repr__(self):
        return '<id {}> <name {}>'.format(self.id, self.name)
    
class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "completed", "machine", "name", "guide", "description", "hours")
        
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
    