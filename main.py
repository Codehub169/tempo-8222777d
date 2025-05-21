import os
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db  # Import the db instance from models.py
from auth import auth_bp, load_user as auth_load_user
from main_routes import main_bp
import db as db_module # For registering CLI commands

login_manager = LoginManager()

def create_app(config_class=Config):
    """
    Application factory function to create and configure the Flask app.
    Args:
        config_class (class): The configuration class to use (e.g., Config from config.py).
    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        app.logger.error(f"Error creating instance folder {app.instance_path}: {e}")

    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError as e:
        app.logger.error(f"Error creating upload folder {app.config['UPLOAD_FOLDER']}: {e}")

    # Initialize Flask extensions with the app
    db.init_app(app)  # Initialize the db instance imported from models.py
    login_manager.init_app(app)
    db_module.register_db_commands(app) # Register CLI commands like init-db

    # Configure Flask-Login
    login_manager.user_loader(auth_load_user)
    login_manager.login_view = 'auth.login' # Route in auth_bp for login
    login_manager.login_message_category = 'info'

    # Register Blueprints
    app.register_blueprint(main_bp) 
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

# Create the Flask app instance using the factory.
app = create_app()

if __name__ == '__main__':
    # debug=True is useful for development. 
    # The logic below determines debug status based on app.config['DEBUG'] (if set, e.g., by FLASK_DEBUG env var),
    # or falls back to checking FLASK_ENV. This ensures 'python main.py' behaves consistently.
    is_debug_mode = app.config.get('DEBUG', str(os.environ.get('FLASK_ENV', 'development')).lower() == 'development')
    app.run(host='0.0.0.0', port=9000, debug=is_debug_mode)
