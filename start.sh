#!/bin/bash

echo "========================================"
echo "AI Automated Red Team Agent (AARTA)"
echo "========================================"
echo
echo "Starting AARTA Web Interface..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
if ! pip show fastapi > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Dependencies installed."
    echo
fi

# Start the server
echo
echo "========================================"
echo "AARTA is starting..."
echo "========================================"
echo
echo "Frontend URL: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo

python app/main.py
