import os
import requests
from typing import Optional, List

class WordPressJWTAuth:
    def __init__(self):
        self.base_url = os.getenv("WP_BASE_URL", "").rstrip("/")
        self.user = os.getenv("WP_USER", "")
        self.password = os.getenv("WP_PASS", "")
        self.token = None
        
        if not all([self.base_url, self.user, self.password]):
            raise RuntimeError("WP_BASE_URL, WP_USER, WP_PASS required")
    
    def authenticate(self) -> bool:
        """Usa Application Passwords (WordPress 5.6+) invece di JWT"""
        # Con Application Passwords non serve ottenere un token,
        # basta usare HTTP Basic Auth direttamente
        return True
    
    def post_exists_by_slug(self, slug: str) -> bool:
        url = f"{self.base_url}/wp-json/wp/v2/posts"
        params = {"slug": slug, "status": "any"}
        try:
            r = requests.get(url, params=params, auth=(self.user, self.password))
            return len(r.json()) > 0
        except: return False
    
    def publish_post(self, title: str, content_html: str, slug: str = "", status: str = "draft", categories: List[int] = None, tags: List[str] = None, excerpt: str = "") -> Optional[str]:
        if not self.authenticate(): return None
        
        if not slug:
            slug = title.lower().replace(" ", "-")[:50]
        
        if self.post_exists_by_slug(slug):
            print(f"Post già esistente con slug '{slug}'")
            return None
        
        url = f"{self.base_url}/wp-json/wp/v2/posts"
        payload = {
            "title": title,
            "content": content_html,
            "slug": slug,
            "status": status,
            "excerpt": excerpt
        }
        
        if categories:
            payload["categories"] = categories
        if tags:
            payload["tags"] = tags
        
        try:
            r = requests.post(url, json=payload, auth=(self.user, self.password))
            if r.status_code in [200, 201]:
                post_url = r.json().get("link", "")
                print(f"Post pubblicato: {post_url}")
                return post_url
            else:
                print(f"Errore pubblicazione: {r.status_code} - {r.text}")
                return None
        except Exception as e:
            print(f"Eccezione pubblicazione: {e}")
            return None
