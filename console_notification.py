# console_notification.py
from notification import Notification


class ConsoleNotification(Notification):
    def notify(self, message: str):
        print(message)
