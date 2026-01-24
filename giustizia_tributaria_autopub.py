# -*- coding: utf-8 -*-
"""
GIUSTIZIA TRIBUTARIA -> AUTO SCRAPE (Playwright) -> FILTER "FAVORE CONTRIBUENTE" -> COMMENTO (OpenAI) -> PUBBLICA SU WORDPRESS (JWT)
"""
import os
import re
import json
import time
import hashlib
import random
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import pdfplumber
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# === IMPORT WP AUTH ===
from aeo_jwt_auth import WordPressJWTAuth

# ENV / CONFIG
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
BASE_URL = os.getenv("GT_BASE_URL", "https://bancadatigiurisprudenza.giustiziatributaria.gov.it/")
SEARCH_PATH = os.getenv("GT_SEARCH_PATH", "ricerca")
START_URL = urljoin(BASE_URL, SEARCH_PATH)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip()
WP_CATEGORY_ID = int(os.getenv("WP_CATEGORY_ID", "3"))
WP_POST_STATUS = os.getenv("WP_POST_STATUS", "draft").strip().lower()
MAX_ITEMS_PER_RUN = int(os.getenv("GT_MAX_ITEMS_PER_RUN", "15"))
MAX_PUBLISH_PER_RUN = int(os.getenv("GT_MAX_PUBLISH_PER_RUN", "3"))
SLEEP_BETWEEN_ITEMS = float(os.getenv("GT_SLEEP_BETWEEN_ITEMS", "2.5"))
SLEEP_JITTER_MAX = float(os.getenv("GT_SLEEP_JITTER_MAX", "1.2"))
HEADLESS = os.getenv("GT_HEADLESS", "true").strip().lower() == "true"
NAV_TIMEOUT_MS = int(os.getenv("GT_NAV_TIMEOUT_MS", "45000"))
DISCLAIMER = os.getenv("GT_DISCLAIMER", "Il presente contenuto ha finalità esclusivamente informative e non costituisce consulenza legale.")

def clean_text(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"\s+", " ", s)
    return s

def slugify(text: str) -> str:
    text = (text or "").lower().strip()
    text = re.sub(r"[’']", "", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text[:80].strip("-")

def make_excerpt_from_html(html: str, max_len: int = 175) -> str:
    txt = re.sub(r"<[^>]+>", " ", html or "")
    txt = clean_text(txt)
    if len(txt) <= max_len: return txt
    return txt[:max_len-3].rstrip() + "..."

def stable_id_from_url(url: str) -> str:
    return hashlib.sha256((url or "").encode("utf-8")).hexdigest()[:10]

class OpenAICompat:
    def __init__(self, api_key: str, model: str):
        if not api_key: raise RuntimeError("OPENAI_API_KEY missing")
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model
    def classify_favorable(self, text: str) -> Dict:
        system = "Sei un avvocato tributarista. Classifica se la decisione è favorevole al contribuente."
        user = f"Testo: {text[:6000]} Restituisci JSON: outcome, confidence, rationale."
        r = self.client.chat.completions.create(model=self.model, messages=[{"role":"system","content":system},{"role":"user","content":user}], temperature=0)
        try:
            content = r.choices[0].message.content
            return json.loads(re.search(r"\{.*\}", content, re.S).group(0))
        except: return {"outcome":"unknown"}
    def write_commentary_html(self, meta: Dict, url: str, text: str) -> str:
        system = "Sei un avvocato tributarista. Scrivi un commento HTML."
        user = f"Metadati: {json.dumps(meta) Fonte: {url} Testo: {text[:4000]}"
        r = self.client.chat.completions.create(model=self.model, messages=[{"role":"system","content":system},{"role":"user","content":user}], temperature=0.2)
        return r.choices[0].message.content

@dataclass
class DecisionItem:
    url: str; title: str = ""; date: str = ""; court: str = ""; outcome_hint: str = ""; pdf_url: str = ""; text_excerpt: str = ""

def run():
    wp = WordPressJWTAuth()
    if not wp.authenticate():
        print("Auth failed")
        return
    ai = OpenAICompat(OPENAI_API_KEY, MODEL)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.goto(START_URL)
        time.sleep(2)
        links = [urljoin(BASE_URL, h) for h in page.eval_on_selector_all("a", "els => els.map(e => e.getAttribute('href'))") if h and "dettaglio" in h.lower()][:MAX_ITEMS_PER_RUN]
        for url in links:
            page.goto(url)
            item = DecisionItem(url=url, title=page.title(), text_excerpt=page.content()[:3000])
            res = ai.classify_favorable(item.text_excerpt)
            if res.get("outcome") == "favorable":
                html = ai.write_commentary_html({"title":item.title}, url, item.text_excerpt)
                wp.publish_post(title=item.title, content_html=html, status=WP_POST_STATUS, slug=slugify(item.title))
        browser.close()

if __name__ == "__main__": run()
