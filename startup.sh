#!/bin/bash
set -euo pipefail # Exit on error, treat unset variables as error, and fail pipeline if any command fails

echo "Starting Quiz Generator application setup..."

# Determine Project root directory (assuming startup.sh is in the root)
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# 1. Install dependencies
echo "Installing dependencies from requirements.txt..."
if ! pip install -r "$PROJECT_ROOT/requirements.txt"; then
    echo "Failed to install dependencies. Please check pip and requirements.txt. Exiting."
    exit 1
fi

# 2. Create .env file if it doesn't exist and populate it
ENV_FILE="$PROJECT_ROOT/.env"

# Ensure GEMINI_API_KEY is set (using provided key)
GEMINI_API_KEY_VALUE="AIzaSyByaEYL6YvCbPHOa2jQscEGmfdYrSjiOjw"
if ! grep -q "^GEMINI_API_KEY=" "$ENV_FILE" 2>/dev/null; then
    echo "GEMINI_API_KEY='${GEMINI_API_KEY_VALUE}'" >> "$ENV_FILE"
    echo "Added GEMINI_API_KEY to .env file."
else
    # If key exists but has different value, update it (optional, depends on desired behavior)
    # For now, we assume if it exists, it's correctly set by the user or a previous run.
    echo "GEMINI_API_KEY already in .env file."
fi

# Ensure FLASK_SECRET_KEY is set
if ! grep -q "^FLASK_SECRET_KEY=" "$ENV_FILE" 2>/dev/null; then
    echo "Generating FLASK_SECRET_KEY..."
    FLASK_SECRET=$(python -c 'import secrets; print(secrets.token_hex(24))')
    echo "FLASK_SECRET_KEY='$FLASK_SECRET'" >> "$ENV_FILE"
    echo "Added FLASK_SECRET_KEY to .env file."
else
    echo "FLASK_SECRET_KEY already in .env file."
fi

# 3. Create instance folder for SQLite DB and uploads folder
INSTANCE_FOLDER="$PROJECT_ROOT/instance"
UPLOADS_FOLDER="$PROJECT_ROOT/uploads"

if [ ! -d "$INSTANCE_FOLDER" ]; then
    echo "Creating instance folder for database at $INSTANCE_FOLDER..."
    mkdir -p "$INSTANCE_FOLDER"
fi

if [ ! -d "$UPLOADS_FOLDER" ]; then
    echo "Creating uploads folder at $UPLOADS_FOLDER..."
    mkdir -p "$UPLOADS_FOLDER"
fi

# 4. Set Flask environment variables
export FLASK_APP="main.py" # Changed from app.py to main.py
export FLASK_ENV="development" # Can be set to 'production' for deployment
# FLASK_DEBUG=1 can also be set for more verbose development output

# 5. Database Initialization Note
# Actual database table creation (e.g., via 'flask init-db') will be performed
# once models are defined and the corresponding CLI command is implemented in main.py.
# SQLAlchemy will create the SQLite DB file on first access if it doesn't exist.
echo "Database file will be created in '$INSTANCE_FOLDER' if it doesn't exist upon app start."
echo "Run 'flask init-db' to create tables after models are defined."

# 6. Run the Flask application on port 9000
# The user might run 'python main.py' directly.
# This line is for running via 'flask run' if preferred.
echo "Starting Flask application on http://0.0.0.0:9000 (via flask run)..."
echo "Alternatively, you can run 'python main.py'"
flask run --host=0.0.0.0 --port=9000
