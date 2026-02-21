from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Algorithm Guard Online!"

if __name__ == '__main__':
    print("SUNUCU BASLATILIYOR...")
    app.run(host='0.0.0.0', port=5000)