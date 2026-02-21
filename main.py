from flask import Flask, request, make_response
from fpdf import FPDF
import datetime
import os

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'ALGORITHM GUARD', ln=True, align='C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'PROTECT YOUR CREATIVE WORK', ln=True, align='C')
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
        video_link = str(data.get('link', 'Unknown'))
        customer_email = str(data.get('email', 'N/A'))
        
        pdf = PDF()
        pdf.add_page()
        
        # 1. Başlık
        pdf.set_font('Arial', 'B', 20)
        pdf.set_text_color(33, 37, 41)
        pdf.cell(0, 20, 'AI Scan Report', ln=True, align='C')
        
        # 2. Scan Details
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, 'Scan Details', ln=True)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0)
        pdf.cell(0, 7, f'Date: {datetime.datetime.now().strftime("%Y-%m-%d")}', ln=True)
        pdf.cell(0, 7, f'Link: {video_link[:50]}...', ln=True) # Uzun linkleri keser
        pdf.ln(10)
        
        # 3. Kırmızı Uyarı Kutusu (Basitleştirilmiş)
        pdf.set_fill_color(255, 200, 200)
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(200, 0, 0)
        pdf.cell(0, 10, 'IMMEDIATE ACTION REQUIRED!', ln=1, align='C', fill=True)
        
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0)
        warning_msg = "AI detected 3-5 unauthorized re-uploads. Upgrade to Full Report for $29."
        pdf.multi_cell(0, 10, warning_msg, align='C')
        
        # 4. Buton Alanı
        pdf.ln(10)
        pdf.set_fill_color(0, 123, 255)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 12)
        # Ödeme Linkini buraya ekle
        pdf.cell(60, 12, 'UPGRADE NOW', ln=True, align='C', fill=True, link="https://buy.stripe.com/test")

        response = make_response(pdf.output(dest='S').encode('latin-1', errors='ignore'))
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename='Report.pdf')
        return response
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
