#!/bin/bash
# install.sh - Script to install pych-gui
#
# Author: Yecid Moreno <GitHub @YecidMoreno> <Email yecidmoreno@alumni.usp.br>
# Created: 2025-10-25
# Description: Script to install pych-gui
#
# Usage:
#   ./install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="pych-gui.sh"
TARGET="/usr/local/bin/pych-gui"

# Create a virtual environment
VENV_DIR="$SCRIPT_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating a virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
else
    echo "The virtual environment already exists in $VENV_DIR."
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"
echo "Virtual environment activated."

# Check if pip is installed in the virtual environment
if ! command -v pip &> /dev/null; then
    echo "pip is not available in the virtual environment. Please check the Python installation."
    deactivate
    exit 1
fi

# Install requirements from requirements.txt
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
    echo "Dependencies installed successfully."
else
    echo "requirements.txt file not found. Make sure to generate it before running this script."
    deactivate
    exit 1
fi

pip install pyqtdarktheme

chmod +x "$SCRIPT_DIR/$SCRIPT_NAME"

sudo ln -sf "$SCRIPT_DIR/$SCRIPT_NAME" "$TARGET"

echo "pych-gui installed successfully at $TARGET"

deactivate

