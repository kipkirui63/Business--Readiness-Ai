from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf(assessment, scores, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, f"AI Readiness Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 80, f"Organization ID: {assessment.organization_id}")
    c.drawString(100, height - 100, f"User: {assessment.user.full_name}")
    c.drawString(100, height - 120, f"Date: {assessment.date_submitted.strftime('%Y-%m-%d')}")

    y = height - 160
    c.drawString(100, y, "Scores:")
    for key, value in scores.items():
        y -= 20
        c.drawString(120, y, f"{key.capitalize()} Score: {value}")

    y -= 30
    c.drawString(100, y, "Recommendation:")
    y -= 20
    c.drawString(120, y, assessment.recommendation)

    c.save()
    return output_path
