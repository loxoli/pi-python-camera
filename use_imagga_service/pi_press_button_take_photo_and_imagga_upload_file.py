# pi_press_button_take_photo_and_imagga_upload_file.py
# Take a picture after the button pressed
# & Upload file to imagga service and get the result of tag
#
# Date   : 2016/03/27

import RPi.GPIO as GPIO
import time
import picamera
import requests
import json

GPIO.setmode(GPIO.BOARD)
BTN_PIN = 11
GPIO.setup(BTN_PIN, GPIO.IN,pull_up_down=GPIO.PUD_UP)

def callback_function(channel):
    print("Start to take a photo...")

    with picamera.PiCamera() as camera:
        # Camera warm-up time
        #time.sleep(2)
        # The default resolution is 1280x800
        camera.capture('tmp-image.jpg')
        url = "http://api.imagga.com/v1/content"
        files = {"file": open("/home/pi/tmp-image.jpg", "rb")}

        headers = {
            'accept': "application/json",
            'authorization': "Basic [REPLACE_YOUR_API_KEY_HERE]"
            }
        response = requests.post(url, files=files, headers=headers)
        print(response.text)
        data = json.loads(response.text.encode("ascii"))
        print(data["uploaded"][0]["id"])

        url = "http://api.imagga.com/v1/tagging"
        querystring = {"content": data["uploaded"][0]["id"]}
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text.encode("ascii"))
        print(data["results"][0]["tags"][0]["tag"].encode("ascii"))

    print("End to take")

try:
    GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, callback=callback_function, bouncetime=2000)

    while True:
        time.sleep(5)

except KeyboardInterrupt:
    print "Exception: KeyboardInterrupt"

finally:
    GPIO.cleanup()