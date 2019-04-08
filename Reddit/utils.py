import os
import shutil
import keyboard
import math

def removeFolders(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def waitPress(key):
    while True:
        try:
            if keyboard.is_pressed(key):
                break
            else:
                pass
        except:
            break

def roundIntToEven(int):
    print('ini = ' + str(int) +  'final = ' + str(2 * math.floor(int / 2)))
    return 2 * math.floor(int / 2)
