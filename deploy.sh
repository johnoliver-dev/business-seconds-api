#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting deployment of business-seconds-api..."

# Step 1: Create a Python virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Step 2: Activate the virtual environment
source venv/bin/activate

# Step 3: Install/update dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 4: Stop any existing running instance of the app
# pkill will send SIGTERM to any process with "gunicorn: master [app:app]"
# The -f flag matches against the full command line.
# The `|| true` prevents the script from exiting if no process is found.
echo "Stopping any existing Gunicorn process..."
pkill -f "gunicorn: master [app:app]" || true
sleep 2 # Give it a moment to shut down

# Step 5: Start the Flask application with Gunicorn
# -b: bind to address and port
# --daemon: run in the background
# --workers: number of worker processes (a good starting point is 2*CPU_CORES + 1)
# app:app: look for the 'app' object in the 'app.py' file
echo "Starting Gunicorn server in daemon mode..."
gunicorn --bind 0.0.0.0:5000 --daemon --workers 3 app:app

echo "Deployment complete. API is running on http://0.0.0.0:5000"
echo "To test the endpoint:"
echo "curl \"http://127.0.0.1:5000/calculate?start_time=2025-07-21T08:00:00Z&end_time=2025-07-21T17:00:00Z\""