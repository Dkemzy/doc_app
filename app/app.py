from flask import Flask
from flask_login import LoginManager
from models import db, User, Patient
import os

file_path = os.path.abspath(os.getcwd())+"\instance\database.db"

# Initialize the extensions
login_manager = LoginManager()


def create_app():
    # Create and configure the app
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '47a715eeb9c3c884c12a4840c585244a'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
    # Register the blueprint

    # Initialize the extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Import the blueprint from main module and register it with the app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        # Import inside the function to avoid circular imports
        return User.query.get(int(user_id))

    # Create the tables within the application context
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5030)
