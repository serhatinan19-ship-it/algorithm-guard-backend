from flask import Flask, request, make_response
from fpdf import FPDF
import datetime
import os

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        # Logo yerine şık bir yazı başlığı (Eğer logon varsa image komutu eklenebilir)
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 51, 102) # Kurumsal Lacivert
        self.cell(0, 10, 'ALGORITHM GUARD', ln=True, align='C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'PROTECT YOUR CREATIVE WORK', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Confidential | Page {self.page_no()} | © {datetime.datetime.now().year} Algorithm Guard', align='C')

@app.route('/scan', methods=['POST'])
def handle_scan():
    data = request.get_json()
    video_link = data.get('link', 'Unknown')
    customer_email = data.get('email', 'N/A')
    
    pdf = PDF()
    pdf.add_page()
    
    # 1. Başlık: AI Scan Report
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 20, 'AI Scan Report', ln=True, align='C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Initial Findings for Digital Copyright Infringement', ln=True, align='C')
    pdf.ln(5)
    
    # 2. Scan Details Bölümü
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Scan Details', ln=True)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0)
    pdf.cell(0, 7, f'• Scan Date: {datetime.datetime.now().strftime("%B %d, %Y")}', ln=True)
    pdf.cell(0, 7, f'• Target Link: {video_link}', ln=True)
    pdf.cell(0, 7, f'• Customer Email: {customer_email}', ln=True)
    pdf.ln(10)
    
    # 3. Executive Summary
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Executive Summary', ln=True)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(33, 37, 41)
    summary_text = ("Our advanced AI algorithms have completed an initial deep scan of major social media platforms, "
                    "identifying potential unauthorized re-uploads and misuse of your video content.")
    pdf.multi_cell(0, 7, summary_text)
    pdf.ln(10)
    
    # 4. Kırmızı Uyarı Kutusu (IMMEDIATE ACTION REQUIRED)
    pdf.set_fill_color(255, 235, 235) # Hafif kırmızı arka plan
    pdf.set_draw_color(255, 0, 0)     # Kırmızı kenarlık
    pdf.set_line_width(0.5)
    pdf.rect(10, pdf.get_y(), 190, 45, 'DF')
    
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 10, 'IMMEDIATE ACTION REQUIRED!', ln=True, align='C')
    
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0)
    warning_text = ("Our AI detected 3-5 unauthorized re-uploads. To view detailed links, infringer profiles, "
                    "and initiate automated takedown notices, please upgrade to the Full Report for $29.")
    pdf.set_x(15)
    pdf.multi_cell(180, 6, warning_text, align='C')
    
    # 5. Upgrade Now Butonu (Linkli)
    pdf.ln(5)
    pdf.set_fill_color(0, 123, 255) # Mavi buton
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 12)
    # Butonun yerini ortalayalım
    button_width = 50
    pdf.set_x((210 - button_width) / 2)
    # ÖDEME LİNKİNİ BURAYA KOY (Örn: Stripe linki)
    payment_url = "https://buy.stripe.com/test_ekleme_yap" 
    pdf.cell(button_width, 12, 'Upgrade Now', ln=True, align='C', fill=True, link=payment_url)

    # Yanıtı oluştur
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='AI_Scan_Report.pdf')
    
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
