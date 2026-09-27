#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path

SRC = Path("public")
DST = Path("plain-html-site")

if not SRC.exists():
    raise SystemExit("Error: 'public' folder not found.")

if DST.exists():
    shutil.rmtree(DST)

shutil.copytree(SRC, DST)

def clean_html(html: str) -> str:
    # Remove Hugo livereload/dev scripts
    html = re.sub(
        r'<script[^>]*livereload[^>]*></script>',
        '',
        html,
        flags=re.IGNORECASE
    )

    # Remove localhost:1313 absolute URLs
    html = html.replace("http://localhost:1313/", "/")
    html = html.replace("https://localhost:1313/", "/")
    html = html.replace("//localhost:1313/", "/")

    # Remove generator meta if present
    html = re.sub(
        r'<meta\s+name=["\']generator["\'][^>]*>',
        '',
        html,
        flags=re.IGNORECASE
    )

    return html

for path in DST.rglob("*.html"):
    content = path.read_text(encoding="utf-8", errors="ignore")
    content = clean_html(content)
    path.write_text(content, encoding="utf-8")

print(f"Done. Clean static site created in: {DST.resolve()}")
