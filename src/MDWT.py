#!/usr/bin/env python

# Note: swap the above line with the following two ones to switch
# between the standar and the optimized mode.

#!/bin/sh
''''exec python3 -O -- "$0" ${1+"$@"} # '''

import sys

from DWT import DWT
sys.path.insert(0, "..")
from src.IO import image
from src.IO import pyramid

class MDWT:

    def __init__(self):
        self.dwt = DWT()

    def forward(self, s="/tmp/stockholm/", S="/tmp/stockholm_", N=5):
        ''' Motion 1-iteration forward 2D DWT of a sequence of images.

        Compute the 2D-DWT of each image of the sequence s.

        Input:
        -----

            s: the sequence of images to be transformed.

        Output:
        ------

            S: the sequence of pyramids (transformed images).

        '''
        for i in range(N):
            img = image.read("{}{:03d}".format(s, i))
            pyr = self.dwt.forward(img)
            pyramid.write(pyr, "{}{:03d}".format(S, i))
    #    S = Sequence()
    #    for image in s:
    #        S.append(DWT(image))
    #    return S

    def backward(self, S="/tmp/stockholm_", s="/tmp/stockholm_", N=5):
        ''' Motion 1-iteration forward 2D DWT of a sequence of pyramids.

        Compute the inverse 2D-DWT of each pyramid of the sequence S.

        Input:
        -----

            S: the sequence of pyramids to be transformed.

        Output:
        ------

            s: the sequence of images.

        '''

        for i in range(N):
            pyr = pyramid.read("{}{:03d}".format(S, i))
            img = self.dwt.backward(pyr)
            image.write8(img, "{}{:03d}".format(s, i))

    #    s = []
    #    for pyramid in S:
    #        s.append(iDWT(pyramid))
    #    return s

if __name__ == "__main__":

    import argparse

    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        pass
    
    parser = argparse.ArgumentParser(
        description = "Motion 2D Discrete Wavelet (color) Transform\n\n"
        "Examples:\n\n"
        "  cp -rf ../sequences/stockholm/ /tmp/\n"
        "  ./MDWT.py    -i /tmp/stockholm/ -p /tmp/stockholm_ # Forward transform\n"
        "  ./MDWT.py -b -i /tmp/stockholm_ -p /tmp/stockholm_ # Backward transform\n",
        formatter_class=CustomFormatter)

    parser.add_argument("-b", "--backward", action='store_true',
                        help="Performs backward transform")

    parser.add_argument("-i", "--images",
                        help="Sequence of images", default="/tmp/stockholm/")

    parser.add_argument("-p", "--pyramids",
                        help="Sequence of pyramids", default="/tmp/stockholm_")

    parser.add_argument("-N",
                        help="Number of images/pyramids", default=5, type=int)

    args = parser.parse_args()

    d = MDWT()
    if args.backward:
        if __debug__:
            print("Backward transform")
        d.backward(args.pyramids, args.images, args.N)
    else:
        if __debug__:
            print("Forward transform")
        p = d.forward(args.images, args.pyramids, args.N)
