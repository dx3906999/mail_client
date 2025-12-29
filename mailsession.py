import smtplib
import poplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
from email.utils import make_msgid
from mailstorage import MailStorage
from email import message_from_string
from email.utils import parseaddr, getaddresses, parsedate_to_datetime
import datetime,time
from email.header import decode_header

class MailSession:
    def __init__(self, smtp_server:str, smtp_port:int, smtp_is_ssl:bool, pop3_server:str, pop3_port:int, pop3_is_ssl:bool, user_mail:str, username:str, password:str, storage: MailStorage = None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_is_ssl = smtp_is_ssl
        self.pop3_server = pop3_server
        self.pop3_port = pop3_port
        self.pop3_is_ssl = pop3_is_ssl
        self.user_mail = user_mail
        self.username = username
        self.password = password
        self.smtp_connection = None
        self.pop3_connection = None
        self.storage = storage
        self.account_id = None
        if self.storage:
            try:
                self.account_id = self.storage.get_account_id(self.user_mail)
            except Exception:
                self.account_id = None

    def connect_smtp(self, timeout: int = 10):
        try:
            if self.smtp_is_ssl:
                self.smtp_connection = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=timeout)
            else:
                self.smtp_connection = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=timeout)
                self.smtp_connection.starttls()
            self.smtp_connection.login(self.user_mail, self.password)
        except Exception:
            if self.smtp_connection:
                self.smtp_connection.quit()
                self.smtp_connection = None
            raise

    def connect_pop3(self, timeout: int = 10):
        try:
            if self.pop3_is_ssl:
                self.pop3_connection = poplib.POP3_SSL(self.pop3_server, self.pop3_port, timeout=timeout)
            else:
                self.pop3_connection = poplib.POP3(self.pop3_server, self.pop3_port, timeout=timeout)
            self.pop3_connection.user(self.user_mail)
            self.pop3_connection.pass_(self.password)
        except Exception:
            if self.pop3_connection:
                self.pop3_connection.quit()
                self.pop3_connection = None
            raise

    def send_email(self, to_address:list, subject:str, body:str, Cc:list = None, attachments:list = None) -> dict:
        if not self.smtp_connection:
            raise Exception("SMTP connection not established.")
        
        msg = MIMEMultipart('mixed')
        msg['From'] = f'{Header(self.username, "utf-8").encode()} <{self.user_mail}>'
        msg['To'] = ', '.join(to_address)
        msg['Subject'] = Header(subject, 'utf-8').encode()
        if Cc:
            msg['Cc'] = ', '.join(Cc)
        msg['Message-ID'] = make_msgid(idstring=self.username,domain="localhost")
        
        text_part = MIMEText(body, 'plain', 'utf-8')
        msg.attach(text_part)
        
        if attachments:
            for attachment_path in attachments:
                if os.path.exists(attachment_path):
                    self._attach_file(msg, attachment_path)
                else:
                    pass
        
        recipients = list(to_address)
        if Cc:
            recipients += list(Cc)

        send_result = self.smtp_connection.sendmail(self.user_mail, recipients, msg.as_string())

        try:
            if self.storage and self.account_id:
                receivers_address_str = ', '.join(to_address) if to_address else ''
                cc_address_str = ', '.join(Cc) if Cc else ''
                has_attachment = bool(attachments)
                message_id = msg.get('Message-ID', '')
                date_ts = int(time.time())

                email_id = self.storage.save_full_email(
                    account_id=self.account_id,
                    message_id=message_id,
                    folder='SENTBOX',
                    subject=subject,
                    sender=msg.get('From-Name', self.username),
                    sender_address=self.user_mail,
                    receivers_address=receivers_address_str,
                    cc_address=cc_address_str,
                    date=date_ts,
                    body_text=body,
                    body_html='',
                    has_attachment=has_attachment
                )

                if attachments:
                    for attachment_path in attachments:
                        if os.path.exists(attachment_path):
                            try:
                                with open(attachment_path, 'rb') as f:
                                    content = f.read()
                                filename = os.path.basename(attachment_path)
                                self.storage.save_attachment(
                                    email_id=email_id,
                                    account_id=self.account_id,
                                    filename=filename,
                                    content=content,
                                    content_type='application/octet-stream',
                                    content_id=None
                                )
                            except Exception:
                                pass
        except Exception:
            pass

        return send_result
    
    def _attach_file(self, msg:MIMEMultipart, file_path:str):
        try:
            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= "{file_name}"')
            msg.attach(part)
        except Exception as e:
            pass

    def fetch_email_header(self) -> list[dict]:
        if not self.pop3_connection:
            raise Exception("POP3 connection not established.")
        
        email_count, _ = self.pop3_connection.stat()
        headers = []
        for i in range(email_count):
            response, lines, octets = self.pop3_connection.top(i + 1, 0)
            raw_header = b'\n'.join(lines).decode('utf-8')
            header_info = self._parse_email_header(raw_header)
            headers.append(header_info)
        
        return headers
    
    def _parse_email_header(self, raw_header:str) -> dict:
        msg = message_from_string(raw_header)
        sender_name, sender_address = parseaddr(msg.get('From', ''))
        sender_display = self._decode_field(msg.get('From', ''))
        to_list = getaddresses([msg.get('To', '')])
        receivers_addresses = [addr for name, addr in to_list if addr]
        receivers_display = self._decode_field(msg.get('To', ''))
        cc_list = getaddresses([msg.get('Cc', '')])
        cc_addresses = [addr for name, addr in cc_list if addr]
        cc_display = self._decode_field(msg.get('Cc', ''))
        date = parsedate_to_datetime(msg.get('Date', ''))
        struct_time = date.timetuple()
        timestamp = int(time.mktime(struct_time))
        
        header_info = {
            'From': sender_display,
            'From-Name': self._decode_field(sender_name),
            'From-Address': sender_address,
            'To': receivers_display,
            'To-Addresses': receivers_addresses,
            'Cc': cc_display,
            'Cc-Addresses': cc_addresses,
            'Subject': self._decode_field(msg.get('Subject', '')),
            'Date': timestamp,
            'Message-ID': msg.get('Message-ID', '')
        }
        return header_info
    
    def _decode_field(self, value:str) -> str:
        
        if not value:
            return ''
        decoded_parts = decode_header(value)
        result = []
        for content, charset in decoded_parts:
            if isinstance(content, bytes):
                charset = charset or 'utf-8'
                result.append(content.decode(charset, errors='ignore'))
            else:
                result.append(content)
        return ''.join(result)

    def fetch_email(self, index: int):
        if not self.pop3_connection:
            raise Exception("POP3 connection not established.")
        
        email_count, _ = self.pop3_connection.stat()
        if index < 0 or index >= email_count:
            raise IndexError("Email index out of range.")
        
        response, lines, octets = self.pop3_connection.retr(index + 1)
        raw_email = b'\n'.join(lines).decode('utf-8', errors='ignore')
        
        return raw_email

    def close_smtp_connections(self):
        if self.smtp_connection:
            self.smtp_connection.quit()
            self.smtp_connection = None

    def close_pop3_connections(self):
        if self.pop3_connection:
            self.pop3_connection.quit()
            self.pop3_connection = None

