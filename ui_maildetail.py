# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maildetailhFSUWy.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(525, 427)
        self.verticalLayout_2 = QVBoxLayout(Frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.senderLabel = QLabel(Frame)
        self.senderLabel.setObjectName(u"senderLabel")
        self.senderLabel.setTextFormat(Qt.MarkdownText)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.senderLabel)

        self.label_3 = QLabel(Frame)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.receiverLabel = QLabel(Frame)
        self.receiverLabel.setObjectName(u"receiverLabel")
        self.receiverLabel.setTextFormat(Qt.MarkdownText)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.receiverLabel)

        self.label_5 = QLabel(Frame)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.subjectLabel = QLabel(Frame)
        self.subjectLabel.setObjectName(u"subjectLabel")
        self.subjectLabel.setTextFormat(Qt.MarkdownText)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.subjectLabel)


        self.verticalLayout.addLayout(self.formLayout)

        self.textBrowser = QTextBrowser(Frame)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.attachmentPushButton = QPushButton(Frame)
        self.attachmentPushButton.setObjectName(u"attachmentPushButton")

        self.verticalLayout.addWidget(self.attachmentPushButton)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.label.setText(QCoreApplication.translate("Frame", u"\u53d1\u4ef6\u4eba", None))
        self.senderLabel.setText("")
        self.label_3.setText(QCoreApplication.translate("Frame", u"\u6536\u4ef6\u4eba", None))
        self.receiverLabel.setText("")
        self.label_5.setText(QCoreApplication.translate("Frame", u"\u4e3b\u9898\uff1a", None))
        self.subjectLabel.setText("")
        self.attachmentPushButton.setText(QCoreApplication.translate("Frame", u"\u9644\u4ef6", None))
    # retranslateUi

