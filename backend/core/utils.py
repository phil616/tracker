
from json import dumps, loads
from base64 import urlsafe_b64decode, urlsafe_b64encode
from uuid import uuid4
from core.setting import config
from lib.api_email import send_email, Email
from lib.hash import hash_util
def encode_url_safe_b64_data(data: dict)->str:
    json_data = dumps(data)
    url_safe_b64_data = urlsafe_b64encode(json_data.encode()).decode()
    return url_safe_b64_data

def decode_url_safe_b64_data(url_safe_b64_data: str)->dict:
    json_data = urlsafe_b64decode(url_safe_b64_data.encode()).decode()
    data = loads(json_data)
    return data

def get_timestamp()->int:
    import time
    return int(time.time())

def get_random_string(length: int)->str:
    return str(uuid4().hex)[:length]

def get_offset_timestamp(offset: int = 60*60*24*7):
    # offset within a week
    return get_timestamp() + offset


async def send_email_confirmation_link(email:str, query_url:str, confirmation_code:str):
    link = f"http://{config.SERVER_HOST}:{config.SERVER_PORT}/{config.API_STR}/regcheck?hashcode={confirmation_code}"
    email_content = f"dear {email}: click the link below to confirm your email address: {link}"
    email_obj = Email(
        host=config.SMTP_HOST,
        port=config.SMTP_PORT,
        username=config.SMTP_USER,
        password=config.SMTP_PASSWORD,
        subject="Confirm your email address",
        from_addr=config.EMAILS_FROM_EMAIL,
        send_to_addr=email,
        contest_msg=email_content,
        attachments=None,
    )
    await send_email(email_obj)

def get_bytes_hash(data: bytes)->str:
    return hash_util.byte_hash(data)