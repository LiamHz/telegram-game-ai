import cv2
import time
import numpy as np
from mss import mss
from PIL import Image
from pynput.keyboard import Key, Controller, Listener

nBlackThresh = 8192
bounding_box = {'top': 420, 'left': 700, 'width': 400, 'height': 130}
nPixels = bounding_box['width'] * bounding_box['height']
SAVE_IMAGES = False

sct = mss()
keyboard = Controller()
full_images = []
cropped_images = []

def main():
    try:
        while True:
            # Wait for 180 miliseconds
            time.sleep(0.18)

            # Get screen cap
            screen_cap = np.array(sct.grab(bounding_box))

            # Convert screen_cap to black and white with thresholding
            bw_img = cv2.cvtColor(screen_cap, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(bw_img, 200, 255, cv2.THRESH_BINARY)

            # Crop image to left half
            cropped_img = thresh[:, 0:bounding_box['width']//2]

            # If number of black pixels in left half is 0, move left
            nWhite = cv2.countNonZero(cropped_img)
            nBlack = nPixels - nWhite
            if nBlack < nBlackThresh:
                # Press left arrow key
                keyboard.press(Key.left)
                print("LEFT")
            else:
                # Press right arrow key
                keyboard.press(Key.right)
                print("RIGHT")

            if SAVE_IMAGES:
                cropped_images.append(cropped_img)
                full_images.append(thresh)

    except KeyboardInterrupt:
        if SAVE_IMAGES:
            for i in range(len(cropped_images)):
                print("{}-crop.bmp".format(i))
                print("{}-full.bmp".format(i))
                cv2.imwrite("./{}-crop.bmp".format(i), cropped_images[i])
                cv2.imwrite("./{}-full.bmp".format(i), full_images[i])
        cv2.destroyAllWindows()

main()
