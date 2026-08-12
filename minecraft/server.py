import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 10000))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Minecraft server is running!")

    def log_message(self, format, *args):
        print(format % args)


server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Fake Render HTTP server listening on port {PORT}")
server.serve_forever()