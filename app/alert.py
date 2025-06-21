import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_EMAIL = "sainano437@gmail.com"
SMTP_PASSWORD = "ovfu kdrs hlre jcob"
TO_EMAIL = "sai21ulta@gmail.com"  

def send_alert_email(report):
    subject = "🚨 MailShield Alert: Spoofing Detected"
    body = f"""Alert triggered by MailShield:

Spoof Score: {report['spoof_score']}%
Flags:
- {', '.join(report['flags'])}

From: {report['headers']['From']}
Return-Path: {report['headers']['Return-Path']}
Subject: {report['headers']['Subject']}

Domain Age: {report['domain_age']} days
Phishing Hints: {', '.join(report['phishing_keywords'])}

Take action immediately.
    """

    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        print("[+] Email alert sent successfully.")
    except Exception as e:
        print(f"[-] Failed to send alert email: {e}")
