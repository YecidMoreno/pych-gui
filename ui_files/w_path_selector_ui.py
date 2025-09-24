# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'w_path_selector.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Path_Selector(object):
    def setupUi(self, Path_Selector):
        if not Path_Selector.objectName():
            Path_Selector.setObjectName(u"Path_Selector")
        Path_Selector.resize(519, 391)
        self.horizontalLayout_2 = QHBoxLayout(Path_Selector)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listWidget = QListWidget(Path_Selector)
        self.listWidget.setObjectName(u"listWidget")

        self.horizontalLayout_2.addWidget(self.listWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(6, -1, 6, -1)
        self.btn_remove = QPushButton(Path_Selector)
        self.btn_remove.setObjectName(u"btn_remove")

        self.verticalLayout.addWidget(self.btn_remove, 0, Qt.AlignTop)

        self.btn_add = QPushButton(Path_Selector)
        self.btn_add.setObjectName(u"btn_add")

        self.verticalLayout.addWidget(self.btn_add)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Path_Selector)

        QMetaObject.connectSlotsByName(Path_Selector)
    # setupUi

    def retranslateUi(self, Path_Selector):
        Path_Selector.setWindowTitle(QCoreApplication.translate("Path_Selector", u"Form", None))
        self.btn_remove.setText(QCoreApplication.translate("Path_Selector", u"Remove", None))
        self.btn_add.setText(QCoreApplication.translate("Path_Selector", u"Add", None))
    # retranslateUi

