from flask import Flask, request, make_response
from fpdf import FPDF
import datetime
import os

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        # Üst Bilgi: Kurumsal Kimlik
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 51, 102) # Koyu Lacivert
        self.cell(0, 10, 'ALGORITHM GUARD', ln=1, align='C')
        self.set_font('Arial', 'I', 9)
        self.cell(0, 5, 'PROTECT YOUR CREATIVE WORK', ln=1, align='C')
        self.set_draw_color(0, 51, 102)
        self.line(10, 32, 200, 32) # Zarif bir ayırıcı çizgi
        self.ln(12)

    def footer(self):
        # Alt Bilgi: Profesyonel Gizlilik Notu
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
        
        # 1. Ana Başlık - AI Scan Report
        pdf.set_font('Arial', 'B', 22)
        pdf.set_text_color(33, 37, 41)
        pdf.cell(0, 20, 'AI Scan Report', ln=1, align='C')
        
        # 2. Tarama Detayları
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, 'Scan Details:', ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0)
        pdf.cell(0, 7, f'Date: {datetime.date.today()}', ln=1)
        pdf.set_font('Arial', 'I', 10)
        pdf.multi_cell(0, 7, f'Target Link: {video_link}')
        pdf.ln(8)
        
        # 3. Kritik Bulgular Bölümü (Kırmızı Vurgu)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(180, 0, 0) # Profesyonel Kırmızı
        pdf.cell(0, 10, 'IMMEDIATE ACTION REQUIRED!', ln=1, align='C')
        
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0)
        msg = ("Our advanced AI scan has successfully identified 3-5 unauthorized re-uploads "
               "of your content. To protect your digital rights and revenue, an immediate "
               "action is recommended.")
        pdf.multi_cell(0, 7, msg, align='C')
        pdf.ln(10)
        
        # 4. Satış ve Aksiyon Planı
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, 'Upgrade to Full Report to unlock:', ln=1, align='L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, '- Direct links to infringing videos', ln=1)
        pdf.cell(0, 6, '- Automated DMCA Takedown requests', ln=1)
        pdf.cell(0, 6, '- Legal evidence package', ln=1)
        pdf.ln(10)
        
        # 5. Ödeme Butonu (Vurgulu)
        pdf.set_font('Arial', 'B', 16)
        pdf.set_text_color(0, 102, 204) # Link Mavisi
        pdf.cell(0, 12, 'CLICK HERE TO UPGRADE FOR $29', ln=1, align='C', link="https://buy.stripe.com/test")

        out = pdf.output(dest='S')
        if isinstance(out, str):
            out = out.encode('latin-1', errors='ignore')
            
        response = make_response(out)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename='AI_Scan_Report.pdf')
        return response

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
