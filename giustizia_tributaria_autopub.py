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
MAX_ITEMS_PER_RUN = int(os.getenv("GT_MAX_ITEMS_PER_RUN") or "15")
MAX_PUBLISH_PER_RUN = int(os.getenv("GT_MAX_PUBLISH_PER_RUN) or "3")
SLEEP_BETWEEN_ITEMS = float(os.getenv("GT_SLEEP_BETWEEN_) or "2.5")
SLEEP_JITTER_MAX = float(os.getenv("GT_SLEEP_JITTER_MAX") or "1.2")
