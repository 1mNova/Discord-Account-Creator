from email import utils
from xml.dom.minidom import parseString
import time
from datetime import datetime
from base64 import b64encode as b
from httpx_socks import SyncProxyTransport
from outcome import capture
import websocket, json, threading, os, ctypes, random, string, httpx, requests,json,traceback
from data.config import CAPTCHA_KEY
from solver import Solver
class Utils:
    @staticmethod
    def GetProxy():
      with open('data/proxies.txt', "r") as f:
        return "http://" + random.choice(f.readlines()).strip()

    @staticmethod
    def randomc(len):
        return os.urandom(len).hex()[len:]
    
    @staticmethod
    def clearconsole():
        command = 'clear'
        if os.name in ('nt', 'dos'):
            command = 'cls'   
        os.system(command)
    
    @staticmethod
    def GetCookies():
        return f'__dcfduid={Utils.randomc(43)}; __sdcfduid={Utils.randomc(96)}; __stripe_mid={Utils.randomc(18)}-{Utils.randomc(4)}-{Utils.randomc(4)}-{Utils.randomc(4)}-{Utils.randomc(18)}; locale=en-GB; __cfruid={Utils.randomc(40)}-{"".join(random.choice(string.digits) for i in range(10))}'
    
    @staticmethod
    def GetUsername():
        usernames = open("data/usernames.txt", encoding="cp437", errors='ignore').read().splitlines()
        return random.choice(usernames)

class WebSocket:
    @staticmethod
    def Connect(token):
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        response = ws.recv()
        event = json.loads(response)
        auth = {'op': 2, 'd': {'token': token, 'capabilities': 61, 'properties': {'os': 'Windows', 'browser': 'Chrome', 'device': '',  'system_locale': 'en-GB', 'browser_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 'browser_version': '90.0.4430.212', 'os_version': '10', 'referrer': '', 'referring_domain': '', 'referrer_current': '', 'referring_domain_current': '', 'release_channel': 'stable', 'client_build_number': '85108', 'client_event_source': 'null'}, 'presence': {'status': random.choice(['online', 'dnd', 'idle']), 'since': 0, 'activities': [{ "name": "Custom Status", "type": 4, "state": "discord funny", "emoji": None }], 'afk': False}, 'compress': False, 'client_state': {'guild_hashes': {}, 'highest_last_message_id': '0', 'read_state_version': 0, 'user_guild_settings_version': -1}}};
        ws.send(json.dumps(auth))
config = json.load(open("config2.json"))
debug = config["debug"]
if len(config["bio"]) == 0:
    bio = None
else:
    bio = config["bio"]
invite = config["invite_code"]
super_properties = b(json.dumps({"os":"Windows","browser":"Firefox","device":"","system_locale":"en-US","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0","browser_version":"94.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":9999,"client_event_source": 'null'}, separators=(',', ':')).encode()).decode()
headers = {"Accept": "*/*", "Accept-Language": "en-US", "Connection": "keep-alive", "Content-Type": "application/json", "DNT": "1", "Host": "discord.com", "Referer": f"https://discord.com/invite/{invite}", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "TE": "trailers", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0", "X-Discord-Locale": "en-US", "X-Super-Properties": super_properties}
transport = SyncProxyTransport.from_url(Utils.GetProxy())

class solver():
    def solveCaptcha(websiteKey, websiteUrl, UserAgent):
           solvedCaptcha = None
           taskId = ""
           captchaKey = config["key"]

           taskId = httpx.post(f"https://api.{config['capapi']}/createTask", json={"clientKey": captchaKey, "task": { "type": "HCaptchaTaskProxyless",  "websiteURL": websiteUrl, "websiteKey": websiteKey, "userAgent": UserAgent}}, timeout=30).json()
           if int(taskId["errorId"]) > 0:
                print(f"error while creating task: {taskId['errorDescription']}")

           taskId = taskId["taskId"]
            
           while not solvedCaptcha:
                    captchaData = httpx.post(f"https://api.{config['capapi']}/getTaskResult", json={"clientKey": captchaKey, "taskId": taskId}, timeout=30).json()
                    if str(captchaData["status"]) == "ready":
                        solvedCaptcha = captchaData["solution"]["gRecaptchaResponse"]
                        if debug == True:
                            print("captcha solved")
                        return solvedCaptcha

def generateToken():
    try:
        proxy = random.choice(open("data/proxies.txt").read().splitlines())
        session = httpx.Client(headers=headers, cookies={"locale": "en-US"}, proxies={"all://": f"http://{proxy}"})
        session.headers["X-Fingerprint"] = session.get("https://discord.com/api/v9/experiments", timeout=30).json()["fingerprint"]
        username = random.choice(open("data/usernames.txt","r").read().splitlines())
        fingerprint = session.headers["X-Fingerprint"]
        start_time = time()
        #captcha = solver.solveCaptcha('4c672d35-0701-42b2-88c3-78380b0db560', 'https://discord.com/', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
    except Exception as e:
        if debug == True:
            print(e)
    
    try:
        captcha = httpx.post("http://localhost:8080/api/v1/captchasolver", json={ "site_key": "4c672d35-0701-42b2-88c3-78380b0db560", "site_url": "https://discord.com/" }, timeout=None).text
        #captcha = solver.solveCaptcha('4c672d35-0701-42b2-88c3-78380b0db560', 'https://discord.com/', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
        payload = { "fingerprint": fingerprint, "username": username, "invite": invite, "gift_code_sku_id": None, "captcha_key": captcha, "Consent": "true" }
        response = session.post('https://discord.com/api/v9/auth/register', json=payload)
        print(response.text)
        
        if response.status_code == 201:
            token = response.json()['token']
            print(f'joined server: {token[:25]}...')
            WebSocket.Connect(token)
            email = Utils.randomc(8)+"@outlook.io"
            payload = { 'email': email, 'password': 'Void7331@', 'date_of_birth': '1998-01-05', 'bio': bio }
            headsss = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.1012 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36', 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"','accept': '*/*', 'x-debug-options': 'bugReporterEnabled', 'x-discord-locale': 'fr', 'authorization': token }
            resp = session.patch('https://discord.com/api/v9/users/@me', json=payload, headers=headsss).json()
            print("sleeping")
            time.sleep(10)

            try:
                WebSocket.Connect(resp['token'])
                with open('data/output.txt', 'a') as fp:
                    fp.write(resp['token'] + "\n")
                    return
            except:
                WebSocket.Connect(token)
                with open('data/output.txt', 'a') as fp:
                    fp.write(token + "\n")
                    return
        else:
            return
    except Exception as e:
        print(traceback.format_exc())
        return
while True:
    if threading.active_count()<=int(config["threads"]):
        threading.Thread(target=generateToken).start()