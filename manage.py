import os
from app import create_app
from flask_migrate import MigrateCommand, Manager

from dotenv import load_dotenv
load_dotenv()

manager = Manager(create_app(os.environ.get('FLASK_CONFIG')))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()