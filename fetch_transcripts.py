#!/usr/bin/env python3
"""Download the public motivated-mislabeling judge-input transcripts.

These transcripts are released by Anthropic / Aengus Lynch as part of
"Agentic Misalignment in Summer 2026". They are NOT redistributed in this repo;
this script fetches them into ./transcripts/ so the harness can run.
"""
import json, os, urllib.request

BASE = "https://www.aenguslynch.com/portfolio-transcript-viewer/"
MANIFEST = BASE + "static/manifest.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcripts")

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": BASE})
    return urllib.request.urlopen(req, timeout=30).read()

def main():
    os.makedirs(OUT, exist_ok=True)
    man = json.loads(get(MANIFEST))
    mis = [v for v in man["transcripts"] if v["id"].startswith("mislabel-input")]
    print(f"{len(mis)} motivated-mislabeling transcripts in manifest")
    for v in mis:
        dst = os.path.join(OUT, os.path.basename(v["href"]))
        if os.path.exists(dst):
            continue
        open(dst, "wb").write(get(BASE + v["href"]))
        print("  fetched", os.path.basename(dst))
    print("done ->", OUT)

if __name__ == "__main__":
    main()
