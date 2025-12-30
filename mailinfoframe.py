from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor, QFontMetrics, QFont
from PySide6.QtWidgets import QFrame, QApplication
from ui_mailinfoframe import Ui_Frame

class MailInfoFrame(QFrame):
    clicked = Signal()

    def __init__(self, email_id: int, mail_name: str, mail_subject: str, mail_date: str, is_read: bool, parent=None):
        super().__init__(parent)
        self.ui = Ui_Frame()
        self.ui.setupUi(self)
        self.email_id = email_id
        self.is_read = is_read


        self.base_font = QFont(QApplication.font(self))
        self._apply_read_style()
        self.ui.mailDateLabel.setText(mail_date)

        font_metrics = QFontMetrics(self.ui.mailSubjectLabel.font())
        elided_subject = font_metrics.elidedText(mail_subject, Qt.ElideRight, 150)
        self.ui.mailSubjectLabel.setText(elided_subject)
        elided_name = font_metrics.elidedText(mail_name, Qt.ElideRight, 200)
        self.ui.mailNameLabel.setText(elided_name)

        self.setCursor(QCursor(Qt.PointingHandCursor))

    def showEvent(self, event):
        self._apply_read_style()
        super().showEvent(event)

    def _apply_read_style(self):
        font = QFont(self.base_font)
        font.setBold(not self.is_read)
        self.ui.mailSubjectLabel.setFont(font)
        self.ui.mailNameLabel.setFont(font)
        self.ui.mailDateLabel.setFont(font)

    def enterEvent(self, event):
        self.setStyleSheet(
            '''
            QFrame {
                background-color: #F0F7FF;
            }
            '''
        )
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.setStyleSheet("")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            self.is_read = True
            self._apply_read_style()
        super().mousePressEvent(event)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QCoreApplication, Qt
    app = QApplication(sys.argv)
    frame = MailInfoFrame(1,"Alice <alice@example.com>", "Meeting Reminder asasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd", "2024-06-01", False)
    frame.show()
    sys.exit(app.exec_())
