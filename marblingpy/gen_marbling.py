#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# marblingpy: a program that generates a randomized mathematical marbling image.
# Copyright (c) 2020 Taktpixel Co.,Ltd.
# Contact: contact@taktpixel.co.jp
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import ast
import sys
from datetime import datetime
import math
import re

import cv2
import numpy as np
import argparse

PACKAGE_NAME = 'marblingpy'

__author__ = "Shinobu Yokoyama <cohomolg@gmail.com>"
__date__ = "2020/10/04 16:23:40"
# __file__="GEN_MARBLING_PY"
__credits__ = ""
with open(os.path.join(os.path.dirname(__file__), '__init__.py')) as f:
    match = re.search(r'__version__\s+=\s+(.*)', f.read())
__version__ = str(ast.literal_eval(match.group(1)))

ELEMENT_TYPE = np.uint16
MIN_THRESHOLD = 1e-8

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

def testDropCircle(img, height, width, count = 10, interpolation = 'nearest', verbose = False):
    for i in range(count):
        color = np.random.randint(0, 256, 3)
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        r = np.random.randint(10, np.min((100, np.max((10, int(np.min((width, height))/2))))))

        if (verbose):
            print('drop circle ({}/{}) : (x, y, r) = ({}, {}, {})'.format(i, count, x, y, r))

        dropCircle(img, color, (y, x), r, interpolation)

def testDrawTineLine(img, height, width, count = 2, interpolation = 'nearest', verbose = False):
    for i in range(count):
        dir1 = np.random.randint(1, height)
        dir2 = np.random.randint(1, width)
        init1 = np.random.randint(0, height)
        init2 = np.random.randint(0, width)
        shift = np.random.randint(0, np.min((width, height)) * 2)
        sharpness = np.random.randint(0, 32)

        if (verbose):
            print('tine line ({}/{}) : (x1, y1), (x2, y2), shift, sharpness = ({}, {}), ({}, {}), {}, {}' \
                    .format(i, count, dir1, dir2, init1, init2, shift, sharpness))

        drawTineLine(img, height, width, (dir1, dir2), (init1, init2), shift, sharpness, interpolation)

#
# utilities
#
def range2dCoord(width, height):
    """get range for 2D iteration

    Args:
        width (int): image width
        height (int): image height

    Returns:
        2D array: shape is (width * height, 2)
    """
    baseArr = [[x for x in range(width)]] * height
    xArr = np.stack(baseArr, axis=0).reshape((height * width,))
    yArr = np.stack(baseArr, axis=1).reshape((height * width,))
    sourceCoord = np.column_stack((xArr, yArr))
    return sourceCoord

def bilinearInterpolation(img, x, y):
    """pickup bilinear interpolated color

    Args:
        img (Mat): 3D, 3-channel color image
        x (float): floating position coordinate
        y (float): floating position coordinate

    Returns:
        value: color value
    """
    x1 = np.floor(x).astype(ELEMENT_TYPE)
    x2 = x1 + 1
    xr = x - x1
    y1 = np.floor(y).astype(ELEMENT_TYPE)
    y2 = y1 + 1
    yr = y - y1

    channel = img.shape[2]
    val = np.zeros((channel))

    xx = np.array([[1 - xr], [xr]], dtype='float32')
    yy = np.array([[1 - yr], [yr]], dtype='float32')
    f = np.array([[img[int(x1), int(y1), :], img[int(x1), int(y2), :]], [img[int(x2), int(y1), :], img[int(x2), int(y2), :]]])

    for i in range(channel):
        b = np.matmul(f[:, :, i], yy)
        v = np.matmul(xx.T, b)
        val[i] = v

    return np.around(np.array(val)).astype(ELEMENT_TYPE).reshape(channel)


#
# tool functions
#
def dropCircle(img, color, dpCoord, r, interpolation = 'nearest'):
    dpCoord = np.array(dpCoord)

    # prepare source coordinate
    h, w, _ = img.shape
    sourceCoord = range2dCoord(w, h)

    # generate pickup coordinate
    derivCoordArray = sourceCoord - dpCoord
    r_2 = r**2
    dArray_2 = np.maximum(np.power(np.linalg.norm(derivCoordArray, axis=1), 2), MIN_THRESHOLD)
    factorArray = np.sqrt(np.maximum((dArray_2 - r_2) / dArray_2, MIN_THRESHOLD))
    pickupCoord = dpCoord + np.multiply(derivCoordArray, factorArray.reshape((1, -1)).T)

    # extract
    outerIndex = np.where(dArray_2 > r_2)
    sourceCoord = sourceCoord[outerIndex]
    pickupCoord = pickupCoord[outerIndex]

    if interpolation == 'nearest':
        # for nearest neighbor
        pickupCoord = np.round(pickupCoord).astype(ELEMENT_TYPE)

        # copy spreading pixel by nearest neighbor
        img[sourceCoord[:, 0], sourceCoord[:, 1], :] = img[pickupCoord[:, 0], pickupCoord[:, 1], :]
    elif interpolation == 'bilinear':
        buf = img.copy()
        for idx in range(len(sourceCoord)):
            p = sourceCoord[idx]
            q = pickupCoord[idx]
            img[p[0], p[1], :] = bilinearInterpolation(buf, q[0], q[1])

    # cv2.circle method specifies the dropping point reverse the order (y, x)
    # instead of (x, y)
    if isinstance(color, np.ndarray):
        _color = color.tolist()
    else:
        _color = color

    cv2.circle(img, (dpCoord[1], dpCoord[0]), r, _color, -1, lineType=cv2.LINE_AA)


def drawTineLine(img, height, width, dirVector, initCoord = (0, 0), shift = 10, sharpness = 2, interpolation = 'nearest'):
    # setup variables
    initCoordArray = np.array(initCoord)

    ## dirVector must not be zero vector (i.e. !=(0,0) )
    ## because the y-axis is inverted within the pixel coordinate, y-coordinate must be multiplied by -1.
    dirVectorArray = np.array((dirVector[0], -dirVector[1]))
    normOfDirVector = np.linalg.norm(dirVectorArray)

    if normOfDirVector == 0:
        raise RuntimeError('"dirVector" must not be zero vector.')

    dirVectorUnitArray = dirVectorArray / normOfDirVector

    ## the y-axis inversion makes the normal vector be equivalent of directional vector of the tine line,
    ## if the orientation is compatible with given arguments, which suffices in this case.
    nCoordArray = np.array(dirVector)
    nCoordUnitArray = nCoordArray / np.linalg.norm(nCoordArray)

    # prepare source coordinate
    h, w, _ = img.shape
    sourceCoord = range2dCoord(w, h)

    # calculate the distance between a point and the tine line
    # note how we calculate the norm of inner product
    sourceCoordSub = np.subtract(sourceCoord, initCoordArray.reshape(-1, 1).T)
    nCoordUnitArrayMul = np.multiply(sourceCoordSub, nCoordUnitArray.reshape(-1, 1).T)
    dArray = np.abs(nCoordUnitArrayMul.sum(axis=1))
    dArray = np.maximum(dArray, MIN_THRESHOLD)

    # calculate the reverse function in order to obtain the originated point to be applied the tool function.
    reverseFactor = shift * sharpness / (dArray + sharpness)
    pickupCoord = sourceCoord - np.multiply(reverseFactor.reshape(-1, 1), dirVectorUnitArray.reshape(-1 , 1).T)
    pickupCoord = np.clip(pickupCoord, (0, 0), (width -1, height - 1))

    if interpolation == 'nearest':
        # for nearest neighbor
        pickupCoord = np.round(pickupCoord).astype(ELEMENT_TYPE)

        # copy spreading pixel by nearest neighbor
        img[sourceCoord[:, 0], sourceCoord[:, 1], :] = img[pickupCoord[:, 0], pickupCoord[:, 1], :]
    elif interpolation == 'bilinear':
        buf = img.copy()
        for idx in range(len(sourceCoord)):
            p = sourceCoord[idx]
            q = pickupCoord[idx]
            img[p[0], p[1], :] = bilinearInterpolation(buf, q[0], q[1])

def main():
    NOW = datetime.now()
    parser = argparse.ArgumentParser(prog=PACKAGE_NAME.replace('_', '-'), description='generate a randomized mathematical marbling image.')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('--init', dest='INIT', type=str, help='if given, the distortion will start based from the image (png) file', metavar='INIT')
    parser.add_argument('--save', dest='FILE', type=str, help='write generating image to FILE', metavar='FILE', default=NOW.strftime('%y%m%d%H%M%S.%f')[:-3] + '.png')
    parser.add_argument('-m', '--method', dest='METHOD', type=str, help='the tool function that applies to the image; I=ink-drop, T=tine-line.', metavar='M', choices=['I', 'T'], required=True)
    parser.add_argument('-W', '--width', dest='WIDTH', type=int, help='the width in integer of generating image file (gif)', metavar='W', default=112)
    parser.add_argument('-H', '--height', dest='HEIGHT', type=int, help='the height in integer of generating image file (gif)', metavar='H', default=112)
    parser.add_argument('--seed', dest='SEED', type=np.uint32, help='input of an unsigned integer 0 or 2^32-1 to the algorithm that generates pseudo-random numbers throughout the program. the same seed produces the same result.', metavar='SEED', default=int(datetime.timestamp(NOW)))
    parser.add_argument('--interpolation', dest='INTERPOLATION', type=str, help='pixel filling interpolation type', metavar='INTERPOLATION', default='nearest', choices=['nearest', 'bilinear'])
    parser.add_argument('--count', dest='COUNT', type=int, help='the total number of times that tool functions shall be applied to render an image', metavar='C', default=1)
    parser.add_argument('-v', '--verbose', dest='VERBOSE', action='store_true', help='show verbose message')

    args = parser.parse_args()
    width = args.WIDTH
    height = args.HEIGHT

    # set seed
    np.random.seed(args.SEED)

    # show seed if verbose option is true
    if args.VERBOSE:
        print ('Current seed: %d' % args.SEED)

    # processing
    if args.INIT != None:
        imgLoaded = cv2.imread(args.INIT, cv2.IMREAD_UNCHANGED)
        orig2DShape = imgLoaded.shape[0:2]
        width = orig2DShape[1]
        height = orig2DShape[0]

        # linearly shrink/stretches the image range for uint16 data pallet
        img = cv2.normalize(imgLoaded, dst=None, alpha=0, beta=np.max(orig2DShape) - 1, norm_type=cv2.NORM_MINMAX)
    else:
        img = np.full((height, width, 3), 255, dtype=ELEMENT_TYPE)

    if args.METHOD == 'I':
        testDropCircle(img, height, width, args.COUNT, interpolation=args.INTERPOLATION, verbose=args.VERBOSE)
    elif args.METHOD == 'T':
        testDrawTineLine(img, height, width, args.COUNT, interpolation=args.INTERPOLATION, verbose=args.VERBOSE)

    # linearly stretches the image range for uint16 display pallet
    img_scaled = cv2.normalize(img, dst=None, alpha=0, beta=2**16 - 1, norm_type=cv2.NORM_MINMAX)
    cv2.imwrite(args.FILE, img_scaled)

if __name__=='__main__':
    main()
