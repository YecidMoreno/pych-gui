from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog

from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLineEdit, QCheckBox,QTextEdit,
    QPushButton, QSizePolicy, QWidget, QListWidgetItem, QStyleOptionButton, QStyle, QStyledItemDelegate, QMenu)
from PySide6.QtGui import QKeyEvent, QTextOption
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem


import sys, json
import config.values as values
import random

from utils.JsonFile import JsonFile


from widgets.Debug import MyDebugWindow
from widgets.PluginBox import PluginBoxWidget        
from widgets.PathEditor import PathEditorWidget             
from widgets.Block import BlockWidget


from ui_files.main_ui import Ui_MainWindow  
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.isOpen = False
        self.j = None
        self.j_obj = None

        self.debug = MyDebugWindow()
        
        
        self.actionLoad_JSON.triggered.connect(self.on_Load_JSON)
        self.actionSave.triggered.connect(self.on_save_action)
        
        self.actionPlugins_Location_so_files.triggered.connect(self.on_path_editor)

        # Dev and Debug
        def on_debug():
            if not self.debug.isVisible():
                self.update_debug()
                self.debug.show()                
                
            else:
                self.update_debug()
                # self.debug.close()

        
        self.actionDebug.triggered.connect(on_debug)
        self.on_Load_JSON()

        # self.on_path_editor()
        # sys.exit()

    def on_save_action(self):
        if self.j:
            self.j.save_to_file()

    def on_path_editor(self):
        if not self.isOpen: return

        self.pop = PathEditorWidget(_paths=self.j.j["plugins"]["path"])
        self.pop.exec()

    def update_debug(self):
        if self.isOpen:
            self.debug.lb_json.clear()
            self.debug.lb_json.setText( json.dumps(self.j.j,indent=2,default=str) )

    def on_data_changed(self,topLeft, bottomRight, roles):
        print(f"topLeft {topLeft.row()}")
        print(f"bottomRight {bottomRight.row()}")
        for row in range(topLeft.row(), bottomRight.row() + 1):
            name_index = self.model.index(row, 0, topLeft.parent())
            value_index = self.model.index(row, 1, topLeft.parent())

            key = self.model.data(name_index)    
            item = self.model.itemFromIndex(value_index)

            if item.isCheckable():
                value = item.checkState() == Qt.Checked
            else:
                value = item.text()

            print(f"key: {key}")
            print(f"value: {value}")
            

    def make_item(self,name, value):
        item_name = QStandardItem(name)
        item_value = QStandardItem()
    

        item_value.setData(type(value), Qt.UserRole)
        item_value.setData(value, Qt.EditRole)

        item_value.setEditable(True)
        item_name.setEditable(True)
        
        return [item_name, item_value]

    def makeModel(self,j,key = None,parent = None, keys=[]):
        if isinstance(j,dict):
            for k0 in j:
                local_key = keys + [k0]
                created = False
                if isinstance(j[k0],dict):
                    # print(f"{k0} {j[k0]}")
                    p = QStandardItem(k0)
                    p.setData(local_key,values.DATA_KEYS)
                    if parent is None:
                        self.model.appendRow(p)
                        
                    else:
                        parent.appendRow(p) 

                    created = True

                    self.j_obj.setFromKeys(local_key+["#obj"],p,create_if_not_exist=True)          
                    

                else:
                    p = parent        

                self.makeModel(j[k0],k0,p,local_key) 
                
                # if(created):
                #     __items = self.make_item("<insert new>", "{}")
                #     p.appendRow(__items)
                
            return
              
        elif isinstance(j,str) or isinstance(j,bool):
            items = self.make_item(key, j)
            items[0].setData(keys,values.DATA_KEYS)
            parent.appendRow(items)
        elif isinstance(j,list):
            items = self.make_item(key, j)
            items[0].setData(keys,values.DATA_KEYS)
            parent.appendRow(items)

            pass

        
        if("items" in locals()):
            self.j_obj.setFromKeys(keys+["#obj"],items[0],create_if_not_exist=True)
            self.j_obj.setFromKeys(keys+["#value"],items[1],create_if_not_exist=True)
        
        
            

    def update_from_json(self):
        
        if not self.isOpen: return
        
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Nombre","Valor"]) 
        
        self.makeModel(self.j.j)

        self.treeView.setModel(self.model)
        self.treeView.setItemDelegate(ModelDelegate(j=self.j,j_obj=self.j_obj,update_debug=self.update_debug))
        self.treeView.expandAll()
        self.treeView.setColumnWidth(0,200)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)


        def handler(pos):
            index = self.treeView.indexAt(pos)
            if not index.isValid():
                return

            menu = QMenu()
            submenu = menu.addMenu("Add")

            action_int = submenu.addAction("Add int")
            action_bool = submenu.addAction("Add bool")
            action_str = submenu.addAction("Add string")
            action_list = submenu.addAction("Add list")
            
            selected_action = menu.exec(self.treeView.viewport().mapToGlobal(pos))
            
            data = None
            if selected_action == action_int:
                data = 0
            elif selected_action == action_bool:
                data = False
            elif selected_action == action_str:
                data = ""
            elif selected_action == action_list:
                data = []

            if data is not None:
                __items = self.make_item("<insert new>", data)
                keys = index.data(values.DATA_KEYS) + ["<insert new>"]
                __items[0].setData(keys,values.DATA_KEYS)
                print(keys)
                self.j_obj.setFromKeys(keys+["#obj"],__items[0],create_if_not_exist=True)
                self.j_obj.setFromKeys(keys+["#value"],__items[1],create_if_not_exist=True)   
                self.j.setFromKeys(keys,data,create_if_not_exist=True)

                item = self.model.itemFromIndex(index)
                item.appendRow(__items)

        self.treeView.customContextMenuRequested.connect(handler)

        self.treeView.setRootIsDecorated(True)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setAnimated(True)
        self.treeView.setIndentation(20)



    def on_Load_JSON(self):
        if self.isOpen: return

        self.j = JsonFile(values.TEST_FILE)
        self.j_obj = JsonFile()
        
        # self.isOpen = self.j.isValid()
        self.isOpen = True

        if not self.isOpen: return
        
        self.update_debug()
        self.update_from_json()
    
    
    def __del__(self):
        self.debug.close()


    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()
            self.debug.close()

def isColumn(idx,col):
    return idx.column()==col

# print(f"index.miData {col0.data(values.DATA_KEYS)}")


class ModelDelegate(QStyledItemDelegate):

    def sizeHint(self, option, index):
        col0, cur_keys = self.getVariables(index)
        value = index.data()
        if isinstance(value, list):
            lines = len(value)+1
            font_metrics = option.fontMetrics
            height = font_metrics.lineSpacing() * lines + 4
            return QSize(option.rect.width(), height)
        else:
            return super().sizeHint(option, index)
    
    # def displayText(self, value, locale):
    #     if isinstance(value, list):
    #         return '\n'.join(value)
    #     return super().displayText(value, locale)

    def paint(self, painter, option, index):
            value = index.data(Qt.DisplayRole)

            if isinstance(value, list):
                text = '\n'.join(str(v) for v in value)
                painter.save()

                if option.state & QStyle.State_Selected:
                    painter.fillRect(option.rect, option.palette.highlight())

                painter.setPen(option.palette.text().color())
                text_option = QTextOption()
                text_option.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
                painter.drawText(option.rect, text, text_option)

                painter.restore()
            else:
                super().paint(painter, option, index)

    def getValue(self,editor):
        if isinstance(editor, QComboBox):
            return editor.currentText()
        if isinstance(editor, QCheckBox):
            return editor.isChecked()
        if isinstance(editor, QTextEdit):
            return editor.toPlainText().split("\n")
        else:
            return editor.text()
        
    def getVariables(self,index):
        col0 = index.siblingAtColumn(0) 
        cur_keys = col0.data(values.DATA_KEYS)
        return [col0, cur_keys]
    

    def __init__(self, j,j_obj,update_debug, parent=None):
        super().__init__(parent)
        self.j = j
        self.j_obj = j_obj
        self.update_debug = update_debug

    def createEditor(self, parent, option, index):
        """Aqui se crea el editos, inclusive los valores y listas,
        pero no se establece un valor
        combo.setEditable(True)
        combo.addItems(COMBO_OPTIONS[name])"""
        
        col0, cur_keys = self.getVariables(index)
        key_str = JsonFile.keys2str(cur_keys)
        value = index.data(Qt.DisplayRole)

        rule = values.get_matching_rule(key_str);

        ed_type = None

        if not isColumn(index,0):
            if("#value" in rule):
                ed_type = rule["#value"]
            else:
                print(f"Editor not defined: {key_str} >> #value")
                print(f"type(value): {type(value)}")
                ed_type = values.DEFAULT_TYPES[type(value)]
                rule["#value"] = ed_type
        else:
            if("#obj" in rule):
                ed_type = rule["#obj"]
            else:
                print(f"Editor not defined: {key_str} >> #value")
                ed_type = QLineEdit
        
        if ed_type is None:
            return None
        if issubclass(ed_type,QComboBox):
            print("QComboBox")
            ed = ed_type(parent)
            ed.setEditable(True)
            if("#values" in rule):
                if(value not in rule["#values"]):
                    rule["#values"].append(value)
                ed.addItems(rule["#values"])
            return ed
        else:
            return ed_type(parent)
            
            
        

    def setEditorData(self, editor, index):

        col0, cur_keys = self.getVariables(index)
        key_str = JsonFile.keys2str(cur_keys)
        value = index.data(Qt.DisplayRole)

        rule = values.get_matching_rule(key_str);

        name = index.siblingAtColumn(0).data()
        value = index.data(Qt.DisplayRole)

        if isinstance(editor, QComboBox):
            idx = editor.findText(value)
            editor.setCurrentIndex(idx if idx >= 0 else 0)
        if isinstance(editor, QTextEdit):
            editor.setText( "\n".join(index.data()) )
        else:
            if hasattr(editor, "setChecked"):
                editor.setChecked(value)
                pass
            elif hasattr(editor, "setText"):
                editor.setText(str(value))
            else:
                super().setEditorData(editor, index)


    def setModelData(self, editor, model, index):
        
        col0, cur_keys = self.getVariables(index)
        rule = values.get_matching_rule(JsonFile.keys2str(cur_keys))
        print(f"rule: {rule}")

        target_keys = cur_keys.copy()

        cur_val = index.data()
        value = self.getValue(editor)

        if isColumn(index,0):   
                        
            target_keys[-1] = value
            if cur_val != value:

                self.j.move_key(target_keys,cur_keys)
                self.j_obj.move_key(target_keys,cur_keys)
                p=self.j_obj.getFromKeys(target_keys)
                for clave in JsonFile.dfs(p):
                    if "#" in clave[-1]: continue
                    cur_v = self.j_obj.getFromKeys(target_keys + clave)
                    cur_v["#obj"].setData(target_keys + clave,values.DATA_KEYS)

                model.setData(col0,target_keys,values.DATA_KEYS)
                                             
    
    
        if isinstance(editor, QComboBox):
            # add to global variables
            if not ("#values" in rule):
                rule["#values"] = []
            if not cur_val in rule["#values"]:
                rule["#values"].append(value)
        elif isinstance(editor, QTextEdit):
            print(f"value: {value}")

        if "value" in locals():
            model.setData(index, value, Qt.EditRole)
            self.j.setFromKeys(target_keys,value)

        self.update_debug()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()

    # sys.exit(app.exec())
    app.exec()
