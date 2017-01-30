import cv2
import numpy as np
import pywt

def _2D_DWT(image:[]) -> []:
    ''' 2D DWT of a color image.

    Arguments
    ---------
        image : []
            2D color frame (a list of 2D matrices) to transform.

    Returns
    -------
        A list of (LL, (LH, HL, HH)) tuples.
    '''
    pyramid = [None]*3
    for c in range(3):
        pyramid[c] = pywt.dwt2(image[:,:,c], 'db5')
    return pyramid

def _2D_iDWT(pyramid:[]) -> []:
    ''' 2D inverse DWT of a color pyramid.

    Arguments
    ---------
        pyramid : ()
            Color pyramid (tuple (LL, (LH, HL, HH)) to transform.

    Returns
    -------
        A 2D color frame (a list of 2D matrices).
    '''
    frame = [None]*3
    for c in range(3):
        frame[c] = pywt.dwt2(pyramid[:,:,c], 'db5')
    return pyramid

def L_zero(y, x) -> np.array:
    ''' Generates a matrix of (y*x) unsigned int8 zeros.

    Arguments
    ---------
        y : int
            Number of zeros in the \'y\' dimension.

        x : int
            Number of zeros in the \'x\' dimension.

    Returns
    -------
        The matrix.
    '''
    return np.zeros((y, x),np.uint8)

def H_zero(y, x):
    ''' Generates a tuple of matrices of (y*x) unsigned int8 zeros.

    Arguments
    ---------
        y : int
            Number of zeros in the \'y\' dimension of each matrix.

        x : int
            Number of zeros in the \'x\' dimension of each matrix.

    Returns
    -------
        The tuple of matrices.
    '''
    return (L_zero, L_zero, L_zero)

class InputImageException(Exception):
    pass

def MCDWT(input = 'input', output = 'output', n=5, l=2) -> None :
    '''A Motion Compensated Discrete Wavelet Transform.

    Compute the 1D-DWT along motion trajectories. The input video (as
    a sequence of images) must be stored in disk (<input> directory)
    and the output (as a sequence of DWT coefficients that are called
    pyramids) will be stored in disk (<output> directory). So, this
    MCDWT implementation does not transform the video on the fly.

    Arguments
    ---------

        input : str
            Directory of the input images that must be named
            000.png, 001.png, etc.

        output : str
            Directory fo the output (transformed) pyramids
            (named 000.png, 001.png, etc.).

         n : int
            Number of images of the input.

         l : int
            Number of leves of the MCDWT (temporal scales). Controls
            the GOP size. Examples: `l`=0 -> GOP_size = 1, `l`=1 ->
            GOP_size = 2, `l`=2 -> GOP_size = 4. etc.

    Returns
    -------
        None.

    '''
    import ipdb; ipdb.set_trace()
    x = 2
    for j in range(l): # Number of temporal scales
        image_name = '{}/{image_number:03d}.png'.format(input,image_number=0)
        image = cv2.imread(image_name)
        if image is None:
            raise InputImageException('{} not found'.format(image_name))
        tmp = _2D_DWT(image)
        AL = _2D_iDWT(tmp[0], H_zero())
        i = 0
        while i < (n//x):
            print('A = ', x*i)
            print('B = ', x*i+x//2)
            print('C = ', x*i+x)
            i += 1
            print('i = ', i)
        x *= 2
