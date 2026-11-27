# Railway sunucusu: tek servis, iki alan adı.
#   demo.* ve *.up.railway.app  -> index.html (sitenin tamamı, arama motorlarına kapalı)
#   diğer her alan adı           -> yapim.html (yapım aşamasında sayfası)
# Klasördeki notlar ve taslaklar dışarı açılmaz; başka hiçbir dosya sunulmaz.
import http.server, os, pathlib

HERE = pathlib.Path(__file__).parent
SITE = (HERE / "index.html").read_bytes()
SOON = (HERE / "yapim.html").read_bytes()

class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, body=True):
        host = (self.headers.get("X-Forwarded-Host") or self.headers.get("Host") or "").split(":")[0].lower()
        demo = host.startswith("demo.") or host.endswith(".up.railway.app") or host in ("localhost", "127.0.0.1")
        path = self.path.split("?")[0]
        ok = path in ("/", "/index.html")
        if path == "/yapim" and demo: ok, demo = True, False  # demoda önizleme
        data = (SITE if demo else SOON) if ok else b"Bulunamadi"
        self.send_response(200 if ok else 404)
        self.send_header("Content-Type", "text/html; charset=utf-8" if ok else "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Vary", "Host")
        if demo or not ok: self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.end_headers()
        if body: self.wfile.write(data)
    def do_GET(self): self._send()
    def do_HEAD(self): self._send(False)

http.server.ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()
