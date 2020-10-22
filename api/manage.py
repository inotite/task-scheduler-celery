import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.config import config

from app.app import flask_app
from app.extensions import db

flask_app.config.from_object(config)

migrate = Migrate(flask_app, db)
manager = Manager(flask_app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()