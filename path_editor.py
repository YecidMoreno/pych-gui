"""
path_editor.py - Path Editor Module

Author: Yecid Moreno <GitHub @YecidMoreno> <Email yecidmoreno@alumni.usp.br>
Created: 2025-10-15
Description: This module provides a graphical interface for managing paths using PySide6.
"""

from utils.utils_ui import load_ui
from PySide6.QtWidgets import QApplication, QMainWindow, QStyle, QListView, QPushButton, QDialog, QVBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

import json

import qdarktheme

class UIPathEditor:
    def __init__(self, ui_path: str | None = None, initial_paths=None, theme: str = "dark"):
        self.ui_path = ui_path 

        self.app = QApplication.instance() or QApplication(sys.argv)

        try:
            self.app.setStyleSheet(qdarktheme.load_stylesheet("light"))
        except Exception:
            pass

        self.window = None
        if initial_paths is None:
            initial_paths = []
        self.paths = initial_paths
        self.path = None  # Variable to store the currently selected path
        self.load()
        self.update_list_view()

    def exec(self):
        """Displays the window modally (loads it first if not already loaded)."""
        if self.window is None:
            self.load()
        
        if isinstance(self.window, QMainWindow):
            dialog = QDialog()
            layout = QVBoxLayout(dialog)
            layout.addWidget(self.window.centralWidget())
            self.window.setCentralWidget(None)
            dialog.setWindowTitle(self.window.windowTitle())
            dialog.setModal(True)
            res = dialog.exec()
            return self.paths, res
        else:
            # For QDialog or other widgets supporting exec
            return self.paths, self.window.exec()

    def load(self):
        """Loads the .ui file and saves the widget in self.window."""
        widget = load_ui(self.ui_path)
        print(type(widget))

        # If the .ui defines a QMainWindow, use it as is to avoid nesting windows.
        if isinstance(widget, QMainWindow):
            self.window = widget
        else:
            # If the .ui returns another type of widget (QWidget), place it
            # as the central widget inside a QMainWindow.
            main = QMainWindow()
            main.setCentralWidget(widget)
            self.window = main

        # Connect buttons to their respective methods
        self.window.btn_add.clicked.connect(self.add_path)
        self.window.btn_remove.clicked.connect(self.remove_path)
        self.window.btn_up.clicked.connect(self.move_path_up)
        self.window.btn_down.clicked.connect(self.move_path_down)

        model = QStandardItemModel()
        self.window.list_path.setModel(model)

        # Connect the dataChanged signal to handle updates
        model.dataChanged.connect(self.on_data_changed)

        self.window.list_path.selectionModel().currentChanged.connect(self.update_selected_path)

        return self.window

    def show(self):
        """Displays the window (loads it first if not already loaded)."""
        if self.window is None:
            self.load()
        self.window.show()

    def run(self):
        self.show()
        return self.app.exec()

    def add_path(self):
        # Logic to add a path
        new_path = f"New Path {len(self.paths)}"  # Replace with actual input logic
        self.paths.append(new_path)

        # Add the new path directly to the model without clearing existing items
        model = self.window.list_path.model()
        if model is None:
            raise RuntimeError("QListView model is not initialized.")
        model.appendRow(QStandardItem(new_path))

    def remove_path(self):
        # Logic to remove the selected path
        selected_indexes = self.window.list_path.selectedIndexes()
        if selected_indexes:
            index = selected_indexes[0].row()
            self.paths.pop(index)
            self.update_list_view()

    def move_path_up(self):
        # Logic to move the selected path up
        selected_indexes = self.window.list_path.selectedIndexes()
        if selected_indexes:
            index = selected_indexes[0].row()
            if index > 0:
                self.paths[index], self.paths[index - 1] = self.paths[index - 1], self.paths[index]
                self.update_list_view()

    def move_path_down(self):
        # Logic to move the selected path down
        selected_indexes = self.window.list_path.selectedIndexes()
        if selected_indexes:
            index = selected_indexes[0].row()
            if index < len(self.paths) - 1:
                self.paths[index], self.paths[index + 1] = self.paths[index + 1], self.paths[index]
                self.update_list_view()

    def update_list_view(self):
        # Update QListView with current paths
        model = self.window.list_path.model()
        if model is None:
            raise RuntimeError("QListView model is not initialized.")
        model.clear()
        for path in self.paths:
            model.appendRow(QStandardItem(path))
        
        print(self.paths)

    def update_selected_path(self, current, previous):
        """Update self.path with the currently selected path."""
        if current.isValid():
            self.path = current.data()
        else:
            self.path = None
            
    def on_data_changed(self, top_left, bottom_right, roles):
        """Handle changes in the model's data."""
        if roles and Qt.EditRole in roles:
            model = self.window.list_path.model()
            self.paths = [model.item(i).text() for i in range(model.rowCount())]
            print("Updated paths:", self.paths)

if __name__ == "__main__":
    import sys
    editor = UIPathEditor("ui_files/path_editor.ui")
    sys.exit(editor.run())