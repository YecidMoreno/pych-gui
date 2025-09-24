# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLayout,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QStatusBar, QTreeView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(990, 600)
        MainWindow.setStyleSheet(u"QTreeView {\n"
"    background: #ffffff;\n"
"    color: #202020;\n"
"    alternate-background-color: #f5f5f5;\n"
"    show-decoration-selected: 1;\n"
"    border: 1px solid #cccccc;\n"
"    font-family: Segoe UI, sans-serif;\n"
"    font-size: 13px;\n"
"    selection-background-color: #cce6ff;\n"
"    selection-color: #000;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QTreeView::item {\n"
"    padding: 6px 4px;\n"
"    border: none;\n"
"}\n"
"\n"
"QTreeView::item:hover {\n"
"    background: #eaf3ff;\n"
"    color: #000;\n"
"}\n"
"\n"
"QTreeView::item:selected {\n"
"    background: #cce6ff;\n"
"    color: #000;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #eaeaea;\n"
"    color: #404040;\n"
"    padding: 6px;\n"
"    border: 1px solid #d0d0d0;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QScrollBar:vertical, QScrollBar:horizontal {\n"
"    background: #f0f0f0;\n"
"    border: none;\n"
"    width: 8px;\n"
"    height: 8px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical, QScrollBar::handl"
                        "e:horizontal {\n"
"    background: #bcbcbc;\n"
"    min-height: 20px;\n"
"    min-width: 20px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:hover {\n"
"    background: #a6a6a6;\n"
"}\n"
"\n"
"QScrollBar::add-line, QScrollBar::sub-line {\n"
"    height: 0;\n"
"    width: 0;\n"
"}\n"
"\n"
"QTreeView::branch {\n"
"\n"
"}")
        self.actionLoad_JSON = QAction(MainWindow)
        self.actionLoad_JSON.setObjectName(u"actionLoad_JSON")
        self.actionDebug = QAction(MainWindow)
        self.actionDebug.setObjectName(u"actionDebug")
        self.actionPlugins_Location_so_files = QAction(MainWindow)
        self.actionPlugins_Location_so_files.setObjectName(u"actionPlugins_Location_so_files")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setObjectName(u"treeView")

        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 1)

        self.ly = QGridLayout()
        self.ly.setSpacing(1)
        self.ly.setObjectName(u"ly")
        self.ly.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.gridLayout.addLayout(self.ly, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 990, 30))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuProject = QMenu(self.menubar)
        self.menuProject.setObjectName(u"menuProject")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())
        self.menuFile.addAction(self.actionLoad_JSON)
        self.menuFile.addAction(self.actionSave)
        self.menuView.addAction(self.actionDebug)
        self.menuProject.addAction(self.actionPlugins_Location_so_files)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLoad_JSON.setText(QCoreApplication.translate("MainWindow", u"Load JSON", None))
#if QT_CONFIG(shortcut)
        self.actionLoad_JSON.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionDebug.setText(QCoreApplication.translate("MainWindow", u"Debug", None))
#if QT_CONFIG(shortcut)
        self.actionDebug.setShortcut(QCoreApplication.translate("MainWindow", u"F11", None))
#endif // QT_CONFIG(shortcut)
        self.actionPlugins_Location_so_files.setText(QCoreApplication.translate("MainWindow", u"Plugins Location (.so files)", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuProject.setTitle(QCoreApplication.translate("MainWindow", u"Project", None))
    # retranslateUi

