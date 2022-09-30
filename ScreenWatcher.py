import time
import json
from playsound import playsound
from PIL import ImageGrab
from pushbullet import Pushbullet
from pushbullet import InvalidKeyError

pixelMark = [0, 0]
try:
    options = open("options.txt", "r")
    pixelMark = options.split()
except:
    pass
print('Welcome to ScreenWatcher, error 2002 edition')

def readPixelMark():
    options = open("options.txt", "r")
    raw = options.read()
    global pixelMark
    pixelMark = json.loads(raw)
def menu():
    choice = None
    while (choice == None):
        print("Enter your choice:")
        print("(1): Change mode - watches a pixel for any change")
        print("(2): Black Pixel mode - watches a pixel until it turns full black (255, 255, 255)")
        print("(3): Setup/Options")
        print("(4): Pushbullet setup - setup a Pushbullet connection to send push notifications to your device")
        print("(5): Quit.")
        choice = input()
        if choice == '1':
            changeMode()
        elif choice == '2':
            blackMode()
        elif choice == '3':
            setupMode()
        elif choice == '4':
            pushbulletSetup()
        if choice != '5':
            choice = None

def setupMode():
    try:
        print("Enter X value of pixel to watch:")
        x = input()
        print("Enter Y value of pixel to watch:")
        y = input()
        options = open("options.txt", "w")
        pixelMark = [int(x), int(y)]
        print (json.dumps(pixelMark))
        options.write(json.dumps(pixelMark))
        print("Options saved")
    except:
        print("An error occured. Options have not been saved.")

def changeMode():
    active = True
    readPixelMark()
    while active:
        screencap = ImageGrab.grab()
        upperLeftPixel = screencap.getpixel((pixelMark[0], pixelMark[1]))
        print(upperLeftPixel)
        print("Correct pixel on screen?")
        keyboard = input()
        if keyboard == "y":
            while True:
                time.sleep(10)
                screencap = ImageGrab.grab()
                newPixel = screencap.getpixel((pixelMark[0], pixelMark[1]))
                if upperLeftPixel != newPixel:
                    print("CHANGE DETECTED")
                    pushbulletSend()
                    while True:
                        playsound("alarmsound.mp3")
                        time.sleep(15)
        print("Are we finished?")
        keyboard = input()
        if keyboard == "y":
            active = false

def blackMode():
    active = True
    readPixelMark()
    print(pixelMark)
    while active:
        screencap = ImageGrab.grab()
        upperLeftPixel = screencap.getpixel((pixelMark[0], pixelMark[1]))
        print(upperLeftPixel)
        print("Watching pixel.")
        while True:
            time.sleep(10)
            screencap = ImageGrab.grab()
            newPixel = screencap.getpixel((pixelMark[0], pixelMark[1]))
            print(newPixel)
            if newPixel == ((0, 0, 0)):
                print("BLACK PIXEL DETECTED")
                pushbulletSend()
                while True:
                    playsound("alarmsound.mp3")
                    time.sleep(15)

def pushbulletSetup():
    print("Enter your PushBullet api-key (will be saved as plain-text, be safe): ")
    keyboard = input()
    try:
        pb = Pushbullet(keyboard)
        print("Key successful, saving...")
        f = open("pushbullet.txt", "w")
        f.write(keyboard)
        print("Successfully saved to file.")
    except InvalidKeyError:
        print("Key did not work, no changes made.")

def pushbulletSend():
    try:
        f = open("pushbullet.txt", "r")
        pb = Pushbullet(f.read())
        pb.push_note("Alert!", "You're getting 2002'd!")
    except:
        pass


menu()
