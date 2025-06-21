import email
from email import policy
import re

def parse_email_headers(file_path):
    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    
    headers = {
        "From": msg["From"],
        "Return-Path": msg["Return-Path"],
        "Reply-To": msg["Reply-To"],
        "Received": msg.get_all("Received"),
        "Subject": msg["Subject"],
        "Body": get_body(msg)
    }
    return headers

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                return part.get_payload(decode=True).decode(errors='ignore')
    else:
        return msg.get_payload(decode=True).decode(errors='ignore')
    return ""

def extract_body_links(body):
    return re.findall(r'(https?://\S+)', body)
