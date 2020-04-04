import cv2
import time
import numpy as np
from mss import mss
from PIL import Image
from pynput.keyboard import Key, Controller

DELAY0 = 0.16
DELAY1 = 0.02
nBlackThresh = 4096
bounding_box = {'top': 130, 'left': 735, 'width': 100, 'height': 370}
nPixels = bounding_box['width'] * bounding_box['height'] * 4

sct = mss()
keyboard = Controller()
og_images = []
full_images = []
cropped_images = []

nPartitions = 4

def main():
    time.sleep(1)
    while True:
        # Wait for animations to complete before screen cap
        time.sleep(DELAY0)
        partitions = []
        command_stack = []

        # Get screen cap
        screen_cap = np.array(sct.grab(bounding_box))

        # Convert screen_cap to black and white with thresholding
        bw_img = cv2.cvtColor(screen_cap, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(bw_img, 200, 255, cv2.THRESH_BINARY)

        # Create a partition for each branch
        # Inserts from top to bottom ("stack order")
        partition_height = bounding_box['height'] // nPartitions
        for i in range(nPartitions):
            partitions.append(thresh[partition_height*i*2:partition_height*(i+1)*2, :])

        for i in range(len(partitions)):
            nWhite = cv2.countNonZero(partitions[i])
            nBlack = nPixels//nPartitions - nWhite

            # If number of black pixels in the left half of the screen is less
            # than a threshold, move left
            if nBlack < nBlackThresh:
                command_stack.append('L')
            else:
                command_stack.append('R')

        for i in range(nPartitions):
            # Delay is needed to let game handle input
            time.sleep(DELAY1)
            command = command_stack.pop()
            if command == "L":
                keyboard.press(Key.left)
                keyboard.release(Key.left)
                time.sleep(DELAY1)
                keyboard.press(Key.left)
                keyboard.release(Key.left)
            elif command == "R":
                keyboard.press(Key.right)
                keyboard.release(Key.right)
                time.sleep(DELAY1)
                keyboard.press(Key.right)
                keyboard.release(Key.right)

main()
