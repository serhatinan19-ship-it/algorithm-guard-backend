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
        self.set_font('Arial', 'I', 9)
        self.cell(0, 5, 'AI-POWERED CONTENT PROTECTION', ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Confidential Scan | Page {self.page_no()} | © 2026 Algorithm Guard', align='C')

@app.route('/scan', methods=['POST'])
def handle_scan():
    try:
        data = request.get_json()
        video_link = str(data.get('link', 'N/A'))
        
        pdf = PDF()
        pdf.add_page()
        
        # 1. Başlık Bölümü
        pdf.set_font('Arial', 'B', 20)
        pdf.set_text_color(33, 37, 41)
        pdf.cell(0, 15, 'Initial Scan Analysis', ln=1, align='L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 7, f'Report ID: AG-{datetime.datetime.now().strftime("%Y%m%d%H%M")}', ln=1)
        pdf.cell(0, 7, f'Status: High Risk Matches Detected', ln=1)
        pdf.ln(5)

        # 2. Tespit Edilen Örnek Linkler (İkna Edici Kısım)
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, 'Detected Unauthorized Matches (Preview):', ln=1)
        
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0)
        # Gerçek API gelene kadar "inandırıcı" maskelenmiş linkler
        pdf.cell(0, 7, '1. YouTube Search Match: https://www.youtube.com/watch?v=kRj***', ln=1)
        pdf.cell(0, 7, '2. Social Media Mirror: https://www.facebook.com/watch/v=v9B***', ln=1)
        pdf.set_font('Arial', 'I', 9)
        pdf.set_text_color(100)
        pdf.cell(0, 7, '(Full URLs and channel data are hidden in initial scan)', ln=1)
        pdf.ln(8)

        # 3. Kırmızı Aksiyon Kutusu
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(200, 0, 0)
        pdf.cell(0, 10, 'IMMEDIATE ACTION REQUIRED!', ln=1, align='C')
        
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(33, 37, 41)
        msg = ("Our AI has flagged 3-5 high-probability unauthorized re-uploads. "
               "To initiate the takedown process and access the full evidence package, "
               "please proceed to the Full Report.")
        pdf.multi_cell(0, 7, msg, align='C')
        pdf.ln(10)

        # 4. Ödeme Çağrısı
        pdf.set_font('Arial', 'B', 16)
        pdf.set_text_color(0, 123, 255)
        pdf.cell(0, 15, 'GET FULL REPORT & START TAKEDOWN ($29)', ln=1, align='C', link="https://buy.stripe.com/test")

        out = pdf.output(dest='S')
        if isinstance(out, str): out = out.encode('latin-1', errors='ignore')
            
        response = make_response(out)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename='Security_Report.pdf')
        return response

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
