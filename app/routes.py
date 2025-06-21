from flask import Blueprint, render_template, request, redirect, flash, send_file
import os
from .email_parser import parse_email_headers, extract_body_links
from .checker import run_full_analysis
from .alert import send_alert_email
from .pdf_report import generate_pdf

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    report = None
    if request.method == "POST":
        if 'email_file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['email_file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file:
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)
            
            report = run_full_analysis(file_path)
            
            if report["spoof_score"] > 70:
                send_alert_email(report)
            
            # Generate PDF after analysis
            generate_pdf(report)
                
    return render_template("index.html", report=report)

@main.route("/download-pdf")
def download_pdf():
    if not os.path.exists("report.pdf"):
        return "No report found."
    
    return send_file("report.pdf", as_attachment=True)