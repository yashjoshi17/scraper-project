# email_notification.py
import smtplib
from email.mime.text import MIMEText
from notification import Notification


class EmailNotification(Notification):
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, to_email: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.to_email = to_email

    def notify(self, message: str):
        msg = MIMEText(message)
        msg['Subject'] = 'Scraping Status'
        msg['From'] = self.username
        msg['To'] = self.to_email

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, self.to_email, msg.as_string())
