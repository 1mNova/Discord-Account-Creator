import os
from datetime import datetime
from pystyle import Colors, Colorate, System, Write



def Success(text):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    Write.Print(text + '\n', Colors.rainbow, interval=0)

def Error(text):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    Write.Print(text + '\n', Colors.rainbow, interval=0)