import httpx


captchakey = httpx.post("http://localhost:8080/api/v1/captchasolver", json={
    "site_key": "91e4137f-95af-4bc9-97af-cdcedce21c8c",
    "site_url": "https://www.epicgames.com/"
}, timeout=None)
print(captchakey.text)