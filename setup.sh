#!/bin/bash

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install

# Run the main script
python scrapper.py