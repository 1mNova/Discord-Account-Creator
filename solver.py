from turtle import title
from tensorflow.keras.models import load_model
import Utils.logger as Logger
import cv2, os, json, hcaptcha, win32console, numpy as np, random, string, httpx, tensorflow as tf
model = load_model('hcaptcha/imagedata.h5')
config =  json.load(open('hcaptcha/config.json'))



class Utils:
    def getRandomText( length=5, charType="l"):
        randomText = []
        if charType == "l":
            return  ''.join(random.choice(string.ascii_lowercase) for x in range(length))
        elif charType == "u":
            return  ''.join(random.choice(string.ascii_uppercase) for x in range(length))
        elif charType == "n":
            return  ''.join(random.choice(string.digits) for x in range(length))
        elif charType == "a":
            tempList = []
            for i in range(length):
                r = random.randint(1,3)
                if r == 1:
                    tempList.append(random.choice(string.ascii_lowercase)  )
                elif  r ==2:
                    tempList.append(random.choice(string.ascii_uppercase)  )
                else:
                    tempList.append(random.choice(string.digits)  )

            return  ''.join(tempList)

class Solver:
    def SolvehCaptcha(siteurl, sitekey):
        ch = hcaptcha.Challenge(site_key=sitekey, site_url=siteurl, timeout=10)
        print(ch)
        if ch.token:
            print(ch.token)
            exit()
        Logger.Success(ch.question["en"])
        for tile in ch:
            image = tile.get_image(raw=True)
            img = cv2.imdecode(np.fromstring(image, np.uint8), cv2.IMREAD_COLOR)
            img = cv2.resize(img,(config['image_size'],config['image_size']))
            img = np.expand_dims(img, axis=0)
            res = np.argmax(model.predict(img),axis=1)
            if res == 0:
                img_type = 'airplaine'
            if res == 1:
                img_type = 'bicycle'
            if res == 2:
                img_type = 'boat'
            if res == 3:
                img_type = 'motorbus'
            if res == 4:
                img_type = 'motorcycle'
            if res == 5:
                img_type = 'seaplane'
            if res == 6:
                img_type = 'train'
            if res == 7:
                img_type = 'truck'

            if img_type in ch.question["en"]:
                Logger.Success(f'[+] Fetched Image : {img_type} | {tile}....')
                ch.answer(tile)
            else:
                Logger.Error(f'[-] False, Image Is :  {img_type} | {tile}....')
        try:
            token = ch.submit()
            return token
        except hcaptcha.ChallengeError as err:
            print(err)


#while True:
    #token = Solver.SolvehCaptcha("https://discord.com", "4c672d35-0701-42b2-88c3-78380b0db560")
    #print(token)
