from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog

from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QListWidgetItem)

from ui_files.block_ui import Ui_BlockWidget
class BlockWidget(QWidget, Ui_BlockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  

        