# Railway sunucusu: tek servis, iki alan adı.
#   demo.* ve *.up.railway.app  -> index.html (sitenin tamamı, arama motorlarına kapalı)
#   diğer her alan adı           -> yapim.html (yapım aşamasında sayfası)
# Klasördeki notlar ve taslaklar dışarı açılmaz; başka hiçbir dosya sunulmaz.
import http.server, os, pathlib

HERE = pathlib.Path(__file__).parent

# Umami (analytics.simetri.app). Ana alan adının kimliği aşağıda varsayılan olarak durur; ortam değişkeniyle değiştirilebilir.
#   UMAMI_WEBSITE_ID       -> ana alan adı (yapım aşamasında sayfası, ileride sitenin kendisi)
#   UMAMI_DEMO_WEBSITE_ID  -> demo (isteğe bağlı; boşsa demo ölçülmez)
UMAMI_SRC = os.environ.get("UMAMI_SRC", "https://analytics.simetri.app/script.js")

def page(name, website_id):
    html = (HERE / name).read_text(encoding="utf-8")
    website_id = (website_id or "").strip()
    if website_id:
        html = html.replace("<style>", '<script defer src="%s" data-website-id="%s"></script>\n<style>' % (UMAMI_SRC, website_id), 1)
    return html.encode("utf-8")

SITE = page("index.html", os.environ.get("UMAMI_DEMO_WEBSITE_ID"))
SOON = page("yapim.html", os.environ.get("UMAMI_WEBSITE_ID", "e402c698-6060-4afb-929a-e2515a86f74f"))

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
