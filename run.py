import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from flask_migrate import Migrate

app = create_app('production')
Migrate(app, db)