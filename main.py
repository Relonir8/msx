from flask import Flask, Response, request
import requests
import os
import pickle

app = Flask(__name__)

# URL прокси для YouTube
PROXY_URL = "https://webproxy.lumiproxy.com/request?area=US&u=https://www.youtube.com/tv#/"

# Сессия для сохранения cookies
session = requests.Session()
COOKIE_FILE = "cookies.pkl"

# Загрузка cookies при запуске
if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, "rb") as f:
        session.cookies.update(pickle.load(f))

# Главный маршрут для прокси
@app.route("/", methods=["GET", "POST"])
def proxy():
    try:
        # Отправка запроса к прокси-серверу
        response = session.get(
            PROXY_URL,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("Content-Type", "text/html")
        )
    except Exception as e:
        return f"Ошибка подключения: {e}", 500

# Сохранение cookies после каждого запроса
@app.after_request
def save_cookies(response):
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(session.cookies, f)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
