#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--delay", type=int, default=30, help=" Time delay, defaults to 30 ms")
    parser.add_argument("-w", "--webcam", type=int, default=0, help=" Webcam channel (machine-dependent), defaults to 0")
    parser.add_argument("-v", "--video", type=str, default=None, help=" Path to input video")
    parser.add_argument("-t", "--threshold", type=np.uint8, default=np.uint8(100), help=" Threshold for red shades")

    args = parser.parse_args()
    if args.video is None:
        source= args.webcam # use webcam
    else:
        source= args.video # use video
    delay = args.delay
    cap = args.threshold

    captSource = cv.VideoCapture(source)
    framenum = -1 # Frame counter
    if not captSource.isOpened():
        print("Could not open the video device on channel #" + str(source))
        sys.exit(-1)
    srcS = (int(captSource.get(cv.CAP_PROP_FRAME_WIDTH)), int(captSource.get(cv.CAP_PROP_FRAME_HEIGHT)))
    print("Source size: " + str(srcS))

    WIN_SRC = "Source"
    cv.namedWindow(WIN_SRC, cv.WINDOW_AUTOSIZE)

    cv.moveWindow(WIN_SRC, 400, 0) #750,  2 (bernat =0)

    print("Reference frame resolution: Width={} Height={} of nr#: {}".format(srcS[0], srcS[1],
                                                                             captSource.get(cv.CAP_PROP_FRAME_COUNT)))

    # creating lut
    identity = np.arange(256, dtype = np.dtype('uint8'))
    identity_capped = np.arange(cap, dtype = np.dtype('uint8'))
    identity_capped = np.pad(identity_capped,(0,256-cap),'constant',constant_values=(0,0))
    zeros = np.zeros(256, np.dtype('uint8'))
    lut = np.dstack((identity_capped, identity_capped, identity))

    while True: # Show the image captured in the window and repeat
        _, frameSource = captSource.read()
        if frameSource is None:
            print(" < < <  Game over!  > > > ")
            break
        framenum += 1

        # converting colored image to gray scale (but expressed in RGB)
        grayFrame = cv.cvtColor(frameSource, cv.COLOR_BGR2GRAY)

        grayFrameBGR = cv.cvtColor(grayFrame,cv.COLOR_GRAY2BGR)

        finalFrame = cv.LUT(grayFrameBGR, lut)

        cv.imshow(WIN_SRC, finalFrame) # showing the frame

        k = cv.waitKey(delay)
        if k == 27: # key 27 is the Esc key on the keyboard
            break
    sys.exit(0)

if __name__ == "__main__":
    main()
