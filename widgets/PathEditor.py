from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog

from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QListWidgetItem)

from  ui_files.w_path_selector_ui import Ui_Path_Selector
class PathEditorWidget(QDialog,Ui_Path_Selector):
    def __init__(self, _paths = None):
        super().__init__()
        self.setupUi(self)
        self._paths = _paths

        self.ed_items = []

        for idx, p in enumerate(self._paths):
            self.add_item(idx,p)

        self.btn_add.clicked.connect(self.on_btn_add_item)
        self.btn_remove.clicked.connect(self.on_btn_remove_item)

    def on_btn_remove_item(self):
        current_row = self.listWidget.currentRow()
        if current_row >= 0 and current_row < len(self._paths):
            self.listWidget.takeItem(current_row)
        
            del self._paths[current_row]

    def on_btn_add_item(self):
        import os
        self._paths.append(os.getcwd())
        self.add_item(len(self._paths)-1,self._paths[-1])
        pass

    def add_item(self,idx,p):
        item = QListWidgetItem()
        ed = QLineEdit()
        ed.setText(p)

        def on_ed_changed(text, index=idx):
            print(f"Updated index {index} with {text}")
            self._paths[index] = text
            print(self._paths)

        ed.textChanged.connect(on_ed_changed)

        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, ed)

        self.ed_items.append(ed)