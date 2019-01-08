#!/usr/bin/env python

import cv2
import numpy as np
import pywt
import math

class DWT:
    
    #def forward(i = "/tmp/i000.png", I = "/tmp/p000.png"):
    def forward(image):
        '''2D 1-iteration forward DWT of a color image.

        Input:
        -----

            image: an array[y, x, component] with a color image.

                  x
             +---------------+
             |               |-+ component
           y |               | |-+
             |               | | |
             |               | | |
             |               | | |
             |               | | |
             |               | | |
             +---------------+ | |
               +---------------+ |
                 +---------------+


        Output:
        ------

            pyramid: a tuple (L, H), where L  (low-frequencies subband) is an array[y, x, component], and H (high-frequencies subbands) is a tuple (LH, HL, HH), where LH, HL, HH are array[y, x, component], with the color pyramid.

                 x
             +-------+-------+
             |       |       |-+ component
           y |  LL   |  HL   | |-+
             |       |       | | |
             +-------+-------+ | |
             |       |       |-+ |
             |  LH   |  HH   | |-+
             |       |       | | |
             +-------+-------+ | |
               +-------+-------+ |
                 +-------+-------+
        '''

        y = math.ceil(image.shape[0]/2)
        x = math.ceil(image.shape[1]/2)
        LL = np.ndarray((y, x, 3), np.float64)
        LH = np.ndarray((y, x, 3), np.float64)
        HL = np.ndarray((y, x, 3), np.float64)
        HH = np.ndarray((y, x, 3), np.float64)
        for c in range(3):
            (LL[:,:,c], (LH[:,:,c], HL[:,:,c], HH[:,:,c])) = pywt.dwt2(image[:,:,c], 'db5', mode='per')

        pyramid = (LL, (LH, HL, HH))
        return pyramid

    #def backward(I = "/tmp/p000.png", i = "/tmp/i000.png"):
    def backward(pyramid):
        '''2D 1-iteration inverse DWT of a color pyramid.

        Input:
        -----

            pyramid: the input pyramid (see forward transform).

        Output:
        ------

            image: the inversely transformed image (see forward transform).
        '''

        LL = pyramid[0]
        LH = pyramid[1][0]
        HL = pyramid[1][1]
        HH = pyramid[1][2]
        image = np.ndarray((LL.shape[0]*2, LL.shape[1]*2, 3), np.float64)
        for c in range(3):
            frame[:,:,c] = pywt.idwt2((LL[:,:,c], (LH[:,:,c], HL[:,:,c], HH[:,:,c])), 'db5', mode='per')
        return image

if __main__:

    import argparse

    parser = argparse.ArgumentParser(
        description = "2D Discrete Wavelet (color) Transform")

    parser.add_argument("-b", "--backward",
                        help="Backward transform")

    parser.add_argument("-i", "--image",
                        help="Image to be transformed", default="/tmp/i000.png")

    parser.add_argument("-p", "--pyramid",
                        help="Pyramid to be transformed", default="/tmp/p000.png")

    args = parser.parse_args()

    d = DWT()
    if args.backward:
        p = pyramid.read("{}".format(args.pyramid))
        i = d.backward(p)
        image.write("{}".format(args.image))
    else:
        i = image.read("{}".format(args.image))
        p = d.forward(i)
        pyramid.write("{}".format(args.pyramid))
