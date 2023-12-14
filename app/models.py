from flask_login import UserMixin
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    illness = db.Column(db.String(200), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Create the tables within the application context
with app.app_context():
    db.create_all()
