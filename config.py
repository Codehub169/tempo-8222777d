import os
from dotenv import load_dotenv

# Determine the project root directory (assuming config.py is in the project root)
project_root = os.path.abspath(os.path.dirname(__file__))

# Construct the path to the .env file located in the project root
dotenv_path = os.path.join(project_root, '.env')

# Load environment variables from the .env file
# If .env doesn't exist, it will not raise an error, and os.environ.get will return None or default.
load_dotenv(dotenv_path)

class Config:
    """Configuration class for the Flask application."""
    
    # Secret key for session management, CSRF protection, etc.
    # Loaded from .env or uses a default (less secure, should be overridden in .env).
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'a-default-fallback-secret-key-change-this'

    # Database configuration
    # Uses DATABASE_URL from .env if set, otherwise defaults to SQLite in 'instance' folder.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              f"sqlite:///{os.path.join(project_root, 'instance', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disables SQLAlchemy event system overhead if not used.

    # Gemini API Key for quiz generation services
    # Loaded from .env file.
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    # File upload settings
    # Folder to store uploaded files, located in the project root.
    UPLOAD_FOLDER = os.path.join(project_root, 'uploads')
    # Allowed file extensions for uploads.
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    # Maximum allowed file size for uploads (e.g., 16MB).
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 

    # Flask specific settings (can be extended)
    # DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't') # Example for debug mode
