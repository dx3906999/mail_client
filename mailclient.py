# This Python file uses the following encoding: utf-8
import sys
from datetime import datetime
from smtplib import SMTPAuthenticationError
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QAbstractItemView, QProgressDialog
from PySide2.QtCore import QCoreApplication, Qt, QThread
from PySide2.QtGui import QFont, QFontMetrics, QCursor
from ui_mailclient import Ui_MainWindows
from mailsession import MailSession
from mailstorage import MailStorage
from mailsync import MailSync
from mailinfoframe import MailInfoFrame
from maildetail import MailDetailFrame


class MailClient(QWidget):
    def __init__(self):
        super().__init__()
        self.mail_session = None
        self.mail_storage = None
        self.mail_sync = None
        self.sync_thread = None
        self.inbox_mail_frames = []
        self.sentbox_mail_frames = []
        self.ui = Ui_MainWindows()
        self.ui.setupUi(self)
        
        self.init_ui()

    def init_ui(self):

        self.ui.logInOutPushButton.clicked.connect(self.on_logInOutPushButton_clicked)
        self.ui.inboxPushButton.clicked.connect(self.on_inboxPushButton_clicked)
        self.ui.sentboxPushButton.clicked.connect(self.on_sentboxPushButton_clicked)
        
        # 连接标签页关闭信号
        self.ui.mailsTabWidget.tabCloseRequested.connect(self.on_tab_close_requested)

        self.ui.inboxListWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.inboxListWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.inboxListWidget.setSpacing(4)
        self.ui.sentboxListWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.sentboxListWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.sentboxListWidget.setSpacing(4)
        
        # 加载上次登录的用户信息
        self.load_last_login_info()

        # 演示数据：创建并添加到收件箱 QListWidget
        for i in range(10):
            frame = MailInfoFrame(
                email_id=i,
                mail_name="测试邮件发件人",
                mail_subject="这是一个测试邮件的主题，用于测试邮件客户端的显示效果",
                mail_date="2024-10-01",
                is_read=False
            )
            self.inbox_mail_frames.append(frame)
            frame.clicked.connect(lambda eid=i: self.on_mailInfoFrame_clicked(eid))
            item = QListWidgetItem(self.ui.inboxListWidget)
            item.setSizeHint(frame.sizeHint())
            self.ui.inboxListWidget.addItem(item)
            self.ui.inboxListWidget.setItemWidget(item, frame)

    def load_emails(self, folder: str = 'INBOX', list_widget=None, frames_list=None):
        """
        从数据库加载邮件到列表中
        
        参数：
            folder: 文件夹名称（'INBOX' 或 'SENTBOX'）
            list_widget: 要填充的 QListWidget
            frames_list: 要填充的框架列表
        """
        if not self.mail_storage or not self.mail_session:
            return
        
        # 清空现有数据
        if list_widget:
            list_widget.clear()
        if frames_list is not None:
            frames_list.clear()
        
        # 从数据库查询邮件，最新的在前
        emails = self.mail_storage.get_emails_sorted_by_date(
            account_id=self.mail_session.account_id,
            folder=folder,
            limit=100
        )
        
        for email_row in emails:
            email_id, subject, sender, sender_address, date, read, received_date = email_row
            
            frame = MailInfoFrame(
                email_id=email_id,
                mail_name=sender or sender_address or "未知发件人",
                mail_subject=subject or "(无主题)",
                mail_date=datetime.fromtimestamp(date).strftime("%Y-%m-%d"),
                is_read=bool(read)
            )
            
            if frames_list is not None:
                frames_list.append(frame)
            
            frame.clicked.connect(lambda eid=email_id: self.on_mailInfoFrame_clicked(eid))
            
            if list_widget:
                item = QListWidgetItem(list_widget)
                item.setSizeHint(frame.sizeHint())
                list_widget.addItem(item)
                list_widget.setItemWidget(item, frame)
    
    def load_last_login_info(self):
        """从数据库加载上次登录的用户信息到UI"""
        temp_storage = MailStorage("mailclient.db")
        last_login = temp_storage.get_last_login_account()
        temp_storage.close()
        
        if last_login:
            self.ui.usermailLineEdit.setText(last_login['email'])
            self.ui.usernameLineEdit.setText(last_login['username'])
            self.ui.smtpServerLineEdit.setText(last_login['smtp_server'])
            self.ui.smtpPortLineEdit.setText(str(last_login['smtp_port']))
            self.ui.isSmtpsslCheckBox.setChecked(last_login['smtp_ssl'])
            self.ui.pop3ServerLineEdit.setText(last_login['pop3_server'])
            self.ui.pop3PortLineEdit.setText(str(last_login['pop3_port']))
            self.ui.isPop3sslCheckBox.setChecked(last_login['pop3_ssl'])
    
    def clear_mail_lists(self):
        """清空所有邮件列表和框架"""
        self.ui.inboxListWidget.clear()
        self.ui.sentboxListWidget.clear()
        self.inbox_mail_frames.clear()
        self.sentbox_mail_frames.clear()




    def on_logInOutPushButton_clicked(self):
        if self.ui.logInOutPushButton.text() == "登录":
            username = self.ui.usernameLineEdit.text()
            password = self.ui.passwordLineEdit.text()
            user_mail = self.ui.usermailLineEdit.text()
            smtp_server = self.ui.smtpServerLineEdit.text()
            smtp_port_str = self.ui.smtpPortLineEdit.text()
            smtp_is_ssl = self.ui.isSmtpsslCheckBox.isChecked()
            pop3_server = self.ui.pop3ServerLineEdit.text()
            pop3_port_str = self.ui.pop3PortLineEdit.text()
            pop3_is_ssl = self.ui.isPop3sslCheckBox.isChecked()

            if not all([username, password, user_mail, smtp_server, smtp_port_str, pop3_server, pop3_port_str]):
                QMessageBox.warning(self, "提示", "请填写完整的登录信息！")
                return

            try:
                smtp_port = int(smtp_port_str)
                pop3_port = int(pop3_port_str)
            except ValueError:
                QMessageBox.warning(self, "提示", "端口号必须是整数！")
                return
            
            self.mail_session = MailSession(
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                smtp_is_ssl=smtp_is_ssl,
                pop3_server=pop3_server,
                pop3_port=pop3_port,
                pop3_is_ssl=pop3_is_ssl,
                user_mail=user_mail,
                username=username,
                password=password
            )

            try:
                self.mail_session.connect_smtp(timeout=10)
                self.mail_session.connect_pop3(timeout=10)
            except SMTPAuthenticationError:
                QMessageBox.critical(self, "错误", "SMTP认证失败，请检查用户名和密码！")
                return
            except TimeoutError:
                QMessageBox.critical(self, "错误", "连接超时，请检查网络连接或服务器地址！")
                return
            except Exception as e:
                QMessageBox.critical(self, "错误", f"连接邮件服务器失败：{str(e)}")
                return
            
            self.ui.usermailLineEdit.setEnabled(False)
            self.ui.usernameLineEdit.setEnabled(False)
            self.ui.passwordLineEdit.setEnabled(False)
            self.ui.smtpServerLineEdit.setEnabled(False)
            self.ui.smtpPortLineEdit.setEnabled(False)
            self.ui.isSmtpsslCheckBox.setEnabled(False)
            self.ui.pop3ServerLineEdit.setEnabled(False)
            self.ui.pop3PortLineEdit.setEnabled(False)
            self.ui.isPop3sslCheckBox.setEnabled(False)

            self.ui.logInOutPushButton.setEnabled(False)

            self.mail_storage = MailStorage("mailclient.db")
            self.mail_session.storage = self.mail_storage
            self.mail_session.account_id = self.mail_storage.get_account_id(user_mail)
            if not self.mail_session.account_id:
                self.mail_session.account_id = self.mail_storage.add_account(
                    email=user_mail,
                    username=username,
                    smtp_server=smtp_server,
                    smtp_port=smtp_port,
                    smtp_ssl=smtp_is_ssl,
                    pop3_server=pop3_server,
                    pop3_port=pop3_port,
                    pop3_ssl=pop3_is_ssl
                )
            
            # 更新上次登录时间
            self.mail_storage.update_last_login(self.mail_session.account_id)
            
            self.mail_sync = MailSync(self.mail_session, self.mail_storage, self.mail_session.account_id)
            
            # 从数据库加载已有的邮件
            # self.load_emails('INBOX', self.ui.inboxListWidget, self.inbox_mail_frames)
            self.load_emails('SENTBOX', self.ui.sentboxListWidget, self.sentbox_mail_frames)
            
            # 启动同步并显示进度条
            self.start_sync()
            
            self.ui.logInOutPushButton.setEnabled(True)
            self.ui.logInOutPushButton.setText("登出")
        else:

            reply = QMessageBox.question(self, "提示", "确定要登出吗？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return

            self.mail_session.close_smtp_connections()
            self.mail_session.close_pop3_connections()
            self.mail_session = None
            self.mail_storage.close()
            self.mail_storage = None
            self.mail_sync = None

            # 清空邮件列表
            self.clear_mail_lists()

            # TODO：取消tab页中的邮件显示
            self.ui.mailsTabWidget.clear()

            self.ui.usermailLineEdit.setEnabled(True)
            self.ui.usernameLineEdit.setEnabled(True)
            self.ui.passwordLineEdit.setEnabled(True)
            self.ui.smtpServerLineEdit.setEnabled(True)
            self.ui.smtpPortLineEdit.setEnabled(True)
            self.ui.isSmtpsslCheckBox.setEnabled(True)
            self.ui.pop3ServerLineEdit.setEnabled(True)
            self.ui.pop3PortLineEdit.setEnabled(True)
            self.ui.isPop3sslCheckBox.setEnabled(True)

            self.ui.logInOutPushButton.setText("登录")

    def on_inboxPushButton_clicked(self):
        self.ui.mailBoxStackedWidget.setCurrentIndex(0)

    def on_sentboxPushButton_clicked(self):
        self.ui.mailBoxStackedWidget.setCurrentIndex(1)

    def on_mailInfoFrame_clicked(self, email_id: int):
        """点击邮件列表项时，在 tab 中打开邮件详情"""
        if not self.mail_storage:
            return
        
        # 检查邮件是否已在某个 tab 中打开
        for i in range(self.ui.mailsTabWidget.count()):
            tab_widget = self.ui.mailsTabWidget.widget(i)
            if isinstance(tab_widget, MailDetailFrame) and tab_widget.email_id == email_id:
                # 邮件已打开，切换到该 tab
                self.ui.mailsTabWidget.setCurrentIndex(i)
                return
        
        # 从数据库获取邮件详情
        email_detail = self.mail_storage.get_email_detail(email_id)
        if not email_detail:
            QMessageBox.warning(self, "提示", "无法获取邮件详情")
            return
        
        (email_db_id, subject, sender, sender_address, receivers_address, 
         cc_address, date, body_text, body_html, read, flagged, has_attachment, received_date) = email_detail
        
        # 创建邮件详情框架
        detail_frame = MailDetailFrame(
            account_id=self.mail_session.account_id,
            email_id=email_id,
            sender=f'{sender} <{sender_address}>' if sender_address else sender or "未知发件人",
            recipient=receivers_address or "",
            subject=subject or "(无主题)",
            mail_content=body_html if body_html else body_text,
            is_html=bool(body_html),
            has_attachments=bool(has_attachment)
        )
        
        # tab 标题：超过15个字符则省略
        tab_title = subject or "(无主题)"
        if len(tab_title) > 15:
            font_metrics = QFontMetrics(self.ui.mailsTabWidget.font())
            tab_title = font_metrics.elidedText(tab_title, Qt.ElideRight, 100)
        
        # 添加到 tab widget
        tab_index = self.ui.mailsTabWidget.addTab(detail_frame, tab_title)
        
        # 切换到新 tab
        self.ui.mailsTabWidget.setCurrentIndex(tab_index)

        self.mail_storage.mark_email_as_read(email_id, True)
    
    def on_tab_close_requested(self, index: int):
        self.ui.mailsTabWidget.removeTab(index)
    
    def start_sync(self):
        if not self.mail_sync:
            return
        
        # 创建进度对话框
        self.progress_dialog = QProgressDialog("准备同步邮件...", "取消", 0, 100, self)
        self.progress_dialog.setWindowTitle("同步邮件")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        
        # 创建线程
        self.sync_thread = QThread()
        self.mail_sync.moveToThread(self.sync_thread)
        
        self.sync_thread.started.connect(self.mail_sync.sync_once)
        self.mail_sync.progress_updated.connect(self.on_sync_progress)
        self.mail_sync.sync_finished.connect(self.on_sync_finished)
        self.mail_sync.sync_error.connect(self.on_sync_error)
        self.mail_sync.sync_canceled.connect(self.on_sync_canceled)
        self.progress_dialog.canceled.connect(self.mail_sync.request_cancel)
        
        self.sync_thread.start()
    
    def on_sync_progress(self, current: int, total: int, message: str):
        if self.progress_dialog:
            self.progress_dialog.setMaximum(total)
            self.progress_dialog.setValue(current)
            font_metrics = QFontMetrics(self.progress_dialog.font())
            elided_message = font_metrics.elidedText(message, Qt.ElideRight, 300)
            self.progress_dialog.setLabelText(elided_message)
    
    def on_sync_finished(self, synced_count: int):
        if self.sync_thread:
            self.sync_thread.quit()
            self.sync_thread.wait()
            self.sync_thread = None
        
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
        
        # 同步完成后刷新邮件列表
        self.load_emails('INBOX', self.ui.inboxListWidget, self.inbox_mail_frames)
        
        if synced_count > 0:
            QMessageBox.information(self, "同步完成", f"成功同步 {synced_count} 封新邮件！")
        else:
            QMessageBox.information(self, "同步完成", "没有新邮件")
    
    def on_sync_error(self, error_msg: str):
        if self.sync_thread:
            self.sync_thread.quit()
            self.sync_thread.wait()
            self.sync_thread = None
        
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
        
        QMessageBox.critical(self, "同步失败", error_msg)
    
    def on_sync_canceled(self):
        # 工作线程已确认取消
        if self.sync_thread:
            self.sync_thread.quit()
            self.sync_thread.wait()
            self.sync_thread = None
        
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
        
        QMessageBox.information(self, "已取消", "邮件同步已取消")

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    window = MailClient()
    window.show()
    sys.exit(app.exec_())
