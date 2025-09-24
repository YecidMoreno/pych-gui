from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog

from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QListWidgetItem)

from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, QRect


from ui_files.debug_ui import Ui_DebugWindow
class MyDebugWindow(QMainWindow, Ui_DebugWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()
