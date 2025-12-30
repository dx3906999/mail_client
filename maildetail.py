from ui_maildetail import Ui_Frame
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFontMetrics, QDesktopServices
import os


class MailDetailFrame(QFrame):
    def __init__(self, account_id: int, email_id: int, sender: str, recipient: str, subject: str, mail_content: str, is_html: bool = False, has_attachments: bool = False, parent=None):
        super().__init__(parent)
        self.account_id = account_id
        self.email_id = email_id
        self.ui = Ui_Frame()
        self.ui.setupUi(self)
        font_metrics = QFontMetrics(self.ui.senderLabel.font())
        elided_sender = font_metrics.elidedText(sender, Qt.ElideRight, 400)
        self.ui.senderLabel.setText(elided_sender)
        elided_recipient = font_metrics.elidedText(recipient, Qt.ElideRight, 400)
        self.ui.receiverLabel.setText(elided_recipient)
        elided_subject = font_metrics.elidedText(subject, Qt.ElideRight, 400)
        self.ui.subjectLabel.setText(elided_subject)

        if is_html:
            self.ui.textBrowser.setHtml(mail_content)
        else:
            self.ui.textBrowser.setPlainText(mail_content)
        
        if has_attachments:
            self.ui.attachmentPushButton.setEnabled(True)
        else:
            self.ui.attachmentPushButton.setEnabled(False)

        self.ui.attachmentPushButton.clicked.connect(self.on_attachmentPushButton_clicked)

    def on_attachmentPushButton_clicked(self):
        """打开该邮件的附件文件夹"""
        attachment_dir = os.path.join('attachments', str(self.account_id), str(self.email_id))
        
        if not os.path.exists(attachment_dir):
            os.makedirs(attachment_dir, exist_ok=True)
        
        absolute_path = os.path.abspath(attachment_dir)
        QDesktopServices.openUrl(QUrl.fromLocalFile(absolute_path))
        

        

