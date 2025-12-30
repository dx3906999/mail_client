import sqlite3
import os
import time


class MailStorage:
    def __init__(self, db_path:str):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.attachment_root = os.path.join(os.path.dirname(db_path), 'attachments')
        os.makedirs(self.attachment_root, exist_ok=True)
        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT,
                smtp_server TEXT,
                smtp_port INTEGER,
                smtp_ssl INTEGER DEFAULT 1,
                pop3_server TEXT,
                pop3_port INTEGER,
                pop3_ssl INTEGER DEFAULT 1,
                last_login INTEGER DEFAULT 0,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                message_id TEXT UNIQUE,
                folder TEXT DEFAULT 'INBOX',
                subject TEXT,
                sender TEXT,
                sender_address TEXT,
                receivers_address TEXT,
                cc_address TEXT,
                date INTEGER,
                received_date INTEGER DEFAULT (strftime('%s', 'now')),
                read INTEGER DEFAULT 0,
                flagged INTEGER DEFAULT 0,
                has_attachment INTEGER DEFAULT 0,
                body_text TEXT,
                body_html TEXT,
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id INTEGER,
                filename TEXT,
                content_id TEXT,
                content_type TEXT,
                size INTEGER,
                file_path TEXT,
                FOREIGN KEY (email_id) REFERENCES emails (id)
            )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_emails_account_id ON emails (account_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_emails_message_id ON emails (message_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_emails_date ON emails (date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_emails_received_date ON emails (received_date)')
        
        self.connection.commit()
    
    def add_account(self, email:str, username:str, smtp_server:str, smtp_port:int,
                    smtp_ssl:bool, pop3_server:str, pop3_port:int, pop3_ssl:bool) -> int:
        cur = self.connection.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO accounts (email, username, smtp_server, smtp_port, smtp_ssl, pop3_server, pop3_port, pop3_ssl)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (email, username, smtp_server, smtp_port, int(smtp_ssl), pop3_server, pop3_port, int(pop3_ssl)))
        self.connection.commit()
        return cur.lastrowid

    def get_account_id(self, email:str) -> int:
        cur = self.connection.cursor()
        cur.execute("SELECT id FROM accounts WHERE email=?", (email,))
        result = cur.fetchone()
        return result[0] if result else None
    
    def get_last_login_account(self) -> dict:
        """获取上次登录的账户信息
        
        返回格式: {
            'id': account_id,
            'email': email,
            'username': username,
            'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'smtp_ssl': smtp_ssl,
            'pop3_server': pop3_server,
            'pop3_port': pop3_port,
            'pop3_ssl': pop3_ssl
        }
        或 None (无登录历史)
        """
        cur = self.connection.cursor()
        cur.execute("""
            SELECT id, email, username, smtp_server, smtp_port, smtp_ssl, 
                   pop3_server, pop3_port, pop3_ssl
            FROM accounts 
            WHERE last_login > 0
            ORDER BY last_login DESC
            LIMIT 1
        """)
        result = cur.fetchone()
        if result:
            return {
                'id': result[0],
                'email': result[1],
                'username': result[2],
                'smtp_server': result[3],
                'smtp_port': result[4],
                'smtp_ssl': bool(result[5]),
                'pop3_server': result[6],
                'pop3_port': result[7],
                'pop3_ssl': bool(result[8])
            }
        return None
    
    def update_last_login(self, account_id: int):
        """更新账户的上次登录时间"""
        cur = self.connection.cursor()
        cur.execute(
            "UPDATE accounts SET last_login = ? WHERE id = ?",
            (int(time.time()), account_id)
        )
        self.connection.commit()

    def email_exists(self, account_id: int, message_id: str) -> bool:
        cur = self.connection.cursor()
        cur.execute("SELECT 1 FROM emails WHERE account_id=? AND message_id=?", (account_id, message_id))
        return cur.fetchone() is not None

    def close(self):
        self.connection.close()
    
    def save_attachment(self, email_id: int, account_id: int, 
                       filename: str, content: bytes, 
                       content_type: str = 'application/octet-stream',
                       content_id: str = None) -> int:
        """
        保存附件到文件系统，并在数据库记录
        
        返回：attachment_id
        """
        # attachments/account_id/email_id/
        attach_dir = os.path.join(self.attachment_root, str(account_id), str(email_id))
        os.makedirs(attach_dir, exist_ok=True)
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(attach_dir, safe_filename)
        base, ext = os.path.splitext(safe_filename)
        counter = 1
        while os.path.exists(file_path):
            safe_filename = f"{base}_{counter}{ext}"
            file_path = os.path.join(attach_dir, safe_filename)
            counter += 1
        with open(file_path, 'wb') as f:
            f.write(content)
        file_size = len(content)
        relative_path = os.path.join(str(account_id), str(email_id), safe_filename)
        cur = self.connection.cursor()
        cur.execute("""
            INSERT INTO attachments (email_id, filename, content_id, content_type, size, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email_id, safe_filename, content_id, content_type, file_size, relative_path))
        self.connection.commit()
        
        return cur.lastrowid
    
    def get_attachment_path(self, attachment_id: int) -> str:
        cur = self.connection.cursor()
        cur.execute("SELECT file_path FROM attachments WHERE id=?", (attachment_id,))
        result = cur.fetchone()
        if result:
            return os.path.join(self.attachment_root, result[0])
        return None
    
    def get_email_attachments(self, email_id: int) -> list:
        cur = self.connection.cursor()
        cur.execute("""
            SELECT id, filename, content_type, size, file_path
            FROM attachments WHERE email_id=?
        """, (email_id,))
        return cur.fetchall()
    
    def delete_attachment(self, attachment_id: int):
        file_path = self.get_attachment_path(attachment_id)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        cur = self.connection.cursor()
        cur.execute("DELETE FROM attachments WHERE id=?", (attachment_id,))
        self.connection.commit()

    def save_full_email(self, account_id: int, message_id: str, folder: str,
                        subject: str, sender: str, sender_address: str, receivers_address: str, cc_address: str,
                        date: int, body_text: str, body_html: str,
                        has_attachment: bool) -> int:
        cur = self.connection.cursor()
        cur.execute("""
            INSERT INTO emails (account_id, message_id, folder, subject, sender, sender_address, receivers_address, cc_address,
                                date, body_text, body_html, has_attachment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            account_id, message_id, folder, subject, sender, sender_address, receivers_address, cc_address,
            date, body_text, body_html, int(has_attachment)
        ))
        self.connection.commit()
        return cur.lastrowid
    
    def get_emails_by_time_range(self, account_id: int, start_time: int, end_time: int, 
                                  folder: str = 'INBOX', limit: int = None):
        """
        按时间范围查询邮件（Unix时间戳）
        
        参数：
            account_id: 账户ID
            start_time: 开始时间（Unix时间戳，秒数）
            end_time: 结束时间（Unix时间戳，秒数）
            folder: 文件夹名称
            limit: 最多返回多少条，None表示不限制
            
        返回：[(id, subject, sender, sender_address, date, read), ...]
        """
        cur = self.connection.cursor()
        
        if limit:
            cur.execute("""
                SELECT id, subject, sender, sender_address, date, read, received_date
                FROM emails
                WHERE account_id=? AND folder=? AND date BETWEEN ? AND ?
                ORDER BY date DESC
                LIMIT ?
            """, (account_id, folder, start_time, end_time, limit))
        else:
            cur.execute("""
                SELECT id, subject, sender, sender_address, date, read, received_date
                FROM emails
                WHERE account_id=? AND folder=? AND date BETWEEN ? AND ?
                ORDER BY date DESC
            """, (account_id, folder, start_time, end_time))
        
        return cur.fetchall()
    
    def get_emails_sorted_by_date(self, account_id: int, folder: str = 'INBOX', 
                                   limit: int = 50, descending: bool = True):
        """
        按日期排序获取邮件
        
        参数：
            account_id: 账户ID
            folder: 文件夹名称
            limit: 最多返回多少条
            descending: True=最新的优先，False=最旧的优先
            
        返回：[(id, subject, sender, sender_address, date, read, received_date), ...]
        """
        cur = self.connection.cursor()
        
        order = 'DESC' if descending else 'ASC'
        if limit:
            cur.execute(f"""
                SELECT id, subject, sender, sender_address,date, read, received_date
                FROM emails
                WHERE account_id=? AND folder=?
                ORDER BY date {order}
                LIMIT ?
            """, (account_id, folder, limit))
        else:
            cur.execute(f"""
                SELECT id, subject, sender, sender_address, date, read, received_date
                FROM emails
                WHERE account_id=? AND folder=?
                ORDER BY date {order}
            """, (account_id, folder))
        
        return cur.fetchall()
    
    def get_emails_by_folder(self, account_id: int, folder: str = 'INBOX', limit: int = 50):
        """
        按文件夹获取邮件（按接收时间倒序）
        
        参数：
            account_id: 账户ID
            folder: 文件夹名称
            limit: 最多返回多少条
            
        返回：[(id, subject, sender, sender_address, date, read, received_date), ...]
        """
        cur = self.connection.cursor()
        cur.execute("""
            SELECT id, subject, sender, sender_address, date, read, received_date
            FROM emails
            WHERE account_id=? AND folder=?
            ORDER BY received_date DESC
            LIMIT ?
        """, (account_id, folder, limit))
        
        return cur.fetchall()
    
    def get_email_detail(self, email_id: int):
        """
        获取邮件完整信息
        
        返回：(id, subject, sender, sender_address, receivers_address, cc_address, date, 
               body_text, body_html, read, flagged, has_attachment, received_date)
        """
        cur = self.connection.cursor()
        cur.execute("""
            SELECT id, subject, sender, sender_address, receivers_address, cc_address, date,
                   body_text, body_html, read, flagged, has_attachment, received_date
            FROM emails
            WHERE id=?
        """, (email_id,))
        
        return cur.fetchone()
    
    def mark_email_as_read(self, email_id: int, read: bool = True):
        """
        标记邮件为已读/未读
        """
        cur = self.connection.cursor()
        cur.execute("UPDATE emails SET read=? WHERE id=?", (int(read), email_id))
        self.connection.commit()
    
    def mark_email_as_flagged(self, email_id: int, flagged: bool = True):
        """
        标记邮件为标星/取消标星
        """
        cur = self.connection.cursor()
        cur.execute("UPDATE emails SET flagged=? WHERE id=?", (int(flagged), email_id))
        self.connection.commit()
    

if __name__ == "__main__":
    storage = MailStorage("mailclient.db")
    emails = storage.get_emails_sorted_by_date(account_id=1, folder='INBOX', limit=10)
    print(emails)