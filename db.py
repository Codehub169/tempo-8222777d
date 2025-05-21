from flask import current_app
from flask.cli import with_appcontext
import click
from .models import db # Import db instance from models.py

def init_db():
    # Import all models here to ensure they are registered with SQLAlchemy
    from .models import User, Quiz, Question, QuestionOption 
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Register database functions with the Flask app."""
    db.init_app(app) # Initialize db with the app
    app.cli.add_command(init_db_command)
