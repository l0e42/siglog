#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number>"
    exit 1
fi

# Assign the provided number to a variable
number=$1

# Run the Python scripts with the specified number
python3 process.py $number
python3 html.py
python3 html.py email
python3 tex.py
