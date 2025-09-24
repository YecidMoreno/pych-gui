from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog

from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QListWidgetItem)

from ui_files.plugin_box_ui import Ui_Pluguin_box
class PluginBoxWidget(QWidget, Ui_Pluguin_box):
    def __init__(self,j={},key=None):
        super().__init__()
        self.setupUi(self)  
        self.j = j
        self.key = key

        self.ed_name.setText(key)
        self.ed_path.setText(self.j[self.key])

        self.btn_file.clicked.connect(self.on_btn_file)

        self.ed_path.textChanged.connect(self.on_ed_path)

        self.cb_custom.stateChanged.connect(self.on_cb_changed)
        
        self.ed_name.textChanged.connect(self.on_ed_name)

        self.ed_name.setVisible(False)

        self.btn_del.clicked.connect(self.on_btn_del)

    def on_btn_del(self):
        del self.j[self.key]
        self.setParent(None)
        self.deleteLater()
        pass

    def on_ed_name(self,text):
        del self.j[self.key]
        self.key = text
        self.j[self.key] = self.ed_path.text()
        pass
    
    def on_cb_changed(self):
        if self.cb_custom.isChecked():
            self.cb_name.setVisible(False)
            self.ed_name.setVisible(True)
            pass
        else:
            self.cb_name.setVisible(True)
            self.ed_name.setVisible(False)
            pass

    def on_ed_path(self,text):
        self.ed_path.setToolTip(text)
        if self.key:
            # print(f"self.j: { self.j[self.key]}  text: { text }")
            self.j[self.key] = text
            # self.j[self.key] = text
            pass
            # 


    def on_btn_file(self):
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            caption="Select a .so file",
            dir=".",
            filter="Shared Object Files (*.so);;All Files (*)"
        )
        self.set_file_path(file_path)
        
    def set_file_path(self,file_path):
        if file_path:
            self.ed_path.setText(file_path)