import time
import pyautogui

pyautogui.FAILSAFE = True
print("WARNING! Please use this script carefully")
print("Move to top left corner of the screen to stop this script")
num = input("Please enter the number you want to press Enter:")

time.sleep(5)

for i in range(int(num)):
    pyautogui.press("enter")
    pyautogui.PAUSE = 2
    print(i)


