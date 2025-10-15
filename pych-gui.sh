#!/bin/bash
# pych-gui - Python C++ GUI Builder
#
# Author: Yecid Moreno <GitHub @YecidMoreno> <Email yecidmoreno@alumni.usp.br>
# Created: 2025-10-25
# Description: Script to build and run the pych-gui application
#
# Usage:
#   ./pych-gui.sh

# Detect the real location of the script even if it is a symbolic link
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
source "$VENV_DIR/bin/activate"

# Change to the project directory
cd "$SCRIPT_DIR"

# Run the Python script
python3 pych_config.py

# Deactivate the virtual environment
deactivate