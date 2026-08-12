import os
import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 10000))
LOG_PATH = "/data/logs/latest.log"

claim_link = None
recent_lines = []
link_lock = threading.Lock()

def watch_log():
    global claim_link, recent_lines
    import time

    while not os.path.exists(LOG_PATH):
        time.sleep(2)
        print(f"[server.py] Waiting for log file at {LOG_PATH}...")

    print(f"[server.py] Log file found, watching...")

    with open(LOG_PATH, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                line = line.strip()
                print(f"[LOG] {line}")
                with link_lock:
                    recent_lines.append(line)
                    if len(recent_lines) > 50:
                        recent_lines.pop(0)
                    match = re.search(r'(https://playit\.gg/[^\s]+)', line)
                    if match:
                        claim_link = match.group(1)
                        print(f"[server.py] Found link: {claim_link}")
            else:
                time.sleep(1)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with link_lock:
            link = claim_link
            lines = list(recent_lines)

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        logs_html = ""
        if lines:
            log_text = "\n".join(lines[-30:])
            logs_html = f"""
            <h3>📄 Recent Server Logs</h3>
            <pre style="background:#111;color:#0f0;padding:16px;border-radius:6px;
                        font-size:12px;overflow-x:auto;white-space:pre-wrap">{log_text}</pre>
            """

        if link:
            html = f"""
            <html><body style="font-family:sans-serif;padding:40px;max-width:800px">
            <h2>✅ Minecraft Server Running</h2>
            <p><strong>playit.gg claim link:</strong></p>
            <a href="{link}" target="_blank" style="font-size:1.2em">{link}</a>
            {logs_html}
            </body></html>
            """
        else:
            log_status = f"Log file found, reading {len(lines)} lines..." if os.path.exists(LOG_PATH) else "⚠️ Log file not found yet at " + LOG_PATH
            html = f"""
            <html><body style="font-family:sans-serif;padding:40px;max-width:800px">
            <h2>⏳ Minecraft Server Starting...</h2>
            <p>Status: {log_status}</p>
            <p>The playit.gg claim link hasn't appeared yet. Auto-refreshing...</p>
            <script>setTimeout(()=>location.reload(), 8000)</script>
            {logs_html}
            </body></html>
            """

        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        pass


watcher = threading.Thread(target=watch_log, daemon=True)
watcher.start()

server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"[server.py] Listening on port {PORT}")
server.serve_forever()