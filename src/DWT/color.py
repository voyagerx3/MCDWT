import cv2
import numpy as np
import pywt
import math

def forward(image):
    '''2D 1-iteration DWT of a color image.

    Input:
    -----

        image: [component,y,x].

            A color frame.

    Output:
    ------

        pyramid: (L, H), where L = [component,y,x] (low-frequencies color subband) and H = (LH,HL,HH), where LH, HL, HH: [component,y,x] (high-frequencies color subbands).

            A color pyramid.
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

def backward(pyramid):
    '''2D 1-iteration inverse DWT of a color pyramid.

    Input:
    -----

        pyramid: see forward transform.

    Output:
    ------

        image: see forward transform.
    '''

    LL = pyramid[0]
    LH = pyramid[1][0]
    HL = pyramid[1][1]
    HH = pyramid[1][2]
    image = np.ndarray((LL.shape[0]*2, LL.shape[1]*2, 3), np.float64)
    for c in range(3):
        frame[:,:,c] = pywt.idwt2((LL[:,:,c], (LH[:,:,c], HL[:,:,c], HH[:,:,c])), 'db5', mode='per')
    return image
