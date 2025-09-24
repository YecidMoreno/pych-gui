# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'block.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

class Ui_BlockWidget(object):
    def setupUi(self, BlockWidget):
        if not BlockWidget.objectName():
            BlockWidget.setObjectName(u"BlockWidget")
        BlockWidget.resize(660, 137)
        BlockWidget.setMinimumSize(QSize(0, 100))
        BlockWidget.setMaximumSize(QSize(660, 16777215))
        BlockWidget.setStyleSheet(u"#frame{\n"
"background-color: rgb(255, 245, 220);\n"
"border-radius: 10px;\n"
"}\n"
"#btn_del{\n"
"background-color: rgb(170, 0, 0);\n"
"}")
        self.horizontalLayout_2 = QHBoxLayout(BlockWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame = QFrame(BlockWidget)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_title = QLabel(self.frame)
        self.lbl_title.setObjectName(u"lbl_title")
        font = QFont()
        font.setPointSize(12)
        self.lbl_title.setFont(font)
        self.lbl_title.setScaledContents(False)

        self.verticalLayout.addWidget(self.lbl_title, 0, Qt.AlignTop)

        self.ly = QGridLayout()
        self.ly.setObjectName(u"ly")
        self.ly.setContentsMargins(20, -1, -1, -1)

        self.verticalLayout.addLayout(self.ly)


        self.horizontalLayout_2.addWidget(self.frame)


        self.retranslateUi(BlockWidget)

        QMetaObject.connectSlotsByName(BlockWidget)
    # setupUi

    def retranslateUi(self, BlockWidget):
        BlockWidget.setWindowTitle(QCoreApplication.translate("BlockWidget", u"Form", None))
        self.lbl_title.setText(QCoreApplication.translate("BlockWidget", u"Title", None))
    # retranslateUi

