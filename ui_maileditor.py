# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maileditorAdyRxF.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(544, 556)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.senderLabel = QLabel(Form)
        self.senderLabel.setObjectName(u"senderLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.senderLabel.sizePolicy().hasHeightForWidth())
        self.senderLabel.setSizePolicy(sizePolicy)
        self.senderLabel.setMinimumSize(QSize(0, 19))
        self.senderLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.senderLabel)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.senderLineEdit = QLineEdit(Form)
        self.senderLineEdit.setObjectName(u"senderLineEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.senderLineEdit)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.ccLineEdit = QLineEdit(Form)
        self.ccLineEdit.setObjectName(u"ccLineEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.ccLineEdit)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.subjectLineEdit = QLineEdit(Form)
        self.subjectLineEdit.setObjectName(u"subjectLineEdit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.subjectLineEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.textEdit = QTextEdit(Form)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.addAttachmentsPushButton = QPushButton(Form)
        self.addAttachmentsPushButton.setObjectName(u"addAttachmentsPushButton")

        self.verticalLayout.addWidget(self.addAttachmentsPushButton)

        self.attachmentListWidget = QListWidget(Form)
        self.attachmentListWidget.setObjectName(u"attachmentListWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.attachmentListWidget.sizePolicy().hasHeightForWidth())
        self.attachmentListWidget.setSizePolicy(sizePolicy1)
        self.attachmentListWidget.setMinimumSize(QSize(0, 50))
        self.attachmentListWidget.setMaximumSize(QSize(16777215, 100))
        self.attachmentListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.verticalLayout.addWidget(self.attachmentListWidget)

        self.sendMailPushButton = QPushButton(Form)
        self.sendMailPushButton.setObjectName(u"sendMailPushButton")

        self.verticalLayout.addWidget(self.sendMailPushButton)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u53d1\u4ef6\u4eba", None))
        self.senderLabel.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"\u6536\u4ef6\u4eba", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u6284\u9001", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u4e3b\u9898", None))
        self.addAttachmentsPushButton.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0\u9644\u4ef6", None))
        self.sendMailPushButton.setText(QCoreApplication.translate("Form", u"\u53d1\u9001", None))
    # retranslateUi

