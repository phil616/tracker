from pydantic import BaseModel,Field
from typing import List,Literal,Optional

from email.mime.base import MIMEBase

from core.logger import log
import aiosmtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header



class Attachment(BaseModel):
    filename: str = Field(..., description="Attachment filename")
    content: bytes = Field(..., description="Attachment content")


class Email(BaseModel):
    host: str = Field(..., description="SMTP host")
    port: int = Field(..., description="SMTP port")
    username: str = Field(..., description="SMTP username")
    password: str = Field(..., description="SMTP password")
    subject: str = Field(..., description="Email subject")
    send_to_addr: str = Field(..., description="Email send to address")
    from_addr: str = Field(..., description="Email from address")
    contest_msg: str = Field(..., description="Contest message")
    text: Literal['plain', 'html'] = Field('plain', description="Email text format")
    attachments: Optional[List[Attachment]] = Field(None, description="Email attachments")

async def send_email(
        email: Email
):
    
    server = aiosmtplib.SMTP(hostname=email.host, port=email.port, start_tls=True)
    await server.connect()

    await server.login(email.username, email.password)

    msg = MIMEMultipart()
    msg['From'] = email.from_addr  # sender email address
    msg['To'] = email.send_to_addr # target email address
    msg['Subject'] =email.subject  # Subject / title
    # Construct the message body
    msg.attach(MIMEText(email.contest_msg, email.text, 'utf-8'))

    # Attach any attachments
    if email.attachments:
        for attachment in email.attachments:
            filename = attachment.filename
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.content)
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            encoders.encode_base64(part)
            msg.attach(part)

    log.info(f"Sending email to {email.send_to_addr} with subject {email.subject}")
    await server.sendmail(email.from_addr, email.send_to_addr, msg.as_string())
    await server.quit()
