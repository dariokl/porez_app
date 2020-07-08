import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from flask_migrate import Migrate

app = create_app(os.environ.get('FLASK_CONFIG'))
Migrate(app, db)