from flask import Flask, request
from solver import Solver
from pystyle import Colors, Colorate, System, Write
import Utils.userinterface as ui
import ctypes, os, sys
import threading, httpx, win32console

app = Flask(__name__)
System.Init()

win32console.SetConsoleTitle('hCaptcha Solver - Server Active - Model Loaded')

@app.route('/api/v1/captchasolver', methods=['GET', 'POST'])
def lmao():
    if request.method == 'POST':
        json = request.json
        sitekey = json['site_key']
        siteurl = json['site_url']
        print(f"[+] Request Received To Solve hCaptcha... ({siteurl}:{sitekey})")
        captchakey = Solver.SolvehCaptcha(siteurl, sitekey)
        print(f'<-> hCaptcha Solved Successfully : {captchakey[:20]}...')
        return captchakey
    else:
        return "405: Method Not Allowed"
        
os.system('cls')

print(Colorate.Horizontal(Colors.purple_to_blue, ui.GetBanner(), 1))
app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)