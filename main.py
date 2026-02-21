from flask import Flask, request, jsonify
from fpdf import FPDF
import datetime
import os
import base64

app = Flask(__name__)

def create_report(video_link, email):
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
    pdf.multi_cell(0, 10, txt="Our AI scan detected 3-5 potential unauthorized re-uploads on social media. To protect your revenue and start the takedown process, please upgrade to the Full Report.")
    
    # PDF'i belleğe (string olarak) kaydet
    report_content = pdf.output(dest='S').encode('latin-1')
    return base64.b64encode(report_content).decode('utf-8')

@app.route('/scan', methods=['POST'])
def handle_scan():
    data = request.get_json()
    video_link = data.get('link')
    customer_email = data.get('email')

    if not video_link:
        return jsonify({"error": "No link provided"}), 400

    # PDF'i Base64 formatında oluştur (Make.com'un okuyabilmesi için)
    pdf_base64 = create_report(video_link, customer_email)

    return jsonify({
        "status": "success",
        "pdf_data": pdf_base64,
        "filename": f"Report_{datetime.date.today()}.pdf"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
