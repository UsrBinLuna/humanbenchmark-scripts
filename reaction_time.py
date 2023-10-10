import pyautogui
from mss import mss
import cv2
import tempfile
from time import sleep

def detectColor(image, x, y):
    image = cv2.imread(image)
    pixel_color = image[y, x]
    pixel_color_rgb = (pixel_color[2], pixel_color[1], pixel_color[0])
    if (pixel_color_rgb[0], pixel_color_rgb[1], pixel_color_rgb[2]) == (75, 219, 106):
        return True


def detect(x, y):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        with mss() as sct:
            screenshot_path = temp_file.name
            screen = sct.shot(output=screenshot_path)  

    if detectColor(screen, x, y) == True:
        return True


# program loop
while True:
    x, y = pyautogui.position()
    status = detect(x, y)

    if status is True:
        pyautogui.leftClick()
        print("Is green!")
        sleep(0.1)
        pyautogui.leftClick()

