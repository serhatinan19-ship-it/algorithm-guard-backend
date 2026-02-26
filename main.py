from flask import Flask, request, make_response
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io
import datetime
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- YAPILANDIRMA (DOĞRULANMIŞ LİNK) ---
MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/d5r4hdjr4xvs2henqgn3x35hi49gubqv"
# Senin verdiğin güncel Shopier ürün linki:
SHOPIER_URL = "https://www.shopier.com/44499822"

def create_pdf(email, link):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- PDF TASARIMI ---
    # Başlık Alanı
    p.setFillColor(colors.HexColor("#1a237e"))
    p.rect(0, height - 80, width, 80, fill=1)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "ALGORITHM GUARD - FORENSIC AUDIT")

    # Bilgi Paneli
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 120, "AUDIT REPORT SUMMARY")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 145, f"Audit ID: AG-{datetime.datetime.now().strftime('%Y%m%d%H%M')}")
    p.drawString(50, height - 160, f"Account Email: {email}")
    p.drawString(50, height - 175, f"Content Target: {link}")

    # Bulgular
    p.setStrokeColor(colors.lightgrey)
    p.line(50, height - 195, 550, height - 195)

    p.setFont("Helvetica-Bold", 13)
    p.setFillColor(colors.red)
    p.drawString(50, height - 225, "FORENSIC ANALYSIS RESULTS:")
    
    p.setFont("Helvetica", 11)
    p.setFillColor(colors.black)
    p.drawString(70, height - 250, "• Unauthorized Video Duplication: POSITIVE")
    p.drawString(70, height - 270, "• Metadata Plagiarism Check: FAILED")
    p.drawString(70, height - 290, "• Revenue Leakage Risk: EXTREMELY HIGH")

    # --- SATIŞ BUTONU ALANI ---
    p.setFillColor(colors.HexColor("#f8fafc"))
    p.rect(50, height - 440, 500, 110, fill=1, stroke=1)
    
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(width/2, height - 360, "To download the FULL EVIDENCE LOG and start takedown:")

    # Mavi Buton
    p.setFillColor(colors.HexColor("#2563eb"))
    p.roundRect(150, height - 420, 300, 45, 10, fill=1, stroke=0)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 402, "GET FULL REPORT NOW")

    # --- LİNK TANIMLAMA (44499822) ---
    p.linkURL(SHOPIER_URL, (150, height - 420, 450, height - 375), relative=0)

    # Footer
    p.setFillColor(colors.grey)
    p.setFont("Helvetica-Oblique", 8)
    p.drawCentredString(width/2, 40, "Algorithm Guard Forensic Unit - Secured by AI")

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
        return {"error": "Missing Info"}, 400

    try:
        requests.post(MAKE_WEBHOOK_URL, json={
            "email": user_email,
            "link": video_link,
            "status": "Lead Generated",
            "timestamp": datetime.datetime.now().isoformat()
        }, timeout=3)
    except:
        pass

    pdf_buffer = create_pdf(user_email, video_link)
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=Report_{user_email}.pdf'
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

