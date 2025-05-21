from flask.cli import with_appcontext
import click
from .models import db # Import db instance from models.py

def init_db():
    # Import all models here to ensure they are registered with SQLAlchemy
    # This is crucial for db.create_all() to know about all tables.
    from .models import User, Quiz, Question, QuestionOption 
    # db.drop_all() # Optional: drop tables before creating. Use with caution in development.
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data (if db.drop_all() is uncommented) and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def register_db_commands(app):
    """Register database CLI commands with the Flask app."""
    # db.init_app(app) is called in main.py's create_app function.
    app.cli.add_command(init_db_command)
