from api.extensions import db, ma

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    machine = db.Column(db.String())
    completed = db.Column(db.Boolean)
    name = db.Column(db.String())
    guide = db.Column(db.String())
    description = db.Column(db.String())
    
    def __init__(self, machine, completed, name, guide, description):
        self.machine = machine
        self.completed = completed
        self.name = name
        self.guide = guide
        self.description = description
    
    def __repr__(self):
        return '<id {}>'.format(self._id)
    
class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "completed", "machine", "name", "guide", "description")
        
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
    