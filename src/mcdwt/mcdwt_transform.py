import cv2
import numpy as np
import pywt
import math

import image_io
import pyramid_io
import motion_compensation
import color_dwt

def forward(input = '../images/', output='/tmp/', N=5, S=2):
    '''A Motion Compensated Discrete Wavelet Transform.

    Compute the 1D-DWT along motion trajectories. The input video (as
    a sequence of images) must be stored in disk (<input> directory)
    and the output (as a sequence of DWT coefficients that are called
    pyramids) will be stored in disk (<output> directory).

    Arguments
    ---------

        input : str

            Path where the input images are. Example:
            "../input/image".

        output : str

            Path where the (transformed) pyramids will be. Example:
            "../output/pyramid".

         N : int

            Number of images to process.

         S : int

            Number of leves of the MCDWT (temporal scales). Controls
            the GOP size. Examples: S = 0 -> GOP_size = 1, S = 1 ->
            GOP_size = 2, S = 2 -> GOP_size = 4. etc.

    Returns
    -------

        None.

    '''
    
    #import ipdb; ipdb.set_trace()
    ir = image_io.ImageReader()
    iw = image_io.ImageWritter()
    pw = pyramid_io.PyramidWritter()
    x = 2
    for s in range(S): # Number of temporal scales
        i = 0
        A = ir.read(i, "/tmp/scale_"+str(s)+"_L")
        dwtA = color_dwt._2D_DWT(A)
        L_y = dwtA[0].shape[0]
        L_x = dwtA[0].shape[1]
        pw.write(dwtA, i, "/tmp/scale_"+str(s+1)+"_")
        zero_L = np.zeros(dwtA[0].shape, np.float64)
        zero_H = (zero_L, zero_L, zero_L)
        AL = color_dwt._2D_iDWT(dwtA[0], zero_H)
        if __debug__:
            iw.write(AL, i, "/tmp/scale_"+str(s)+"_AL_")
        AH = color_dwt._2D_iDWT(zero_L, dwtA[1])
        if __debug__:
            iw.write(AH, i, "/tmp/scale_"+str(s)+"_AH_") 
        while i < (N//x):
            B = ir.read(x*i+x//2, "/tmp/scale_"+str(s)+"_L")
            dwtB = color_dwt._2D_DWT(B)
            BL = color_dwt._2D_iDWT(dwtB[0], zero_H)
            BH = color_dwt._2D_iDWT(zero_L, dwtB[1])
            C = ir.read(x*i+x, "/tmp/scale_"+str(s)+"_L")
            dwtC = color_dwt._2D_DWT(C)
            pw.write(dwtC, x*i+x, "/tmp/scale_"+str(s+1)+"_")
            CL = color_dwt._2D_iDWT(dwtC[0], zero_H)
            CH = color_dwt._2D_iDWT(zero_L, dwtC[1])
            BHA = motion_compensation.motion_compensation(BL, AL, AH)
            BHC = motion_compensation.motion_compensation(BL, CL, CH)
            if __debug__:
                iw.write(BH, x*i+x//2, "/tmp/scale_"+str(s)+"_BH_")
            prediction = (BHA + BHC) / 2
            if __debug__:
                iw.write(prediction+128, x*i+x//2, "/tmp/scale_"+str(s)+"_prediction_")
            rBH = BH - prediction
            if __debug__:
                iw.write(rBH, x*i+x//2, "/tmp/scale_"+str(s)+"_residue_")
            rBH = color_dwt._2D_DWT(rBH)
            rBH[0][0:L_y,0:L_x,:] = dwtB[0]
            pw.write(rBH, x*i+x//2, "/tmp/scale_"+str(s+1)+"_")
            AL = CL
            AH = CH
            i += 1
            print('s = ', S, 'i =', i)
        x *= 2

def backward(input = '/tmp/', output='/tmp/', N=5, S=2):
    '''A (Inverse) Motion Compensated Discrete Wavelet Transform.

    iMCDWT is the inverse transform of MCDWT. Inputs a sequence of
    pyramids and outputs a sequence of images.

    Arguments
    ---------

        input : str

            Path where the input pyramids are. Example:
            "../input/image".

        output : str

            Path where the (inversely transformed) images will
            be. Example: "../output/pyramid".

         N : int

            Number of pyramids to process.

         S : int

            Number of leves of the MCDWT (temporal scales). Controls
            the GOP size. Examples: `l`=0 -> GOP_size = 1, `l`=1 ->
            GOP_size = 2, `l`=2 -> GOP_size = 4. etc.

    Returns
    -------

        None.

    '''
    
    #import ipdb; ipdb.set_trace()
    ir = image_io.ImageReader()
    iw = image_io.ImageWritter()
    pr = pyramid_io.PyramidReader()
    x = 2**S
    for s in range(S): # Number of temporal scales
        #import ipdb; ipdb.set_trace()
        A = pr.read(0, input)
        zero_L = np.zeros(A[0].shape, np.float64)
        zero_H = (zero_L, zero_L, zero_L)
        AL = color_dwt._2D_iDWT(A[0], zero_H)
        AH = color_dwt._2D_iDWT(zero_L, A[1])
        A = AL + AH
        iw.write(A, 0, output)
        i = 0
        while i < (N//x):
            B = pr.read(x*i+x//2, input)
            BL = color_dwt._2D_iDWT(B[0], zero_H)
            rBH = color_dwt._2D_iDWT(zero_L, B[1])
            C = pr.read(x*i+x, input)
            CL = color_dwt._2D_iDWT(C[0], zero_H)
            CH = color_dwt._2D_iDWT(zero_L, C[1])
            C = CL + CH
            iw.write(C, x*i+x, output)
            BHA = motion_compensation.motion_compensation(BL, AL, AH)
            BHC = motion_compensation.motion_compensation(BL, CL, CH)
            BH = rBH + (BHA + BHC) / 2
            B = BL + BH
            iw.write(B, x*i+x//2, output)
            AL = CL
            AH = CH
            i += 1
            print('i =', i)
        x //=2
