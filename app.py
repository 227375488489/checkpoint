#!/usr/bin/env python3
# server.py — простой файловый сервер с CORS, пытается слушать 51.75.118.170:20084

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import socket
import sys

class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Разрешаем CORS (если нужно)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def serve(host, port):
    server = ThreadingHTTPServer((host, port), CORSHandler)
    sa = server.socket.getsockname()
    print(f"🚀 Serving HTTP on {sa[0]} port {sa[1]} (http://{sa[0]}:{sa[1]}/) ...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server.shutdown()

if __name__ == "__main__":
    HOST_WANTED = "51.75.118.170"
    PORT = 20084

    # Попытаемся привязаться к желаемому IP; при ошибке используем 0.0.0.0
    try:
        serve(HOST_WANTED, PORT)
    except OSError as e:
        print(f"⚠️ Не удалось привязать {HOST_WANTED}:{PORT}: {e}")
        fallback = "0.0.0.0"
        print(f"ℹ️ Попытка привязки к {fallback}:{PORT} вместо этого...")
        try:
            serve(fallback, PORT)
        except Exception as e2:
            print(f"❌ Не удалось запустить сервер: {e2}")
            sys.exit(1)
