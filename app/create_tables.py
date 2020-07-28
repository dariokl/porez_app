from app import create_app, db

with app.app_context():
    db.create_all()