# Set FLASK_APP environment variable
export FLASK_APP=app.py

flask db init
flask db migrate -m "Initial migration."
flask db upgrade

# Run database migrations
flask db upgrade

# Start the Flask app
flask run --debug --debugger --reload
