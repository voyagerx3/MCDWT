#!/usr/bin/env python

import cv2
import numpy as np
import pywt
import math
import sys

sys.path.insert(0, "..")
from src.IO import image
from src.IO import pyramid

class DWT:
    
    #def forward(i = "/tmp/i000.png", I = "/tmp/p000.png"):
    def forward(self, image):
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
    def backward(self, pyramid):
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
            image[:,:,c] = pywt.idwt2((LL[:,:,c], (LH[:,:,c], HL[:,:,c], HH[:,:,c])), 'db5', mode='per')
        return image

if __name__ == "__main__":

    import argparse

    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        pass
    
    parser = argparse.ArgumentParser(
        description = "2D Discrete Wavelet (color) Transform\n\n"
        "Examples:\n\n"
        "  ./DWT.py                          <- Forward transform\n"
        "  ./DWT.py -b -i /tmp/a -p /tmp/000 <- Backward transform\n",
        formatter_class=CustomFormatter)

    parser.add_argument("-b", "--backward", action='store_true',
                        help="Performs backward transform")

    parser.add_argument("-i", "--image",
                        help="Image to be transformed", default="../sequences/stockholm/000")

    parser.add_argument("-p", "--pyramid",
                        help="Pyramid to be transformed", default="/tmp/000")

    args = parser.parse_args()

    d = DWT()
    if args.backward:
        if __debug__:
            print("Backward transform")
        p = pyramid.read("{}".format(args.pyramid))
        i = d.backward(p)
        image.write8(i, "{}".format(args.image))
    else:
        if __debug__:
            print("Forward transform")
        i = image.read("{}".format(args.image))
        p = d.forward(i)
        pyramid.write(p, "{}".format(args.pyramid))
