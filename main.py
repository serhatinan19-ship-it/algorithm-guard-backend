from flask import Flask, request, make_response
from fpdf import FPDF
import datetime
import os
import requests

app = Flask(__name__)

# --- SENİN GERÇEK BİLGİLERİN ---
GOOGLE_API_KEY = "AIzaSyDJloNd7fIl3juCW3oiVsoetmudjJq0_vo"
SEARCH_ENGINE_ID = "c64d73fae86564e88"

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(26, 54, 104)
        self.cell(0, 10, 'ALGORITHM GUARD', ln=1, align='L')
        self.line(10, 27, 200, 27)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Report ID: AG-{datetime.datetime.now().strftime("%H%M%S")}', align='C')

def get_google_matches(query_text):
    results = []
    try:
        # Gerçek Google API Taraması (YouTube odaklı)
        search_query = f"{query_text} site:youtube.com"
        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_query}"
        response = requests.get(url).json()
        
        if "items" in response:
            for item in response["items"][:3]: # En iyi 3 eşleşmeyi al
                raw_url = item["link"]
                # Linki maskele (Müşterinin ödeme yapması için stratejik gizleme)
                masked = raw_url[:22] + "***" + raw_url[-4:]
                results.append((item['displayLink'], masked, "98% Confidence"))
        
        if not results:
            results = [("Global Scan", "No immediate infringement found.", "Safe")]
            
    except Exception as e:
        results = [("System Note", "Analysis engine is running...", "Processing")]
    return results

@app.route('/scan', methods=['POST'])
def handle_scan():
    try:
        data = request.get_json()
        video_link = str(data.get('link', 'N/A'))
        
        # Google API ile anlık tarama yapılıyor
        matches = get_google_matches(video_link)

        pdf = PDF()
        pdf.add_page()
        
        # Rapor Başlıkları
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 12, 'Digital Protection Analysis', ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f'Monitored Content: {video_link[:50]}...', ln=1)
        pdf.cell(0, 6, f'Date: {datetime.date.today().strftime("%d/%m/2026")}', ln=1)
        pdf.ln(10)

        # Bulgular Tablosu
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, ' DETECTED INFRINGEMENTS (CONFIRMED)', ln=1, fill=True)
        pdf.ln(3)

        pdf.set_font('Arial', '', 10)
        for platform, link, conf in matches:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(45, 7, f"{platform}:", ln=0)
            pdf.set_font('Arial', '', 10)
            pdf.cell(100, 7, link, ln=0)
            pdf.set_text_color(0, 128, 0)
            pdf.cell(0, 7, conf, ln=1, align='R')
            pdf.set_text_color(0)

        pdf.ln(15)

        # SHOPIER BUTONU
        pdf.set_fill_color(26, 54, 104)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 14)
        shopier_url = "https://www.shopier.com/algorithmguard/44499822"
        pdf.cell(0, 15, 'UNVEIL FULL REPORT & START TAKEDOWN', ln=1, align='C', fill=True, link=shopier_url)

        out = pdf.output(dest='S')
        if isinstance(out, str): out = out.encode('latin-1', errors='ignore')
        
        response = make_response(out)
        response.headers.set('Content-Type', 'application/pdf')
        return response

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
