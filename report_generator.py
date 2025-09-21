import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st

def generate_pdf_bytes(kpis, alerts):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Earthquake + Volcano Risk Report")
    y -= 40

    c.setFont("Helvetica", 12)
    for key, val in kpis.items():
        c.drawString(40, y, f"{key}: {val}")
        y -= 20

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Risk Alerts:")
    y -= 30

    c.setFont("Helvetica", 12)
    for alert in alerts:
        text = f"{alert['quake_place']} → {alert['volcano_name']} ({alert['distance_km']} km)"
        c.drawString(40, y, text)
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer.getvalue()

