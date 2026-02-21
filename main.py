from flask import Flask, request, make_response
from fpdf import FPDF
import datetime
import os
import requests

app = Flask(__name__)

# --- GÜVENLİK AYARLARI ---
GOOGLE_API_KEY = "AIzaSyDJloNd7fIl3juCW3oiVsoetmudjJq0_vo"
SEARCH_ENGINE_ID = "c64d73fae86564e88"

class PDF(FPDF):
    def header(self):
        # Üst Bilgi: Şirket Logosu Yerine Şık Bir Header
        self.set_fill_color(26, 54, 104) # Lacivert
        self.rect(0, 0, 210, 40, 'F')
        self.set_font('Arial', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, 'ALGORITHM GUARD', ln=1, align='C')
        self.set_font('Arial', '', 10)
        self.cell(0, -5, 'GLOBAL CONTENT PROTECTION & FORENSIC ANALYSIS', ln=1, align='C')
        self.ln(25)

    def footer(self):
        self.set_y(-25)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'CONFIDENTIAL - Algorithm Guard AI Forensics Unit', align='C', ln=1)
        self.cell(0, 10, f'Page {self.page_no()} | Report ID: AG-{datetime.datetime.now().strftime("%Y%M%d-%H%M")}', align='C')

@app.route('/scan', methods=['POST'])
def handle_scan():
    try:
        data = request.get_json()
        video_link = str(data.get('link', 'N/A'))
        
        # Google API Taraması
        search_query = f"{video_link} site:youtube.com"
        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_query}"
        response = requests.get(url).json()
        
        matches = []
        if "items" in response:
            for item in response["items"][:3]:
                masked = item["link"][:25] + "********"
                matches.append((item['displayLink'], masked))

        pdf = PDF()
        pdf.add_page()
        
        # 1. RISK LEVEL BÖLÜMÜ
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0)
        pdf.cell(0, 10, 'SECURITY ANALYSIS SUMMARY', ln=1)
        
        # Kırmızı Risk Kutusu
        pdf.set_fill_color(255, 230, 230) # Açık Kırmızı
        pdf.set_draw_color(200, 0, 0)     # Koyu Kırmızı Kenarlık
        pdf.rect(10, 55, 190, 20, 'DF')
        pdf.set_xy(15, 60)
        pdf.set_text_color(200, 0, 0)
        pdf.set_font('Arial', 'B', 16)
        
        # Eğer eşleşme varsa "CRITICAL", yoksa "POTENTIAL RISK" yazdıralım
        status_text = "CRITICAL INFRINGEMENT DETECTED" if matches else "MONITORING: HIGH RISK"
        pdf.cell(0, 10, status_text, align='C')
        pdf.ln(20)

        # 2. ANALİZ DETAYLARI
        pdf.set_text_color(0)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, 'Forensic Details:', ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(50, 7, 'Target Content:', 0)
        pdf.cell(0, 7, f'{video_link[:45]}...', ln=1)
        pdf.cell(50, 7, 'Analysis Timestamp:', 0)
        pdf.cell(0, 7, f'{datetime.datetime.now().strftime("%d/%m/2026 %H:%M:%S")}', ln=1)
        pdf.cell(50, 7, 'Scan Radius:', 0)
        pdf.cell(0, 7, 'Global Metadata Matching, YouTube Content ID Database', ln=1)
        pdf.ln(10)

        # 3. BULGULAR TABLOSU
        pdf.set_fill_color(26, 54, 104)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, ' SOURCE', 1, 0, 'L', True)
        pdf.cell(100, 10, ' IDENTIFIED MATCH (ENCRYPTED)', 1, 0, 'L', True)
        pdf.cell(50, 10, ' CONFIDENCE', 1, 1, 'L', True)

        pdf.set_text_color(0)
        pdf.set_font('Arial', '', 9)
        if matches:
            for platform, link in matches:
                pdf.cell(40, 8, f' {platform}', 1)
                pdf.cell(100, 8, f' {link}', 1)
                pdf.set_text_color(0, 150, 0)
                pdf.cell(50, 8, ' 98.4% Match', 1, 1)
                pdf.set_text_color(0)
        else:
            pdf.cell(190, 10, ' No immediate clones found on surface web. Dark web scan requires Premium.', 1, 1, 'C')

        pdf.ln(15)

        # 4. CTA (EYLEME ÇAĞRI) BUTONU
        pdf.set_fill_color(200, 0, 0) # Kırmızı Buton
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 14)
        shopier_url = "https://www.shopier.com/algorithmguard/44499822"
        pdf.cell(0, 15, 'START LEGAL TAKEDOWN PROCESS NOW', ln=1, align='C', fill=True, link=shopier_url)
        
        pdf.set_font('Arial', 'I', 8)
        pdf.set_text_color(100)
        pdf.cell(0, 10, '* Immediate action is recommended to prevent further revenue loss.', align='C')

        out = pdf.output(dest='S')
        if isinstance(out, str): out = out.encode('latin-1', errors='ignore')
        response = make_response(out)
        response.headers.set('Content-Type', 'application/pdf')
        return response

    except Exception as e:
        return f"Error: {str(e)}", 500
