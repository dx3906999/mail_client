from email import message_from_string
from email.header import decode_header
from PySide6.QtCore import QObject, Signal
from mailsession import MailSession
from mailstorage import MailStorage


class MailSync(QObject):
    sync_finished = Signal(int)
    sync_error = Signal(str)
    progress_updated = Signal(int, int, str)
    sync_canceled = Signal()
    
    def __init__(self, session: MailSession, storage: MailStorage, account_id: int):
        super().__init__()
        self.session = session
        self.storage = storage
        self.account_id = account_id
        self._cancel_requested = False
    
    def parse_email_body(self, raw_email: str):
        msg = message_from_string(raw_email)
        
        body_text = ''
        body_html = ''
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = part.get_content_disposition()
                
                # 跳过附件
                if content_disposition in ['attachment', 'inline']:
                    continue
                
                try:
                    payload = part.get_payload(decode=True)
                    if not payload:
                        continue
                    
                    charset = part.get_content_charset() or 'utf-8'
                    text = payload.decode(charset, errors='ignore')
                    
                    if content_type == 'text/plain':
                        body_text += text
                    elif content_type == 'text/html':
                        body_html += text
                except Exception as e:
                    continue
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or 'utf-8'
                    text = payload.decode(charset, errors='ignore')
                    
                    if msg.get_content_type() == 'text/html':
                        body_html = text
                    else:
                        body_text = text
            except Exception as e:
                pass
        
        return body_text, body_html
    
    def extract_attachments(self, raw_email: str):
        """
        从邮件中提取所有附件
        返回：[(filename, content, content_type, content_id), ...]
        """
        msg = message_from_string(raw_email)
        attachments = []
        
        for part in msg.walk():
            content_disposition = part.get_content_disposition()

            if content_disposition in ['attachment', 'inline']:
                filename = part.get_filename()
                if filename:
                    decoded_parts = decode_header(filename)
                    filename_parts = []
                    for content, charset in decoded_parts:
                        if isinstance(content, bytes):
                            charset = charset or 'utf-8'
                            filename_parts.append(content.decode(charset, errors='ignore'))
                        else:
                            filename_parts.append(content)
                    filename = ''.join(filename_parts)
                else:
                    ext = part.get_content_subtype()
                    filename = f"attachment_{len(attachments) + 1}.{ext}"
                
                content = part.get_payload(decode=True)
                if content:
                    content_type = part.get_content_type()
                    content_id = part.get('Content-ID', '').strip('<>')
                    
                    attachments.append((filename, content, content_type, content_id))
        
        return attachments
    
    def sync_once(self):
        try:
            self._cancel_requested = False
            headers = self.session.fetch_email_header()
            total = len(headers)
            self.progress_updated.emit(0, total, "开始同步...")
            
            synced_count = 0
            
            for idx, header in enumerate(headers):
                if self._cancel_requested:
                    self.sync_canceled.emit()
                    return
                message_id = header.get('Message-ID')
                
                if not message_id:
                    continue
                
                if self.storage.email_exists(self.account_id, message_id):
                    continue
                
                raw_email = self.session.fetch_email(idx)
                if not raw_email:
                    # 若拉取失败则跳过该邮件
                    continue

                parse_result = self.parse_email_body(raw_email)
                body_text, body_html = parse_result if parse_result else ('', '')

                attachments = self.extract_attachments(raw_email) or []
                has_attachment = len(attachments) > 0
                
                receivers_addresses = header.get('To-Addresses', [])
                receivers_address_str = ', '.join(receivers_addresses) if receivers_addresses else ''
                cc_addresses = header.get('Cc-Addresses', [])
                cc_address_str = ', '.join(cc_addresses) if cc_addresses else ''

                email_id = self.storage.save_full_email(
                    account_id=self.account_id,
                    message_id=message_id,
                    folder='INBOX',
                    subject=header.get('Subject', ''),
                    sender=header.get('From-Name', ''),
                    sender_address=header.get('From-Address', ''),
                    receivers_address=receivers_address_str,
                    cc_address=cc_address_str,
                    date=header.get('Date', ''),
                    body_text=body_text,
                    body_html=body_html,
                    has_attachment=has_attachment
                )
                
                for attachment in attachments:
                    if not attachment or len(attachment) != 4:
                        continue
                    filename, content, content_type, content_id = attachment
                    self.storage.save_attachment(
                        email_id=email_id,
                        account_id=self.account_id,
                        filename=filename,
                        content=content,
                        content_type=content_type,
                        content_id=content_id
                    )
                
                synced_count += 1
                subject = header.get('Subject', '(无主题)')
                # print(f"✓ 同步邮件: {subject}")
                self.progress_updated.emit(idx + 1, total, f"已同步: {subject}")
            
            # if synced_count > 0:
            #     print(f"本次同步完成，新增 {synced_count} 封邮件")
            # else:
            #     print("没有新邮件")
            
            self.sync_finished.emit(synced_count)
                
        except Exception as e:
            error_msg = f"同步失败: {str(e)}"
            # print(error_msg)
            self.sync_error.emit(error_msg)
    
    def request_cancel(self):
        """由主线程调用以请求取消同步"""
        self._cancel_requested = True
    
    