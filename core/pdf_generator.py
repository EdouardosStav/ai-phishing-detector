import time
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

def generate_pdf_report(url, indicators, score, risk_level, gpt_summary, output_path=None):
    if not output_path:
        output_path = os.path.abspath("report.pdf")

    time.sleep(1)  # Ensures file is fully written before sending

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Phishing Risk Analysis Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Paragraph(f"<b>Analyzed URL:</b> {url}", styles['Normal']))
    elements.append(Paragraph(f"<b>Risk Score:</b> {score}/10", styles['Normal']))
    elements.append(Paragraph(f"<b>Risk Level:</b> {risk_level}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Triggered Indicators:</b>", styles['Heading3']))
    for key, value in indicators.items():
        if value:
            text = ", ".join(value) if isinstance(value, list) else key.replace('_', ' ').capitalize()
            elements.append(Paragraph(f"• {text}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>AI-Generated Explanation:</b>", styles['Heading3']))
    elements.append(Paragraph(gpt_summary, styles['Normal']))

    doc.build(elements)
    return output_path


def generate_email_pdf_report(email_snippet, indicators, score, risk_level, gpt_summary, output_path=None):
    if not output_path:
        output_path = os.path.abspath("report_email.pdf")

    time.sleep(1)

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Phishing Risk Analysis Report - Email", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Paragraph(f"<b>Email Snippet:</b> {email_snippet[:100]}{'...' if len(email_snippet) > 100 else ''}", styles['Normal']))
    elements.append(Paragraph(f"<b>Risk Score:</b> {score}/10", styles['Normal']))
    elements.append(Paragraph(f"<b>Risk Level:</b> {risk_level}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Triggered Indicators:</b>", styles['Heading3']))
    for key, value in indicators.items():
        if value:
            text = ", ".join(value) if isinstance(value, list) else key.replace('_', ' ').capitalize()
            elements.append(Paragraph(f"• {text}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>AI-Generated Explanation:</b>", styles['Heading3']))
    elements.append(Paragraph(gpt_summary, styles['Normal']))

    doc.build(elements)
    return output_path