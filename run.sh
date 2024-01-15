#!/bin/bash

VENV_FOLDER="venv"
REQUIREMENTS_FILE="requirements.txt"

# Check if virtual environment folder exists
if [ ! -d "$VENV_FOLDER" ]; then
    echo "LOG: Virtual environment not found. Creating..."
    python3 -m venv "$VENV_FOLDER"
    echo "LOG: Virtual environment created."
fi

# Activate the virtual environment
source "$VENV_FOLDER/bin/activate"

echo "LOG: Virtual environment is activated."
echo "LOG: Checking if pip is in VENV."

# Check if pip is installed in the virtual environment
pip --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "LOG: Installing pip in the virtual environment..."
    python -m ensurepip
    echo "LOG: pip successfully installed."
fi

# Check if requirements are already installed
REQUIREMENTS_MET=true
while IFS= read -r req; do
    PACKAGE_FOUND=false
done < "$REQUIREMENTS_FILE"

for package in "$VENV_FOLDER/lib/python*/site-packages/"*; do
    while IFS= read -r req; do
        if [[ "$package" == *"$req"* ]]; then
            PACKAGE_FOUND=true
            break
        fi
    done < "$REQUIREMENTS_FILE"
done

if [ "$PACKAGE_FOUND" == "false" ]; then
    REQUIREMENTS_MET=false
    echo "LOG: Some requirements are missing."
fi

if [ "$REQUIREMENTS_MET" == "false" ]; then
    echo "LOG: Installing requirements..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "LOG: Requirements are already installed."
fi

MODELFOLDER="ssd_mobilenetv2_coco"

# Check if the folder exists
if [ ! -d "$MODELFOLDER" ]; then
    echo "LOG: Model folder does not exist. Creating..."
    mkdir "$MODELFOLDER"
    if [ $? -ne 0 ]; then
        echo "LOG: Failed to create model folder. Aborting."
        exit 1
    else
        echo "LOG: Model folder created successfully."
    fi
fi

echo ""
echo "LOG: Starting the script"
# Run the Python script
python person_autocrop.py
