# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mailclientLliAmX.ui'
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


class Ui_MainWindows(object):
    def setupUi(self, MainWindows):
        if not MainWindows.objectName():
            MainWindows.setObjectName(u"MainWindows")
        MainWindows.resize(1100, 600)
        self.horizontalLayout_2 = QHBoxLayout(MainWindows)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.mainHorizontalLayout = QHBoxLayout()
        self.mainHorizontalLayout.setObjectName(u"mainHorizontalLayout")
        self.leftVerticalLayout = QVBoxLayout()
        self.leftVerticalLayout.setSpacing(0)
        self.leftVerticalLayout.setObjectName(u"leftVerticalLayout")
        self.leftVerticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.userInfoGroupBox = QGroupBox(MainWindows)
        self.userInfoGroupBox.setObjectName(u"userInfoGroupBox")
        self.verticalLayout = QVBoxLayout(self.userInfoGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.userInfoVerticalLayout = QVBoxLayout()
        self.userInfoVerticalLayout.setObjectName(u"userInfoVerticalLayout")
        self.userInfoFormLayout = QFormLayout()
        self.userInfoFormLayout.setObjectName(u"userInfoFormLayout")
        self.userNameLabel = QLabel(self.userInfoGroupBox)
        self.userNameLabel.setObjectName(u"userNameLabel")

        self.userInfoFormLayout.setWidget(0, QFormLayout.LabelRole, self.userNameLabel)

        self.userMailLabel = QLabel(self.userInfoGroupBox)
        self.userMailLabel.setObjectName(u"userMailLabel")

        self.userInfoFormLayout.setWidget(1, QFormLayout.LabelRole, self.userMailLabel)

        self.passwordlabel = QLabel(self.userInfoGroupBox)
        self.passwordlabel.setObjectName(u"passwordlabel")

        self.userInfoFormLayout.setWidget(2, QFormLayout.LabelRole, self.passwordlabel)

        self.label_2 = QLabel(self.userInfoGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.userInfoFormLayout.setWidget(3, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.userInfoGroupBox)
        self.label_3.setObjectName(u"label_3")

        self.userInfoFormLayout.setWidget(4, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(self.userInfoGroupBox)
        self.label_4.setObjectName(u"label_4")

        self.userInfoFormLayout.setWidget(6, QFormLayout.LabelRole, self.label_4)

        self.label = QLabel(self.userInfoGroupBox)
        self.label.setObjectName(u"label")

        self.userInfoFormLayout.setWidget(7, QFormLayout.LabelRole, self.label)

        self.label_5 = QLabel(self.userInfoGroupBox)
        self.label_5.setObjectName(u"label_5")

        self.userInfoFormLayout.setWidget(8, QFormLayout.LabelRole, self.label_5)

        self.label_6 = QLabel(self.userInfoGroupBox)
        self.label_6.setObjectName(u"label_6")

        self.userInfoFormLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.pop3PortLineEdit = QLineEdit(self.userInfoGroupBox)
        self.pop3PortLineEdit.setObjectName(u"pop3PortLineEdit")

        self.userInfoFormLayout.setWidget(7, QFormLayout.FieldRole, self.pop3PortLineEdit)

        self.pop3ServerLineEdit = QLineEdit(self.userInfoGroupBox)
        self.pop3ServerLineEdit.setObjectName(u"pop3ServerLineEdit")

        self.userInfoFormLayout.setWidget(6, QFormLayout.FieldRole, self.pop3ServerLineEdit)

        self.smtpPortLineEdit = QLineEdit(self.userInfoGroupBox)
        self.smtpPortLineEdit.setObjectName(u"smtpPortLineEdit")

        self.userInfoFormLayout.setWidget(4, QFormLayout.FieldRole, self.smtpPortLineEdit)

        self.smtpServerLineEdit = QLineEdit(self.userInfoGroupBox)
        self.smtpServerLineEdit.setObjectName(u"smtpServerLineEdit")

        self.userInfoFormLayout.setWidget(3, QFormLayout.FieldRole, self.smtpServerLineEdit)

        self.passwordLineEdit = QLineEdit(self.userInfoGroupBox)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.userInfoFormLayout.setWidget(2, QFormLayout.FieldRole, self.passwordLineEdit)

        self.usernameLineEdit = QLineEdit(self.userInfoGroupBox)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usernameLineEdit.sizePolicy().hasHeightForWidth())
        self.usernameLineEdit.setSizePolicy(sizePolicy)
        self.usernameLineEdit.setMinimumSize(QSize(0, 0))

        self.userInfoFormLayout.setWidget(0, QFormLayout.FieldRole, self.usernameLineEdit)

        self.usermailLineEdit = QLineEdit(self.userInfoGroupBox)
        self.usermailLineEdit.setObjectName(u"usermailLineEdit")

        self.userInfoFormLayout.setWidget(1, QFormLayout.FieldRole, self.usermailLineEdit)

        self.isSmtpsslCheckBox = QCheckBox(self.userInfoGroupBox)
        self.isSmtpsslCheckBox.setObjectName(u"isSmtpsslCheckBox")

        self.userInfoFormLayout.setWidget(5, QFormLayout.FieldRole, self.isSmtpsslCheckBox)

        self.isPop3sslCheckBox = QCheckBox(self.userInfoGroupBox)
        self.isPop3sslCheckBox.setObjectName(u"isPop3sslCheckBox")

        self.userInfoFormLayout.setWidget(8, QFormLayout.FieldRole, self.isPop3sslCheckBox)


        self.userInfoVerticalLayout.addLayout(self.userInfoFormLayout)

        self.logInOutPushButton = QPushButton(self.userInfoGroupBox)
        self.logInOutPushButton.setObjectName(u"logInOutPushButton")

        self.userInfoVerticalLayout.addWidget(self.logInOutPushButton)


        self.verticalLayout.addLayout(self.userInfoVerticalLayout)


        self.leftVerticalLayout.addWidget(self.userInfoGroupBox)

        self.writeEmailPushButton = QPushButton(MainWindows)
        self.writeEmailPushButton.setObjectName(u"writeEmailPushButton")
        self.writeEmailPushButton.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.writeEmailPushButton.sizePolicy().hasHeightForWidth())
        self.writeEmailPushButton.setSizePolicy(sizePolicy1)
        self.writeEmailPushButton.setMaximumSize(QSize(16777215, 70))

        self.leftVerticalLayout.addWidget(self.writeEmailPushButton)

        self.inboxPushButton = QPushButton(MainWindows)
        self.inboxPushButton.setObjectName(u"inboxPushButton")
        sizePolicy1.setHeightForWidth(self.inboxPushButton.sizePolicy().hasHeightForWidth())
        self.inboxPushButton.setSizePolicy(sizePolicy1)
        self.inboxPushButton.setMaximumSize(QSize(16777215, 70))

        self.leftVerticalLayout.addWidget(self.inboxPushButton)

        self.sentboxPushButton = QPushButton(MainWindows)
        self.sentboxPushButton.setObjectName(u"sentboxPushButton")
        sizePolicy1.setHeightForWidth(self.sentboxPushButton.sizePolicy().hasHeightForWidth())
        self.sentboxPushButton.setSizePolicy(sizePolicy1)
        self.sentboxPushButton.setMaximumSize(QSize(16777215, 70))

        self.leftVerticalLayout.addWidget(self.sentboxPushButton)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.leftVerticalLayout.addItem(self.verticalSpacer)


        self.mainHorizontalLayout.addLayout(self.leftVerticalLayout)

        self.mailBoxStackedWidget = QStackedWidget(MainWindows)
        self.mailBoxStackedWidget.setObjectName(u"mailBoxStackedWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.mailBoxStackedWidget.sizePolicy().hasHeightForWidth())
        self.mailBoxStackedWidget.setSizePolicy(sizePolicy2)
        self.mailBoxStackedWidget.setMinimumSize(QSize(280, 0))
        self.mailBoxStackedWidget.setMaximumSize(QSize(320, 16777215))
        self.mailBoxStackedWidget.setFrameShadow(QFrame.Plain)
        self.inboxPage = QWidget()
        self.inboxPage.setObjectName(u"inboxPage")
        self.verticalLayout_2 = QVBoxLayout(self.inboxPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_7 = QLabel(self.inboxPage)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_2.addWidget(self.label_7)

        self.inboxListWidget = QListWidget(self.inboxPage)
        self.inboxListWidget.setObjectName(u"inboxListWidget")
        self.inboxListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.inboxListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout_2.addWidget(self.inboxListWidget)

        self.mailBoxStackedWidget.addWidget(self.inboxPage)
        self.sentboxPage = QWidget()
        self.sentboxPage.setObjectName(u"sentboxPage")
        self.verticalLayout_3 = QVBoxLayout(self.sentboxPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_8 = QLabel(self.sentboxPage)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_3.addWidget(self.label_8)

        self.sentboxListWidget = QListWidget(self.sentboxPage)
        self.sentboxListWidget.setObjectName(u"sentboxListWidget")
        self.sentboxListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.sentboxListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout_3.addWidget(self.sentboxListWidget)

        self.mailBoxStackedWidget.addWidget(self.sentboxPage)

        self.mainHorizontalLayout.addWidget(self.mailBoxStackedWidget)

        self.mailsTabWidget = QTabWidget(MainWindows)
        self.mailsTabWidget.setObjectName(u"mailsTabWidget")
        self.mailsTabWidget.setMinimumSize(QSize(350, 0))
        self.mailsTabWidget.setTabsClosable(True)
        self.mailsTabWidget.setMovable(True)
        self.mailsTabWidget.setTabBarAutoHide(False)

        self.mainHorizontalLayout.addWidget(self.mailsTabWidget)

        self.mainHorizontalLayout.setStretch(0, 1)
        self.mainHorizontalLayout.setStretch(2, 2)

        self.horizontalLayout_2.addLayout(self.mainHorizontalLayout)

        QWidget.setTabOrder(self.usernameLineEdit, self.usermailLineEdit)
        QWidget.setTabOrder(self.usermailLineEdit, self.passwordLineEdit)
        QWidget.setTabOrder(self.passwordLineEdit, self.smtpServerLineEdit)
        QWidget.setTabOrder(self.smtpServerLineEdit, self.smtpPortLineEdit)
        QWidget.setTabOrder(self.smtpPortLineEdit, self.isSmtpsslCheckBox)
        QWidget.setTabOrder(self.isSmtpsslCheckBox, self.pop3ServerLineEdit)
        QWidget.setTabOrder(self.pop3ServerLineEdit, self.pop3PortLineEdit)
        QWidget.setTabOrder(self.pop3PortLineEdit, self.isPop3sslCheckBox)
        QWidget.setTabOrder(self.isPop3sslCheckBox, self.logInOutPushButton)
        QWidget.setTabOrder(self.logInOutPushButton, self.writeEmailPushButton)
        QWidget.setTabOrder(self.writeEmailPushButton, self.inboxPushButton)
        QWidget.setTabOrder(self.inboxPushButton, self.sentboxPushButton)
        QWidget.setTabOrder(self.sentboxPushButton, self.mailsTabWidget)

        self.retranslateUi(MainWindows)

        self.mailBoxStackedWidget.setCurrentIndex(0)
        self.mailsTabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindows)
    # setupUi

    def retranslateUi(self, MainWindows):
        MainWindows.setWindowTitle(QCoreApplication.translate("MainWindows", u"\u90ae\u4ef6\u5ba2\u6237\u7aef", None))
        self.userInfoGroupBox.setTitle(QCoreApplication.translate("MainWindows", u"\u7528\u6237\u4fe1\u606f", None))
        self.userNameLabel.setText(QCoreApplication.translate("MainWindows", u"\u7528\u6237\u540d", None))
        self.userMailLabel.setText(QCoreApplication.translate("MainWindows", u"\u7528\u6237\u90ae\u7bb1", None))
        self.passwordlabel.setText(QCoreApplication.translate("MainWindows", u"\u5bc6\u7801", None))
        self.label_2.setText(QCoreApplication.translate("MainWindows", u"SMTP\u670d\u52a1\u5668", None))
        self.label_3.setText(QCoreApplication.translate("MainWindows", u"SMTP\u670d\u52a1\u5668\u7aef\u53e3", None))
        self.label_4.setText(QCoreApplication.translate("MainWindows", u"POP3\u670d\u52a1\u5668", None))
        self.label.setText(QCoreApplication.translate("MainWindows", u"POP3\u670d\u52a1\u5668\u7aef\u53e3", None))
        self.label_5.setText(QCoreApplication.translate("MainWindows", u"\u4f20\u5165\u4f7f\u7528SSl", None))
        self.label_6.setText(QCoreApplication.translate("MainWindows", u"\u4f20\u51fa\u4f7f\u7528SSL", None))
        self.isSmtpsslCheckBox.setText("")
        self.isPop3sslCheckBox.setText("")
        self.logInOutPushButton.setText(QCoreApplication.translate("MainWindows", u"\u767b\u5f55", None))
        self.writeEmailPushButton.setText(QCoreApplication.translate("MainWindows", u"\u5199\u4fe1", None))
        self.inboxPushButton.setText(QCoreApplication.translate("MainWindows", u"\u6536\u4fe1\u7bb1", None))
        self.sentboxPushButton.setText(QCoreApplication.translate("MainWindows", u"\u5df2\u53d1\u9001", None))
        self.label_7.setText(QCoreApplication.translate("MainWindows", u"\u6536\u4fe1\u7bb1", None))
        self.label_8.setText(QCoreApplication.translate("MainWindows", u"\u5df2\u53d1\u9001", None))
    # retranslateUi

