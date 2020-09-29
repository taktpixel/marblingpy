#!/usr/bin/python
#-*- coding:utf-8 -*-

__author__ = "Shinobu Yokoyama <cohomolg@gmail.com>"
__date__ = "2020/09/29 04:16:11"
__version__ = "$1.0$"
__file__="GEN_MARBLING_PY"
__credits__ = ""

import sys
from datetime import datetime
import cv2
import numpy as np
import math
import argparse

parser = argparse.ArgumentParser(description='generate a randomized mathematical marbling image.')
parser.add_argument('--save', dest='FILE', type=str, help='write generating image to FILE', metavar='FILE', default=datetime.now().strftime('%y%m%d%H%M%S.%f')[:-3] + '.png')
parser.add_argument('--width', dest='WIDTH', type=int, help='the width in integer of generating image file (gif)', metavar='W', default=112)
parser.add_argument('--height', dest='HEIGHT', type=int, help='the height in integer of generating image file (gif)', metavar='H', default=112)
parser.add_argument('--count', dest='COUNT', type=int, help='the total number of times that tool functions shall be applied to render an image', metavar='C', default=10)
args = parser.parse_args()

# init
expandWeight = math.sqrt(2)

def testDropCircle(img, count = args.COUNT):
    for i in range(count):
        color = np.random.randint(0, 255, 3)
        x = np.random.randint(0, args.WIDTH)
        y = np.random.randint(0, args.HEIGHT)
        r = np.random.randint(10, np.min((100, np.max((10, int(np.min((args.WIDTH, args.HEIGHT))/2))))))
        dropCircle(img, color, (x, y), r)

def dropCircle(img, color, dpCoord, r):
    # draw circle
    buf = img.copy()

    for i, row in enumerate(buf):
        for j, col in enumerate(row):
            # setup variables
            dpCoordArray = np.array(dpCoord)
            P = (i, j)
            PArray = np.array(P)

            # calculate the derivative (difference) of vector [dp, p] (turns out to be `p - dp` for a point p in loop)
            derivCoordArray = PArray - dpCoordArray

            # calculate the distance between drop-point and the relevant point
            d = np.linalg.norm(derivCoordArray)

            # skip if the point is within the dropping area or it has new painted
            if d < r:
                continue
            else:
                origCoordArray = dpCoordArray + derivCoordArray * math.sqrt(1 - r**2 / d**2)

                # the point seems to be warped by the last ink-drop transformation,
                # in case the point can be seen as transfered out inside
                # the painting circle, then paint with the dropping color.
                try:
                    Q = tuple(np.uint8(origCoordArray))
                    img[P] = buf[Q]
                except Exception as e:
                    print (e)
                    sys.exit(1)

    # cv2.circle method specifies the dropping point reverse the order (y, x)
    # instead of (x, y)
    cv2.circle(img, (dpCoord[1], dpCoord[0]), r, color.tolist(), -1, lineType=cv2.LINE_AA)

if __name__=='__main__':
    img = np.full((args.WIDTH, args.HEIGHT, 3), 255, dtype=np.uint8)
    testDropCircle(img)
    cv2.imwrite(args.FILE, img)
