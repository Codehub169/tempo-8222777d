import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
# login_manager.login_view and user_loader will be configured later
# when auth blueprints and User model are defined.

def create_app(config_class=Config):
    """
    Application factory function to create and configure the Flask app.
    Args:
        config_class (class): The configuration class to use (e.g., Config from config.py).
    Returns:
        Flask: The configured Flask application instance.
    """
    # Create Flask app instance. 
    # instance_relative_config=True allows loading config from 'instance' folder (e.g., instance/config.py)
    # and sets app.instance_path to project_root/instance/
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration from the provided config class
    app.config.from_object(config_class)

    # Ensure the instance folder exists (Flask might create it for SQLite if path is relative to instance_path)
    # app.instance_path is automatically set by Flask when instance_relative_config=True
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        app.logger.error(f"Error creating instance folder {app.instance_path}: {e}")

    # Ensure upload folder exists, as defined in Config
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError as e:
        app.logger.error(f"Error creating upload folder {app.config['UPLOAD_FOLDER']}: {e}")

    # Initialize Flask extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # === Placeholder for future additions ===
    # User loader for Flask-Login (requires User model from models.py)
    # @login_manager.user_loader
    # def load_user(user_id):
    #     from models import User # To be created in models.py
    #     return User.query.get(int(user_id))

    # Configure login view for Flask-Login (requires auth blueprint)
    # login_manager.login_view = 'auth_bp.login' # Example, 'auth_bp' is blueprint name, 'login' is route name
    # login_manager.login_message_category = 'info' # Category for flashed messages

    # Register Blueprints (routes will be defined in separate files/modules)
    # from .routes.main_routes import main_bp # Example structure
    # app.register_blueprint(main_bp)
    # from .routes.auth_routes import auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # ... other blueprints for quiz generation, history, etc.

    # A simple root route to confirm the app is running
    @app.route('/')
    def index():
        # This will eventually render the main page using templates/index.html
        return "Welcome to the Quiz Generator App! Backend is active and running."

    # CLI command for database initialization (requires models.py)
    # @app.cli.command("init-db")
    # def init_db_command():
    #     """Clears existing data and creates new tables based on models."
    #     # Import models here to ensure they are registered with SQLAlchemy
    #     import models 
    #     with app.app_context():
    #         db.drop_all() # Use with caution, drops all tables
    #         db.create_all()
    #     print("Initialized the database and created tables.")

    return app

# Create the Flask app instance using the factory.
# This 'app' instance is what `flask run` (called by startup.sh) will use.
app = create_app()

# The following block is for running the app directly with `python app.py`.
# However, `flask run` is the recommended way for development and is used by startup.sh.
# if __name__ == '__main__':
# Ensure host is '0.0.0.0' to be accessible externally, and port 9000 as required.
# app.run(host='0.0.0.0', port=9000, debug=app.config.get('DEBUG', False))
