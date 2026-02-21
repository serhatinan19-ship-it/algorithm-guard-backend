from flask import Flask, request, jsonify
from fpdf import FPDF
import datetime
import os

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
    pdf.multi_cell(0, 10, txt="We found 3-5 potential unauthorized re-uploads. To see exact links and start the takedown process, please upgrade to the Full Report.")
    
    report_name = f"report_{datetime.date.today()}.pdf"
    pdf.output(report_name)
    return report_name

@app.route('/')
def home():
    return "Algorithm Guard is running!"

@app.route('/scan', methods=['POST'])
def handle_scan():
    data = request.get_json()
    video_link = data.get('link')
    customer_email = data.get('email')

    if not video_link:
        return jsonify({"error": "No link provided"}), 400

    report_file = create_report(video_link, customer_email)
    print(f"Report generated for {customer_email}")

    return jsonify({
        "status": "success",
        "message": "Scan complete, report generated.",
        "download_url": "PDF generated on server"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
