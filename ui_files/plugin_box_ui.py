# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_box.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_Pluguin_box(object):
    def setupUi(self, Pluguin_box):
        if not Pluguin_box.objectName():
            Pluguin_box.setObjectName(u"Pluguin_box")
        Pluguin_box.resize(832, 265)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Pluguin_box.sizePolicy().hasHeightForWidth())
        Pluguin_box.setSizePolicy(sizePolicy)
        Pluguin_box.setStyleSheet(u"#frame{\n"
"background-color: rgb(255, 213, 155);\n"
"border-radius: 10px;\n"
"}\n"
"#btn_del{\n"
"background-color: rgb(170, 0, 0);\n"
"}")
        self.horizontalLayout_2 = QHBoxLayout(Pluguin_box)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Pluguin_box)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_del = QPushButton(self.frame)
        self.btn_del.setObjectName(u"btn_del")
        self.btn_del.setMaximumSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.btn_del)

        self.cb_custom = QCheckBox(self.frame)
        self.cb_custom.setObjectName(u"cb_custom")

        self.horizontalLayout.addWidget(self.cb_custom)

        self.ed_name = QLineEdit(self.frame)
        self.ed_name.setObjectName(u"ed_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ed_name.sizePolicy().hasHeightForWidth())
        self.ed_name.setSizePolicy(sizePolicy2)
        self.ed_name.setMinimumSize(QSize(150, 0))
        self.ed_name.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout.addWidget(self.ed_name)

        self.cb_name = QComboBox(self.frame)
        self.cb_name.setObjectName(u"cb_name")
        self.cb_name.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.cb_name)

        self.ed_path = QLineEdit(self.frame)
        self.ed_path.setObjectName(u"ed_path")

        self.horizontalLayout.addWidget(self.ed_path)

        self.btn_file = QPushButton(self.frame)
        self.btn_file.setObjectName(u"btn_file")
        sizePolicy2.setHeightForWidth(self.btn_file.sizePolicy().hasHeightForWidth())
        self.btn_file.setSizePolicy(sizePolicy2)
        self.btn_file.setMaximumSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.btn_file)


        self.horizontalLayout_2.addWidget(self.frame, 0, Qt.AlignTop)


        self.retranslateUi(Pluguin_box)

        QMetaObject.connectSlotsByName(Pluguin_box)
    # setupUi

    def retranslateUi(self, Pluguin_box):
        Pluguin_box.setWindowTitle(QCoreApplication.translate("Pluguin_box", u"Form", None))
        self.btn_del.setText(QCoreApplication.translate("Pluguin_box", u"X", None))
        self.cb_custom.setText("")
        self.btn_file.setText(QCoreApplication.translate("Pluguin_box", u"O", None))
    # retranslateUi

