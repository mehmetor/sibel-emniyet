# Railway demo sunucusu: yalnızca index.html'i sunar. Klasördeki notlar ve taslaklar dışarı açılmaz.
import http.server, os, pathlib

PAGE = pathlib.Path(__file__).with_name("index.html").read_bytes()

class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, body=True):
        path = self.path.split("?")[0]
        ok = path in ("/", "/index.html")
        self.send_response(200 if ok else 404)
        self.send_header("Content-Type", "text/html; charset=utf-8" if ok else "text/plain; charset=utf-8")
        data = PAGE if ok else b"Bulunamadi"
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Robots-Tag", "noindex, nofollow")  # demo: arama motorlarına kapalı
        self.end_headers()
        if body: self.wfile.write(data)
    def do_GET(self): self._send()
    def do_HEAD(self): self._send(False)

http.server.ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()
