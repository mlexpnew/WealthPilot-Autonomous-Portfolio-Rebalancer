import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


class EmailService:

    def __init__(

        self,

        sender_email: str,

        sender_password: str,

    ):

        self.sender = sender_email

        self.password = sender_password

    def send_report(

        self,

        recipient: str,

        pdf_path: str,

        client_name: str,

    ):

        msg = MIMEMultipart()

        msg["From"] = self.sender

        msg["To"] = recipient

        msg["Subject"] = (
            "WealthPilot AI Portfolio Report"
        )

        body = f"""
Hello {client_name},

Your latest AI Portfolio Report has been generated.

Please find the attached report.

Regards,
WealthPilot AI
"""

        msg.attach(
            MIMEText(
                body,
                "plain",
            )
        )

        with open(pdf_path, "rb") as attachment:

            part = MIMEBase(
                "application",
                "octet-stream",
            )

            part.set_payload(
                attachment.read()
            )

        encoders.encode_base64(part)

        part.add_header(

            "Content-Disposition",

            f'attachment; filename="{pdf_path.split("/")[-1]}"',

        )

        msg.attach(part)

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587,
        )

        server.starttls()

        server.login(
            self.sender,
            self.password,
        )

        server.send_message(msg)

        server.quit()

        return {
            "status": "Email Sent"
        }