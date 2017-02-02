#!/usr/bin/env python3

import numpy as np
import cv2
import pywt
import argparse

parser = argparse.ArgumentParser(description='video cam recorder')
parser.add_argument('--width', dest='width', help='width', required=True)
parser.add_argument('--height', dest='height', help='height', required=True)
parser.add_argument('--fps', dest='fps', help='fps', required=True)
parser.add_argument('--out', dest='out', help='out', required=True)
args = parser.parse_args()

width = int(args.width)
height = int(args.height)

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(args.out ,fourcc, float(args.fps), (width, height), False)

l = 1

cache = []
first_time = True

def motion_estimation(src, dest, base):
    return base

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        coeff = pywt.dwt2(frame, "haar")
        ll = coeff[0]
        hl = coeff[1][0]
        lh = coeff[1][1]
        hh = coeff[1][2]
        zero_quarter = np.zeros((height//2, width//2), dtype="float64")
        #generate dwt
        dwt = np.zeros((height, width), dtype="float64")
        dwt[0:height//2, 0:width//2] = ll
        dwt[0:height//2, width//2:width] = hl
        dwt[height//2:height, 0:width//2] = lh
        dwt[height//2:height, width//2:width] = hh
        # generate AL
        AL = pywt.idwt2((coeff[0], (zero_quarter, zero_quarter, zero_quarter)), "haar")
        # generate AH
        AH  = pywt.idwt2((zero_quarter, coeff[1]), "haar")
        if len(cache) == 2*l*3:
            # process
            BAH = motion_estimation(cache[1], cache[4], cache[2])
            BCH = motion_estimation(AL, cache[4], AH)
            residuo = cache[5] - (BAH + BCH)/2
            residuo_coeff = pywt.dwt2(residuo, "haar")
            rll = residuo_coeff[0]
            rhl = residuo_coeff[1][0]
            rlh = residuo_coeff[1][1]
            rhh = residuo_coeff[1][2]
            print(rll.max())
            rdwt = np.zeros((height, width), dtype="float64")
            rdwt[0:height//2, 0:width//2] = cache[3][0:height//2, 0:width//2]
            rdwt[0:height//2, width//2:width] = rhl
            rdwt[height//2:height, 0:width//2] = rlh
            rdwt[height//2:height, width//2:width] = rhh
            
            out.write(cv2.convertScaleAbs(np.uint16(rdwt)))
            out.write(cv2.convertScaleAbs(np.uint16(dwt)))

            # clean cache
            cache = []
         
        cache.append(dwt)
        cache.append(AL)
        cache.append(AH)

        if first_time:
            out.write(cv2.convertScaleAbs(np.uint16(dwt)))
            first_time = False
    else:
        break
out.release()
