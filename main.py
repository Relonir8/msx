from flask import Flask, Response, request
import requests

app = Flask(__name__)

# URL прокси для YouTube
PROXY_URL = "https://webproxy.lumiproxy.com/request?area=PL&u=https://www.youtube.com/tv#/"

# Сессия для сохранения cookie
session = requests.Session()

@app.route("/", methods=["GET", "POST"])
def proxy():
    try:
        # Подключение к прокси-серверу
        response = session.get(PROXY_URL, headers={"User-Agent": "Mozilla/5.0"})
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("Content-Type", "text/html")
        )
    except Exception as e:
        return f"Ошибка подключения: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
