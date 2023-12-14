from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '47a715eeb9c3c884c12a4840c585244a'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'

    # Initialize the extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Import the models
    from models import User, Patient

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        # Import inside the function to avoid circular imports
        return User.query.get(int(user_id))

    # Create the tables within the application context
    with app.app_context():
        db.create_all()

    return app