#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="pych-gui.sh"
TARGET="/usr/local/bin/pych-gui"

chmod +x "$SCRIPT_DIR/$SCRIPT_NAME"

sudo ln -sf "$SCRIPT_DIR/$SCRIPT_NAME" "$TARGET"

echo "pych-gui installed successfully at $TARGET"

