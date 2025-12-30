# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mailinfoframebxDNMi.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(257, 70)
        Frame.setFrameShape(QFrame.Shape.Box)
        Frame.setFrameShadow(QFrame.Shadow.Sunken)
        Frame.setLineWidth(1)
        self.verticalLayout = QVBoxLayout(Frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mailNameLabel = QLabel(Frame)
        self.mailNameLabel.setObjectName(u"mailNameLabel")
        self.mailNameLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.mailNameLabel)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.mailSubjectLabel = QLabel(Frame)
        self.mailSubjectLabel.setObjectName(u"mailSubjectLabel")
        self.mailSubjectLabel.setTextFormat(Qt.TextFormat.MarkdownText)
        self.mailSubjectLabel.setWordWrap(False)
        self.mailSubjectLabel.setOpenExternalLinks(False)

        self.gridLayout.addWidget(self.mailSubjectLabel, 0, 0, 1, 1)

        self.mailDateLabel = QLabel(Frame)
        self.mailDateLabel.setObjectName(u"mailDateLabel")
        self.mailDateLabel.setTextFormat(Qt.TextFormat.MarkdownText)
        self.mailDateLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.mailDateLabel, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.mailNameLabel.setText("")
        self.mailSubjectLabel.setText("")
        self.mailDateLabel.setText("")
    # retranslateUi

