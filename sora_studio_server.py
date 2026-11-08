#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sora Theme Studio Server (Port 5901)
Serves the full Sora Generative UI & Design Token Studio with all 105 theme presets on Port 5901.
Lead: Agent Sora (空 - The Loom)
"""

import os
import sys
import json
import urllib.parse
from pathlib import Path
from http.server import HTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = 5901
SORA_DIR = Path(__file__).resolve().parent
STUDIO_HTML = SORA_DIR / "sora_web_studio.html"
MANIFEST_FILE = SORA_DIR / "ALL_THEMES_MANIFEST.json"
HUB_OUTBOX = SORA_DIR.parent / "hub" / "MilaOutbox"

class SoraStudioHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SORA_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("", "/", "/index.html", "/studio", "/theme"):
            if STUDIO_HTML.exists():
                b = STUDIO_HTML.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)
                return
        elif parsed.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "app": "MilaCore Sora Theme Studio",
                "port": PORT,
                "lead": "Sora (空 - The Loom)",
                "themes_count": 105
            }).encode("utf-8"))
            return
        elif parsed.path in ("/api/manifest", "/api/themes"):
            if MANIFEST_FILE.exists():
                b = MANIFEST_FILE.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)
                return
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/api/sync_theme", "/api/theme_sync"):
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
            try:
                data = json.loads(post_body)
                HUB_OUTBOX.mkdir(parents=True, exist_ok=True)
                (HUB_OUTBOX / "sora_theme_sync.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "synced": True}).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
                return
        self.send_response(404)
        self.end_headers()


def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingHTTPServer(server_address, SoraStudioHandler)
    print(f"🎨 Sora Theme Studio running on http://127.0.0.1:{PORT} and http://milacore.ai:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSora Theme Studio stopped.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

