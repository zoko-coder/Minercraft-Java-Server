import os
import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 10000))
LOG_PATH = "/data/logs/latest.log"

claim_link = None
link_lock = threading.Lock()

def watch_log():
    global claim_link
    import time

    # Wait for log file to appear
    while not os.path.exists(LOG_PATH):
        time.sleep(2)

    with open(LOG_PATH, "r") as f:
        f.seek(0, 2)  # seek to end
        while True:
            line = f.readline()
            if line:
                match = re.search(r'(https://playit\.gg/claim/[^\s]+)', line)
                if match:
                    with link_lock:
                        claim_link = match.group(1)
                    print(f"[server.py] Found claim link: {claim_link}")
            else:
                time.sleep(1)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with link_lock:
            link = claim_link

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        if link:
            html = f"""
            <html><body style="font-family:sans-serif;padding:40px">
            <h2>✅ Minecraft Server Running</h2>
            <p><strong>playit.gg claim link:</strong></p>
            <a href="{link}" target="_blank" style="font-size:1.2em">{link}</a>
            </body></html>
            """
        else:
            html = """
            <html><body style="font-family:sans-serif;padding:40px">
            <h2>⏳ Minecraft Server Starting...</h2>
            <p>The playit.gg claim link hasn't appeared yet.</p>
            <p>Refresh this page in 30–60 seconds.</p>
            <script>setTimeout(()=>location.reload(), 10000)</script>
            </body></html>
            """

        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        pass


# Start log watcher in background thread
watcher = threading.Thread(target=watch_log, daemon=True)
watcher.start()

server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"[server.py] Listening on port {PORT}")
server.serve_forever()