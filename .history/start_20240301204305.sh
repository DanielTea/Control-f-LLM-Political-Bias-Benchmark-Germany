#!/bin/bash

# Check if an argument is provided to run headless or not
# If argument is "true", run in headless mode; otherwise, run in non-headless mode
if [ "$1" = "true" ]; then
  export HEADLESS_MODE=true
else
  export HEADLESS_MODE=false
fi

# Activate the virtual environment
source .venv/bin/activate

# Execute the Python script
python script.py
