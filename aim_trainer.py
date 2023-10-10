import pyautogui
from mss import mss
import cv2

# setup cv2 pattern
method = cv2.TM_SQDIFF
pattern = cv2.imread('patterns/aim.png')

def cv2_detect(image_path):
    screen = cv2.imread(image_path)
    result = cv2.matchTemplate(pattern, screen, method)
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)
    if mn < 50000000:
        trows,tcols = pattern.shape[:2]
        pyautogui.click(mnLoc[0]+(tcols/2), mnLoc[1]+(trows/2))




def detect():
    with mss() as sct:
        sct.shot(output="screenshot.png")
    
    cv2_detect("screenshot.png")

while True:
    detect()