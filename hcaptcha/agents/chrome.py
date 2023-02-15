from ..http_ import HTTPClient
from .base import Agent
from urllib.parse import urlsplit
import json
import random

def latest_chrome_agent():
    with HTTPClient() as http:
        resp = http.request(
            method="GET",
            url="https://jnrbsn.github.io/user-agents/user-agents.json")
        data = json.loads(resp.read())
        return data[0]

class ChromeAgent(Agent):
    user_agent = latest_chrome_agent()
    chrome_version = user_agent.split("Chrome/", 1)[1].split(" ", 1)[0]
    chrome_version_short = chrome_version.split(".", 1)[0]
    header_order = [
        "host",
        "connection",
        "content-length",
        "sec-ch-ua",
        "cache-control",
        "content-type",
        "sec-ch-ua-mobile",
        "user-agent",
        "sec-ch-ua-platform",
        "accept",
        "origin",
        "sec-fetch-site",
        "sec-fetch-mode",
        "sec-fetch-dest",
        "referer",
        "accept-encoding",
        "accept-language",
    ]

    def __init__(self):
        super().__init__()
        self.screen_size, self.avail_screen_size = random.choice([
            ((1920, 1080), (1920, 1040)),
            ((2560, 1440), (2560, 1400))
        ])
        self.cpu_count = random.choice([2, 4, 8, 16])
        self.memory_gb = random.choice([2, 4, 8, 16])

    def get_screen_properties(self):
        return {
            "availWidth": self.avail_screen_size[0],
            "availHeight": self.avail_screen_size[1],
            "width": self.screen_size[0],
            "height": self.screen_size[1],
            "colorDepth": 24,
            "pixelDepth": 24,
            "availLeft": 0,
            "availTop": 0
        }

    def get_navigator_properties(self):
        return {
            "vendorSub": "",
            "productSub": "20030107",
            "vendor": "Google Inc.",
            "maxTouchPoints": 0,
            "userActivation": {},
            "doNotTrack": "1",
            "geolocation": {},
            "connection": {},
            "webkitTemporaryStorage": {},
            "webkitPersistentStorage": {},
            "hardwareConcurrency": self.cpu_count,
            "cookieEnabled": True,
            "appCodeName": "Mozilla",
            "appName": "Netscape",
            "appVersion": f"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.chrome_version} Safari/537.36",
            "platform": "Win32",
            "product": "Gecko",
            "userAgent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.chrome_version} Safari/537.36",
            "language": "en-US",
            "languages": ["en-US"],
            "onLine": True,
            "webdriver": False,
            "pdfViewerEnabled": True,
            "scheduling": {},
            "bluetooth": {},
            "clipboard": {},
            "credentials": {},
            "keyboard": {},
            "managed": {},
            "mediaDevices": {},
            "storage": {},
            "serviceWorker": {},
            "wakeLock": {},
            "deviceMemory": self.memory_gb,
            "ink": {},
            "hid": {},
            "locks": {},
            "mediaCapabilities": {},
            "mediaSession": {},
            "permissions": {},
            "presentation": {},
            "serial": {},
            "virtualKeyboard": {},
            "usb": {},
            "xr": {},
            "userAgentData": {
                "brands": [
                    {"brand": "Chromium", "version": self.chrome_version_short},
                    {"brand": "Google Chrome", "version": self.chrome_version_short},
                    {"brand": ";Not A Brand", "version": "99"}
                ],
                "mobile": False
            },
            "plugins": [
                "internal-pdf-viewer",
                "internal-pdf-viewer",
                "internal-pdf-viewer",
                "internal-pdf-viewer",
                "internal-pdf-viewer"
            ]
        }
    
    def format_headers(
        self,
        url: str,
        body: bytes = None,
        headers: dict = {},
        origin_url: str = None,
        sec_site: str = "cross-site",
        sec_mode: str = "cors",
        sec_dest: str = "empty"
    ) -> dict:
        p_url = urlsplit(url)
        p_origin_url = urlsplit(origin_url) if origin_url else None

        headers["Host"] = p_url.hostname
        headers["Connection"] = "keep-alive"
        headers["sec-ch-ua"] = f'"Chromium";v="{self.chrome_version_short}", "Google Chrome";v="{self.chrome_version_short}", ";Not A Brand";v="99"'
        headers["sec-ch-ua-mobile"] = "?0"
        headers["User-Agent"] = self.user_agent
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers.setdefault("Accept", "*/*")
        headers["Accept-Encoding"] = "gzip, deflate, br"
        headers["Accept-Language"] = "en-US,en;q=0.9"

        if body is not None:
            headers["Content-Length"] = str(len(body))

        headers["Sec-Fetch-Site"] = sec_site
        headers["Sec-Fetch-Mode"] = sec_mode
        headers["Sec-Fetch-Dest"] = sec_dest

        if sec_mode == "navigate":
            headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            if sec_site == "same-origin" and origin_url:
                headers["Referer"] = p_origin_url.scheme + "://" + p_origin_url.hostname + p_origin_url.path + (("?" + p_origin_url.query) if p_origin_url.query else "")
            elif origin_url:
                headers["Referer"] = p_origin_url.scheme + "://" + p_origin_url.hostname + p_origin_url.path + "/"
        
        elif sec_mode == "cors" and origin_url:
            headers["Origin"] = p_origin_url.scheme + "://" + p_origin_url.hostname
            headers["Referer"] = p_origin_url.scheme + "://" + p_origin_url.hostname + p_origin_url.path + (("?" + p_origin_url.query) if p_origin_url.query else "")
        
        elif sec_mode == "no-cors" and origin_url:
            headers["Origin"] = p_origin_url.scheme + "://" + p_origin_url.hostname
            headers["Referer"] = p_origin_url.scheme + "://" + p_origin_url.hostname + p_origin_url.path + (("?" + p_origin_url.query) if p_origin_url.query else "")

        headers = dict(sorted(
            headers.items(),
            key=lambda x: x[0].lower() in self.header_order \
                          and self.header_order.index(x[0].lower()) \
                          or 9999
        ))
        return headers