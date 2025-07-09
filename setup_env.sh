#!/bin/bash

set -e

# Create virtual environment if not present or missing activate script
if [ ! -d "venv" ] || { [ ! -f "venv/bin/activate" ] && [ ! -f "venv/Scripts/activate" ]; }; then
    rm -rf venv
    python3 -m venv venv
fi

# Determine activation script based on OS
if [ -f "venv/bin/activate" ]; then
    ACTIVATE="venv/bin/activate"
else
    ACTIVATE="venv/Scripts/activate"
fi

# Activate virtual environment and install requirements
source "$ACTIVATE"
python -m pip install -r requirements.txt

deactivate

# Create .env from template if not exists
if [ ! -f ".env" ] && [ -f ".env.template" ]; then
    cp .env.template .env
    echo "Created .env from template. Please edit .env to set SECRET_KEY."
fi

echo "Environment setup complete."
