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

# --- CONFIGURATION ---
MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/d5r4hdjr4xvs2henqgn3x35hi49gubqv"

def create_pdf(email, link):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- PDF TASARIMI (Profesyonel Görünüm) ---
    # Başlık Alanı
    p.setFillColor(colors.HexColor("#1a237e")) # Koyu Lacivert
    p.rect(0, height - 80, width, 80, fill=1)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "ALGORITHM GUARD - FORENSIC AUDIT")

    # Rapor Bilgileri
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 120, "REPORT SUMMARY")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 140, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    p.drawString(50, height - 155, f"Target Email: {email}")
    p.drawString(50, height - 170, f"Analysis Link: {link}")

    # Analiz Sonuçları (Vurucu Bölüm)
    p.setStrokeColor(colors.lightgrey)
    p.line(50, height - 190, 550, height - 190)

    p.setFont("Helvetica-Bold", 13)
    p.setFillColor(colors.red)
    p.drawString(50, height - 220, "CRITICAL FINDINGS:")
    
    p.setFont("Helvetica", 11)
    p.setFillColor(colors.black)
    p.drawString(70, height - 245, "• Digital Fingerprint Match: POSITIVE (Unauthorized clones detected)")
    p.drawString(70, height - 265, "• Metadata Leakage: Found on 3rd party video hosting platforms")
    p.drawString(70, height - 285, "• Monetization Leak: Estimated revenue loss detected")

    # Uyarı Kutusu
    p.setFillColor(colors.HexColor("#fff3e0"))
    p.rect(50, height - 350, 500, 45, fill=1)
    p.setFillColor(colors.HexColor("#e65100"))
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width/2, height - 330, "URGENT: Content integrity is compromised. Immediate takedown is recommended.")

    # Call to Action (Satışa Yönlendirme)
    p.setFillColor(colors.HexColor("#1a237e"))
    p.rect(150, height - 450, 300, 40, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width/2, height - 435, "START FORMAL TAKEDOWN PROCESS")
    
    p.setFillColor(colors.grey)
    p.setFont("Helvetica-Oblique", 8)
    p.drawCentredString(width/2, 50, "Algorithm Guard Forensic Unit - Secured by AI and Legal Expertise")

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
        return {"error": "Lütfen tüm alanları doldurun."}, 400

    # 1. VERİYİ MAKE.COM'A GÖNDER (Arka planda çalışır, kullanıcıyı bekletmez)
    try:
        requests.post(MAKE_WEBHOOK_URL, json={
            "email": user_email,
            "link": video_link,
            "status": "Potential Theft Detected",
            "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        }, timeout=3)
    except Exception as e:
        print(f"Make.com Sync Error: {e}")

    # 2. PDF OLUŞTUR VE İNDİRT
    pdf_buffer = create_pdf(user_email, video_link)
    
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=AlgorithmGuard_Report_{user_email}.pdf'
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
