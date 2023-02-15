import os

class Themes:
    def blackwhite(text):
        os.system(""); faded = ""
        red = 0; green = 0; blue = 0
        for line in text.splitlines():
            faded += (f"\033[38;2;{red};{green};{blue}m{line}\033[0m\n")
            if not red == 255 and not green == 255 and not blue == 255:
                red += 20; green += 20; blue += 20
                if red > 255 and green > 255 and blue > 255:
                    red = 255; green = 255; blue = 255
        return faded

    def cyan(text):
        os.system(""); fade = ""
        blue = 100
        for line in text.splitlines():
            fade += (f"\033[38;2;0;255;{blue}m{line}\033[0m\n")
            if not blue == 255:
                blue += 15
                if blue > 255:
                    blue = 255
        return fade

    def neon(text):
        os.system(""); fade = ""
        for line in text.splitlines():
            red = 255
            for char in line:
                red -= 2
                if red > 255:
                    red = 255
                fade += (f"\033[38;2;{red};0;255m{char}\033[0m")
            fade += "\n"
        return fade

    def purple(text):
        os.system(""); fade = "" 
        red = 255
        for line in text.splitlines():
            fade += (f"\033[38;2;{red};0;180m{line}\033[0m\n")
            if not red == 0:
                red -= 20
                if red < 0:
                    red = 0
        return fade

    def water(text):
        os.system(""); fade = ""
        green = 10
        for line in text.splitlines():
            fade += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
            if not green == 255:
                green += 15
                if green > 255:
                    green = 255
        return fade

    def fire(text):
        os.system(""); fade = ""
        green = 250
        for line in text.splitlines():
            fade += (f"\033[38;2;255;{green};0m{line}\033[0m\n")
            if not green == 0:
                green -= 25
                if green < 0:
                    green = 0
        return fade


def GetBanner():
    return f'''
                                ______            __       __          ______               __
                               / ____/___ _____  / /______/ /_  ____ _/ ____/___  _________/ /
                              / /   / __ `/ __ \/ __/ ___/ __ \/ __ `/ /   / __ \/ ___/ __  / 
                             / /___/ /_/ / /_/ / /_/ /__/ / / / /_/ / /___/ /_/ / /  / /_/ /  
                             \____/\__,_/ .___/\__/\___/_/ /_/\__,_/\____/\____/_/   \__,_/   
> captchacord.cc                       /_/                                                    
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
'''