What is MailShield?
MailShield is a multi-layered email spoof detection and analysis tool powered by AI and threat intelligence. It scans raw emails (.eml files), detects forged headers, phishing patterns, spoofing attempts, and even generates real-time alerts and PDF reports. All wrapped in a clean, Bootstrap-powered web UI.

🎯 Features
Module	Description
🔍 Header Analysis	Checks From, Reply-To, Return-Path, and sender IP
🔐 SPF/DKIM/DMARC Validation	Validates email authenticity
🌐 AbuseIPDB Lookup	Flags IPs with bad reputation
📆 Zero-Day Domain Detection	WHOIS-based age check
🧠 Phishing NLP	Scans email content for social engineering keywords
📊 Spoof Score & Verdict	Classifies the email: Safe / Suspicious / Spoofed
📨 Email Alerts (SMTP)	Sends alerts for high spoof scores
📄 PDF Report Generator	Downloadable scan report
💻 Flask Dashboard	Beautiful, judge-friendly web interface

 Tech Stack
Python 3.10

Flask (web app)

ReportLab (PDF generation)

Bootstrap 5 (UI styling)

AbuseIPDB API (IP threat intelligence)

dnspython / dkimpy / pyspf (Email auth checks)

nltk / langdetect (NLP engine)

⚙️ How to Run Locally
bash
Copy
Edit
git clone https://github.com/shashu-hyper1/MailShield-Email-Spoof-Detector.git
cd MailShield-Email-Spoof-Detector

# Create a virtual environment
python -m venv mailshield-env
.\mailshield-env\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
Open your browser and go to:
👉 http://localhost:5000

📂 Upload File Format
Upload .eml email files for analysis. Sample test files included in test_emails/.

📬 Email Alerts Setup
Replace with your Gmail SMTP + App Password in app/alert.py:

python
Copy
Edit
SMTP_EMAIL = "yourname@gmail.com"
SMTP_PASSWORD = "your_app_password"
🧾 Generate PDF Report
After scanning, click “Download PDF Report” to get a nicely formatted report of the spoof detection.

🧑‍💻 Authors
Saishashank – Chennai Institute of Technology

Hackathon: CyberHackathon 2025

Team: CyberSentinels

📄 License
MIT License – free to use, modify, and upgrade.

🙌 Contributions Welcome!
Want to add:

Gmail API support?

Threat scoring AI model?

Browser extension?

Pull requests & forks are open! 👾

