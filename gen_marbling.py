#!/usr/bin/env python
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

#
# test functions
#
def testGetRandomIntDivision(n, div, divList = []):
    s = np.random.randint(0, n + 1)
    divList.append(s)

    if div - 2 <= 0:
        divList.append(n - s)
        return divList

    return testGetRandomIntDivision(n - s, div - 1, divList)

def testDropCircle(img, count = 10):
    for i in range(count):
        color = np.random.randint(0, 255, 3)
        x = np.random.randint(0, args.WIDTH)
        y = np.random.randint(0, args.HEIGHT)
        r = np.random.randint(10, np.min((100, np.max((10, int(np.min((args.WIDTH, args.HEIGHT))/2))))))
        dropCircle(img, color, (x, y), r)

def testDrawTineLine(img, count = 2):
    for i in range(count):
        dir1 = np.random.randint(0, args.WIDTH)
        dir2 = np.random.randint(0, args.HEIGHT)
        init1 = np.random.randint(0, args.WIDTH)
        init2 = np.random.randint(0, args.HEIGHT)
        shift = np.random.randint(0, args.HEIGHT * 2)
        sharpness = np.random.randint(0, 32)

        drawTineLine(img, (dir1, dir2), (init1, init2), shift, sharpness)

#
# tool functions
#
def dropCircle(img, color, dpCoord, r):
    # keep buf unchaged for reference
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

            # skip if the point is within the dropping area or it has never painted
            if d < r:
                continue
            else:
                origCoordArray = dpCoordArray + derivCoordArray * math.sqrt(1 - r**2 / d**2)

                try:
                    Q = tuple(np.uint8(origCoordArray))
                    img[P] = buf[Q]
                except Exception as e:
                    print (e)
                    sys.exit(1)

    # cv2.circle method specifies the dropping point reverse the order (y, x)
    # instead of (x, y)
    if isinstance(color, np.ndarray):
        _color = color.tolist()
    else:
        _color = color

    cv2.circle(img, (dpCoord[1], dpCoord[0]), r, _color, -1, lineType=cv2.LINE_AA)

def drawTineLine(img, dirVector, initCoord = (0, 0), shift = 10, sharpness = 10):
    # keep buf unchaged for reference
    buf = img.copy()
    distortCount = 0
    for i, row in enumerate(buf):
        for j, col in enumerate(row):
            # setup variables
            initCoordArray = np.array(initCoord)

            ## because the y-axis is inverted within the pixel coordinate, y-coordinate must be multiplied by -1.
            dirVectorArray = np.array((dirVector[0], -dirVector[1]))
            dirVectorUnitArray = dirVectorArray / np.linalg.norm(dirVectorArray)

            ## the y-axis inversion makes the normal vector be equivalent of directional vector of the tine line,
            ## if the orientation is compatible with given arguments, which suffices in this case.
            NCoord = dirVector
            NCoordArray = np.array(NCoord)
            NCoordUnitArray = NCoordArray / np.linalg.norm(NCoordArray)

            P = (i, j)
            PArray = np.array(P)

            # calculate the distance between a point and the tine line
            # note how we calculate the norm of inner product
            d = np.linalg.norm(((PArray - initCoordArray) * NCoordUnitArray).sum())

            # calculate the reverse function in order to obtain the originated point to be applied the tool function.
            origCoordArray = PArray - shift * sharpness / (d + sharpness) * dirVectorUnitArray

            # the originated point, thought of as warped into the current position, may sometimes become out the bound
            # of the pallet. So we need work-around to fill the gap of `no point to be warped from`.
            # Specular reflection (鏡面反射) method
            if origCoordArray[0] > args.WIDTH:
                origCoordArray[0] = args.WIDTH - 1
                distortCount += 1
            elif origCoordArray[0] < 0:
                origCoordArray[0] = 0
                distortCount += 1
            if origCoordArray[1] > args.HEIGHT:
                origCoordArray[1] = args.HEIGHT - 1
                distortCount += 1
            elif origCoordArray[1] < 0:
                origCoordArray[1] = 0
                distortCount += 1

            try:
                Q = tuple(np.uint8(origCoordArray))
                img[P] = buf[Q]
            except Exception as e:
                print (e)
                sys.exit(1)

if __name__=='__main__':
    img = np.full((args.WIDTH, args.HEIGHT, 3), 255, dtype=np.uint8)
    testDropCircle(img, 10)
    testDrawTineLine(img, 2)
    cv2.imwrite(args.FILE, img)
