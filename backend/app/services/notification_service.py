import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def send_alert(message: str, contact_info: str):
        """
        Send an alert message.
        For MVP, this simply logs to the console.
        Future: Integrate SendGrid/Twilio.
        """
        logger.info(f"ALERT SENT to {contact_info}: {message}")
        # Placeholder for actual email/SMS logic
        # if contact_info.contains("@"): send_email(...)
        return True
