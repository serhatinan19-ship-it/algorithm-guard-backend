from flask import Flask, request, make_response
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io
import datetime
import requests

app = Flask(__name__)
CORS(app)

# --- AYARLAR ---
MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/d5r4hdjr4xvs2henqgn3x35hi49gubqv"
SHOPIER_URL = "https://www.shopier.com/31165415"

def create_pdf(email, link):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- TASARIM BAŞLIYOR ---
    # Üst Bölüm (Lacivert)
    p.setFillColor(colors.HexColor("#1a237e"))
    p.rect(0, height - 80, width, 80, fill=1)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "ALGORITHM GUARD - FORENSIC AUDIT")

    # Rapor Detayları
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 120, "AUDIT SUMMARY")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 145, f"Audit ID: AG-{datetime.datetime.now().strftime('%Y%m%d%H%M')}")
    p.drawString(50, height - 160, f"Account: {email}")
    p.drawString(50, height - 175, f"Target: {link}")

    # Çizgi ve Bulgular
    p.setStrokeColor(colors.lightgrey)
    p.line(50, height - 195, 550, height - 195)

    p.setFont("Helvetica-Bold", 13)
    p.setFillColor(colors.red)
    p.drawString(50, height - 225, "CRITICAL FINDINGS:")
    
    p.setFont("Helvetica", 11)
    p.setFillColor(colors.black)
    p.drawString(70, height - 250, "• Unauthorized Duplication: POSITIVE")
    p.drawString(70, height - 270, "• AdSense Hijacking Risk: HIGH")
    p.drawString(70, height - 290, "• Metadata Plagiarism: DETECTED")

    # SHOPIER BUTONU VE ÇERÇEVESİ
    p.setFillColor(colors.HexColor("#f8fafc"))
    p.rect(50, height - 440, 500, 110, fill=1, stroke=1)
    
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(width/2, height - 360, "To initiate legal removal and revenue recovery:")

    # Buton (Mavi)
    p.setFillColor(colors.HexColor("#2563eb"))
    p.roundRect(150, height - 420, 300, 45, 10, fill=1, stroke=0)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 402, "START TAKEDOWN NOW")

    # --- KRİTİK NOKTA: LİNK TANIMLAMA ---
    # (x1, y1, x2, y2) koordinatları butonun üzerine denk getirildi
    p.linkURL(SHOPIER_URL, (150, height - 420, 450, height - 375), relative=0)

    # Footer
    p.setFillColor(colors.grey)
    p.setFont("Helvetica-Oblique", 8)
    p.drawCentredString(width/2, 40, "Algorithm Guard - Digital Intellectual Property Unit")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    user_email = data.get('email')
    video_link = data.get('link')

    if not user_email or not video_link:
        return {"error": "Missing info"}, 400

    # 1. MAKE.COM'A GÖNDER
    try:
        requests.post(MAKE_WEBHOOK_URL, json={
            "email": user_email,
            "link": video_link,
            "date": datetime.datetime.now().isoformat()
        }, timeout=3)
    except:
        pass

    # 2. PDF OLUŞTUR
    pdf_buffer = create_pdf(user_email, video_link)
    
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=Report_{user_email}.pdf'
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
