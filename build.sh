#!/bin/bash

UI_DIR="gui/ui_files"

find "$UI_DIR" -type f -name "*.ui" | while read ui_file; do
    py_file="${ui_file%.ui}_ui.py"
    echo "Compiling $ui_file -> $py_file"
    pyside6-uic "$ui_file" -o "$py_file"
done

echo "✔️ All .ui files compiled successfully."

# python gui/editor.py