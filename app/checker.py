from .email_parser import parse_email_headers, extract_body_links
from .utils import check_spf, check_dkim, check_dmarc, check_domain_age, check_abuseip, scan_phishing_words

def run_full_analysis(file_path):
    headers = parse_email_headers(file_path)
    from_domain = headers["From"].split("@")[-1].strip()

    spoof_score = 0
    flags = []

    if not check_spf(from_domain):
        spoof_score += 20
        flags.append("SPF Failed")

    if not check_dkim(headers):
        spoof_score += 20
        flags.append("DKIM Failed")

    if not check_dmarc(from_domain):
        spoof_score += 20
        flags.append("DMARC Failed")

    domain_age = check_domain_age(from_domain)
    if domain_age is not None and domain_age < 7:
        spoof_score += 15
        flags.append("New Domain (Zero-Day)")

    abuse_result = check_abuseip(headers["Received"])
    if abuse_result:
        spoof_score += 15
        flags.append("IP Blacklisted (AbuseIPDB)")

    phishing_score, keywords = scan_phishing_words(headers["Body"])
    if phishing_score > 60:
        spoof_score += 10
        flags.append("Phishing Content Detected")

    return {
        "headers": headers,
        "spoof_score": spoof_score,
        "domain_age": domain_age,
        "phishing_keywords": keywords,
        "abuse_ip": abuse_result,
        "flags": flags
    }
