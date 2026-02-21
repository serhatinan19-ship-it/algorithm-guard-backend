from flask import Flask, request, send_file, make_response
from fpdf import FPDF
import datetime
import os
import io

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def handle_scan():
    data = request.get_json()
    video_link = data.get('link', 'Unknown')
    
    # PDF Oluşturma (Doğrudan belleğe)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ALGORITHM GUARD - SCAN REPORT", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Target Link: {video_link}", ln=True)
    
    pdf.ln(10)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt="INITIAL FINDINGS:", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, txt="Our AI detected 3-5 unauthorized re-uploads. Upgrade to Full Report for $29.")

    # PDF'i bir byte nesnesine çevir
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename=f'Report_{datetime.date.today()}.pdf')
    
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

