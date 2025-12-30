from ui_maileditor import Ui_Form
from PySide6.QtWidgets import QFrame, QFileDialog, QListWidgetItem, QMessageBox
from PySide6.QtCore import Qt, Signal
from mailsession import MailSession
import re
import os

class MailEditorFrame(QFrame):
    send_successful = Signal()

    def __init__(self, mail_session: MailSession, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mail_session = mail_session
        self.attachments = []
        self.ui.textEdit.setAcceptRichText(True)
        # self.ui.textEdit.setFontPointSize(12)
        self.ui.textEdit.setFontFamily("Arial")
        
        # 初始化发件人显示与占位提示
        try:
            sender_text = self.mail_session.user_mail if hasattr(self.mail_session, 'user_mail') else ''
            self.ui.senderLabel.setText(sender_text)
        except Exception:
            self.ui.senderLabel.setText("")
        self.ui.senderLineEdit.setPlaceholderText("多个收件人用逗号分隔，例如 a@example.com, b@example.com")
        self.ui.ccLineEdit.setPlaceholderText("抄送（可选），多个用逗号分隔")
        self.ui.subjectLineEdit.setPlaceholderText("主题")
        
        # 连接附件按钮与列表交互
        self.ui.addAttachmentsPushButton.clicked.connect(self.on_addAttachmentPushButton_clicked)
        self.ui.attachmentListWidget.itemDoubleClicked.connect(self.on_attachment_item_double_clicked)

        # 连接发送按钮（兼容多种按钮命名）
        self.ui.sendMailPushButton.clicked.connect(self.on_send_button_clicked)

    def on_addAttachmentPushButton_clicked(self):
        """选择并添加附件到列表"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择附件",
            "",
            "所有文件 (*);;图片 (*.png *.jpg *.jpeg *.gif);;文档 (*.pdf *.doc *.docx *.xls *.xlsx *.txt)"
        )
        if not files:
            return
        for f in files:
            if not f:
                continue
            abs_path = os.path.abspath(f)
            if abs_path in self.attachments:
                continue
            item = QListWidgetItem(os.path.basename(abs_path))
            item.setToolTip(abs_path)
            item.setData(Qt.UserRole, abs_path)
            self.ui.attachmentListWidget.addItem(item)
            self.attachments.append(abs_path)

    def on_attachment_item_double_clicked(self, item: QListWidgetItem):
        """双击删除附件项"""
        path = item.data(Qt.UserRole)
        if path in self.attachments:
            self.attachments.remove(path)
        row = self.ui.attachmentListWidget.row(item)
        self.ui.attachmentListWidget.takeItem(row)

    def get_compose_data(self):
        """采集编辑器中的邮件数据"""

        def parse_addresses(text: str):
            if not text:
                return []
            parts = [p.strip() for p in re.split(r'[;,]', text) if p.strip()]
            seen = set()
            unique = []
            for p in parts:
                if p not in seen:
                    seen.add(p)
                    unique.append(p)
            return unique
        
        to_list = parse_addresses(self.ui.senderLineEdit.text())
        cc_list = parse_addresses(self.ui.ccLineEdit.text())
        subject = self.ui.subjectLineEdit.text().strip()
        body_text = self.ui.textEdit.toPlainText()
        return to_list, cc_list, subject, body_text, list(self.attachments)

    def send_email(self) -> bool:
        """发送当前编辑的邮件，成功返回True，失败返回False"""
        if not self.mail_session:
            QMessageBox.warning(self, "提示", "未连接邮件会话，无法发送")
            return False
        to_list, cc_list, subject, body_text, attachments = self.get_compose_data()
        if not to_list:
            QMessageBox.warning(self, "提示", "请填写至少一个收件人")
            return False
        if not subject:
            subject = "(无主题)"
        try:
            self.mail_session.send_email(
                to_address=to_list,
                subject=subject,
                body=body_text,
                Cc=cc_list,
                attachments=attachments
            )
            QMessageBox.information(self, "发送成功", "邮件已发送")
            self.attachments.clear()
            self.ui.attachmentListWidget.clear()
            return True
        except Exception as e:
            QMessageBox.critical(self, "发送失败", f"发送邮件失败：{e}")
            return False

    def on_send_button_clicked(self):
        success = self.send_email()
        if success:
            self.send_successful.emit()

        