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
        url = f"{self.base_url}/wp-json/jwt-auth/v1/token"
        try:
            r = requests.post(url, json={"username": self.user, "password": self.password})
            if r.status_code == 200:
                self.token = r.json().get("token")
                return True
        except: pass
        return False

    def post_exists_by_slug(self, slug: str) -> bool:
        url = f"{self.base_url}/wp-json/wp/v2/posts"
        params = {"slug": slug, "status": "any"}
        try:
            r = requests.get(url, params=params)
            return len(r.json()) > 0
        except: return False

    def publish_post(self, title: str, content_html: str, slug: str = "", status: str = "draft", categories: List[int] = None, tags: List[str] = None, excerpt: str = "") -> Optional[str]:
        if not self.token and not self.authenticate(): return None
        url = f"{self.base_url}/wp-json/wp/v2/posts"
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "title": title,
            "content": content_html,
            "status": status,
            "slug": slug,
            "categories": categories or [],
            "excerpt": excerpt
        }
        try:
            r = requests.post(url, json=payload, headers=headers)
            if r.status_code in [200, 201]:
                return r.json().get("link")
        except: pass
        return None
