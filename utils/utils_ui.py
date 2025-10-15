import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QStyle
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Qt, QThread, QProcess, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QLineEdit, QFileDialog, QComboBox

def load_ui(path: str):
    ui_file = QFile(path)
    if not ui_file.open(QIODevice.ReadOnly):
        raise FileNotFoundError(f"No se puede abrir el archivo .ui: {path}")
    loader = QUiLoader()
    widget = loader.load(ui_file)
    ui_file.close()
    if widget is None:
        raise RuntimeError(f"No se pudo cargar la interfaz desde: {path}")
    return widget