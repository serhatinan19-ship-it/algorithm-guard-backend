from flask import Flask, request, make_response
from fpdf import FPDF
import datetime
import os

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'ALGORITHM GUARD', ln=1, align='C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'PROTECT YOUR CREATIVE WORK', ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Confidential | Page {self.page_no()} | 2026 Algorithm Guard', align='C')

@app.route('/scan', methods=['POST'])
def handle_scan():
    try:
        data = request.get_json()
        video_link = str(data.get('link', 'N/A'))
        
        pdf = PDF()
        pdf.add_page()
        
        # 1. Ana Başlık
        pdf.set_font('Arial', 'B', 22)
        pdf.set_text_color(33, 37, 41)
        pdf.cell(0, 20, 'AI Scan Report', ln=1, align='C')
        
        # 2. Detaylar
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, 'Scan Details:', ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0)
        pdf.cell(0, 7, f'Date: {datetime.date.today()}', ln=1)
        pdf.cell(0, 7, f'Target: {video_link[:60]}', ln=1)
        pdf.ln(10)
        
        # 3. Özet ve Uyarı (Kutu yerine renkli metin)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(200, 0, 0) # Kırmızı
        pdf.cell(0, 10, 'IMMEDIATE ACTION REQUIRED!', ln=1, align='C')
        
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0)
        msg = ("Our AI detected 3-5 unauthorized re-uploads. To view detailed links, "
               "profiles, and start takedown notices, upgrade to the Full Report.")
        pdf.multi_cell(0, 7, msg, align='C')
        pdf.ln(10)
        
        # 4. Ödeme Linki (Daha güvenli yöntem)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 0, 255) # Mavi
        pdf.cell(0, 10, 'CLICK HERE TO UPGRADE FOR $29', ln=1, align='C', link="https://buy.stripe.com/test")

        # PDF çıktısını al ve encode et
        out = pdf.output(dest='S')
        if isinstance(out, str):
            out = out.encode('latin-1', errors='ignore')
            
        response = make_response(out)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename='AI_Report.pdf')
        return response

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return "Internal Server Error", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
