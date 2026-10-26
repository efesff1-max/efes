#!/usr/bin/env python3
"""Server lokal Klipo.

Cara pakai:
  pip install yt-dlp
  python server.py
Lalu buka http://localhost:8765 (index.html harus satu folder dengan file ini).
"""
import glob, mimetypes, os, shutil, subprocess, tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
DOMAINS = ("youtube.com", "youtu.be", "instagram.com", "tiktok.com")


def allowed(url):
    p = urlparse(url)
    h = (p.hostname or "").lower()
    return p.scheme in ("http", "https") and any(h == d or h.endswith("." + d) for d in DOMAINS)


class Handler(BaseHTTPRequestHandler):
    def reply(self, code, body=b"", ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = urlparse(self.path)
        if p.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                return self.reply(200, f.read(), "text/html; charset=utf-8")
        if p.path != "/api/fetch":
            return self.reply(404, b"Not found")
        url = parse_qs(p.query).get("url", [""])[0]
        if not allowed(url):
            return self.reply(400, "Link tidak didukung".encode())
        tmp = tempfile.mkdtemp(prefix="klipo-")
        try:
            subprocess.run(
                ["yt-dlp", "--no-playlist", "-f",
                 "best[ext=mp4][height<=720]/best[height<=720]/best",
                 "-o", os.path.join(tmp, "v.%(ext)s"), url],
                check=True, capture_output=True, timeout=600)
            path = glob.glob(os.path.join(tmp, "v.*"))[0]
            ctype = mimetypes.guess_type(path)[0] or "video/mp4"
            with open(path, "rb") as f:
                self.reply(200, f.read(), ctype)
        except FileNotFoundError:
            self.reply(500, "yt-dlp belum terpasang: pip install yt-dlp".encode())
        except Exception:
            self.reply(500, "Gagal mengambil video dari link".encode())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("Klipo jalan di http://localhost:8765")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
