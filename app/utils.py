import dns.resolver
import dkim
import socket
import whois
import requests
from datetime import datetime
from langdetect import detect

# ====================== SPF CHECK =========================
def check_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            if any("v=spf1" in txt_str for txt_str in rdata.strings):
                return True
        return False
    except:
        return False

# ====================== DKIM CHECK (simplified) =========================
def check_dkim(headers):
    try:
        # You can expand to actually validate signature, for now check presence
        return 'DKIM-Signature' in headers
    except:
        return False

# ====================== DMARC CHECK =========================
def check_dmarc(domain):
    try:
        dmarc_domain = "_dmarc." + domain
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        for rdata in answers:
            if any("v=DMARC1" in txt_str for txt_str in rdata.strings):
                return True
        return False
    except:
        return False

# ====================== WHOIS Domain Age =========================
def check_domain_age(domain):
    try:
        data = whois.whois(domain)
        creation_date = data.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        today = datetime.utcnow()
        age = (today - creation_date).days
        return age
    except:
        return None

# ====================== AbuseIPDB Lookup =========================
def extract_sender_ip(received_headers):
    for header in received_headers:
        if "from" in header.lower():
            words = header.split()
            for word in words:
                if word.startswith("[") and word.endswith("]"):
                    return word.strip("[]")
    return None

def check_abuseip(received_headers):
    api_key = "767aef933f0bb87c75592177254a8b97ae86333d663112ac53204b9bf8e056005bae1dc710cd1b0b"
    ip = extract_sender_ip(received_headers)
    if not ip:
        return False

    url = f"https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": "30"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()["data"]
        if data["abuseConfidenceScore"] > 50:
            return True
        return False
    except:
        return False

# ====================== Phishing Content Scan =========================
phishing_keywords = ["urgent", "reset", "verify", "click here", "suspended", "account", "security", "confirm", "payment", "login", "bank"]

def scan_phishing_words(body):
    score = 0
    found_keywords = []

    for word in phishing_keywords:
        if word.lower() in body.lower():
            score += 10
            found_keywords.append(word)
    
    try:
        lang = detect(body)
        if lang != 'en':
            score += 10
            found_keywords.append(f"Language: {lang}")
    except:
        pass

    return score, found_keywords
