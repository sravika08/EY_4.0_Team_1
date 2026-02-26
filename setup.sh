#!/bin/bash
# Quick Start Script for College Attendance Management System

echo "Starting College Attendance Management System Setup..."
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [ "$OSTYPE" == "msys" ] || [ "$OSTYPE" == "win32" ]; then
    venv\Scripts\activate
else
    source venv/bin/activate
fi

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "Creating admin superuser..."
echo "Please enter the following details:"
python manage.py createsuperuser

# Run server
echo ""
echo "Starting development server..."
echo "The application will be available at http://127.0.0.1:8000"
python manage.py runserver
