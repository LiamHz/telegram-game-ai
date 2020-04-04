import cv2
import time
import numpy as np
from mss import mss
from PIL import Image
from pynput.mouse import Button, Controller

bounding_box = {'top': 500, 'left': 575, 'width': 400, 'height': 325}
nPixels = bounding_box['width'] * bounding_box['height']
SAVE_IMAGES = False

sct = mss()
mouse = Controller()
full_images = []
og_images = []

def main():
    time.sleep(1)
    try:
        while True:
            # Get screen cap
            screen_cap = np.array(sct.grab(bounding_box))

            # Convert screen_cap to black and white with thresholding
            bw_img = cv2.cvtColor(screen_cap, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(bw_img, 16, 255, cv2.THRESH_BINARY)

            # Invert colors
            thresh = cv2.bitwise_not(thresh)

            # Erode and dilate soccer ball to preserve only center
            kernel = np.ones((8, 8), np.uint8)
            thresh = cv2.erode(thresh, kernel, iterations=5)

            # Get location in numpy array of white pixel (center of ball)
            location_info = np.nonzero(thresh == 255)

            if len(location_info[0]) > 0:
                ball_local_xpos = location_info[1][0]
                ball_local_ypos = location_info[0][0]

                ball_global_xpos = ball_local_xpos // 2 + bounding_box['left']
                ball_global_ypos = ball_local_ypos // 2 + bounding_box['top']
                print("X: {}, Y: {}".format(ball_global_xpos, ball_global_ypos))

                mouse.position = (ball_global_xpos, ball_global_ypos)
                mouse.press(Button.left)
                mouse.release(Button.left)

            if SAVE_IMAGES:
                og_images.append(screen_cap)
                full_images.append(thresh)

    except KeyboardInterrupt:
        if SAVE_IMAGES:
            for i in range(len(full_images)):
                print("{}-og.bmp".format(i))
                print("{}-full.bmp".format(i))
                cv2.imwrite("./{}-og.bmp".format(i), og_images[i])
                cv2.imwrite("./{}-full.bmp".format(i), full_images[i])
        cv2.destroyAllWindows()

main()
