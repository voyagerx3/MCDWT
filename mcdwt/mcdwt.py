import cv2
import numpy as np
import pywt
import math

from motion import motion_compensation

def _2D_DWT(image):
    '''2D DWT of a color image.

    Arguments
    ---------

        image : [:,:,:].

            A color frame.

    Returns
    -------

        (L,H) where L=[:,:,:] and H=(LH,HL,HH), where LH,HL,HH=[:,:,:].

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

    return (LL, (LH, HL, HH))

def _2D_iDWT(L, H):
    '''2D 1-iteration inverse DWT of a color pyramid.

    Arguments
    ---------

        L : [:,:,:].

            Low-frequency color subband.

        H : (LH, HL, HH), where LH,HL,HH=[:,:,:].

            High-frequency color subbands.

    Returns
    -------

        [:,:,:].

            A color frame.

    '''

    LH = H[0]
    HL = H[1]
    HH = H[2]
    frame = np.ndarray((L.shape[0]*2, L.shape[1]*2, 3), np.float64)
    for c in range(3):
        frame[:,:,c] = pywt.idwt2((L[:,:,c], (LH[:,:,c], HL[:,:,c], HH[:,:,c])), 'db5', mode='per')
    return frame

class InputFileException(Exception):
    pass

class ImageReader:
    '''Read PNG images from disk.
    
    Images must be enumerated. Example: "image000.png, image001.png,
    ..."

    '''

    def __init__(self):
        pass

    def set_path(self, path='../input/image'):
        '''Set up the path where the images are.

        Parameters
        ----------

            path : str

                The image path (directory and file prefix). Example:
                '../input/image'.

        Returns
        -------

            None.

        '''

        self.path = path 

    def read(self, number):
        '''Read an image from disk.

        Parameters
        ----------

            number : int.

                Index of the image in the sequence.

        Returns
        -------

            [:,:,:].

                A color image.

        '''

        file_name = '{}{:03d}.png'.format(self.path, number)
        image = cv2.imread(file_name)
        if image is None:
            raise InputFileException('{} not found'.format(file_name))
        else:
            return image

class ImageWritter:
    '''Write PNG images to disk.

    Images should be enumerated. Example: "image000.png, image001.png, ..."

    '''

    def __init__(self):
        pass

    def set_path(self, path='../output/'):
        '''Set up the path where the images will be.

        Parameters
        ----------

            path : str

                The image path (directory and file prefix). Example:
                '../output/image'.

        Returns
        -------

            None.

        '''

        self.path = path 

    def write(self, image, number=0):
        '''Write an image to disk.

        Parameters
        ----------

            image : [:,:,:].

                The color image to write.

            number : int.

                Index of the image in the sequence.

        Returns
        -------

            None.

        '''

        file_name = '{}{:03d}.png'.format(self.path, number)
        cv2.imwrite(file_name, image)

class PyramidReader:
    '''Read PNG pyramids from disk.

    Pyramids should be enumerated. Example: "pyramid000.png,
    pyramid001.png, ..."

    '''

    def __init__(self):
        pass

    def set_path(self, path='../input/'):
        '''Set up the path where the pyramids are.

        Parameters
        ----------

            path : str

                The pyramid path (directory and file prefix). Example:
                '../input/pyramid'.

        Returns
        -------

            None.

        '''

        self.path = path 

    def read(self, number):
        '''Read a pyramid from disk.

        Parameters
        ----------

            number : int.

                Index of the pyramid in the sequence.

        Returns
        -------

            (L,H) where L=[:,:,:] and H=(LH,HL,HH), where LH,HL,HH=[:,:,:].

                A color pyramid.

        '''

        file_name = '{}{:03d}.png'.format(self.path, number)
        buf = cv2.imread(file_name)
        if buf is None:
            raise InputFileException('{} not found'.format(file_name))
        else:
            y = math.ceil(buf.shape[0]/2)
            x = math.ceil(buf.shape[1]/2)
            LL = buf[0:y,0:x,:]
            LH = buf[0:y,x:buf.shape[1],:]
            HL = buf[y:buf.shape[0],0:x,:]
            HH = buf[y:buf.shape[0],x:buf.shape[1],:]
            return (LL, (LH, HL, HH))

class PyramidWritter:
    '''Write PNG pyramids to disk.

    Pyramids must be enumerated. Example: "pyramid000.png,
    pyramid001.png, ..."

    '''

    def __init__(self):
        pass

    def set_path(self, path='../output/'):
        '''Set up the path where the pyramids are.

        Parameters
        ----------

            path : str

                The pyramid path (directory and file prefix). Example:
                '../output/pyramid'.

        Returns
        -------

            None.

        '''

        self.path = path 

    def write(self, pyramid, number=0):
        '''Write a pyramid to disk.

        Parameters
        ----------

            L : [:,:,:].

                LL subband.

            H : (LH, HL, HH), where LH,HL,HH=[:,:,:].

                H subbands.

            number : int.

                Index of the pyramid in the sequence.

        Returns
        -------

            None.

        '''
        file_name = '{}{:03d}.png'.format(self.path, number)
        #import ipdb; ipdb.set_trace()
        LL = pyramid[0]
        LH = pyramid[1][0]
        HL = pyramid[1][1]
        HH = pyramid[1][2]
        y = LL.shape[0]
        x = LL.shape[1]
        buf = np.ndarray((y*2, x*2, 3), np.float64)
        buf[0:y,0:x,:] = LL
        buf[0:y,x:x*2,:] = LH
        buf[y:y*2,0:x,:] = HL
        buf[y:y*2,x:x*2,:] = HH
        cv2.imwrite(file_name, buf)

def MCDWT(input = '../input/', output='../output/', n=5, l=2):
    '''A Motion Compensated Discrete Wavelet Transform.

    Compute the 1D-DWT along motion trajectories. The input video (as
    a sequence of images) must be stored in disk (<input> directory)
    and the output (as a sequence of DWT coefficients that are called
    pyramids) will be stored in disk (<output> directory). So, this
    MCDWT implementation does not transform the video on the fly.

    Arguments
    ---------

        input : str

            Path where the input images are. Example:
            "../input/image".

        output : str

            Path where the (transformed) pyramids will be. Example:
            "../output/pyramid".

         n : int

            Number of images to process.

         l : int

            Number of leves of the MCDWT (temporal scales). Controls
            the GOP size. Examples: `l`=0 -> GOP_size = 1, `l`=1 ->
            GOP_size = 2, `l`=2 -> GOP_size = 4. etc.

    Returns
    -------

        None.

    '''
    ir = ImageReader()
    iw = ImageWritter()
    pw = PyramidWritter()
    ir.set_path(input)
    iw.set_path(output)
    pw.set_path(output)
    x = 2
    for j in range(l): # Number of temporal scales
        #import ipdb; ipdb.set_trace()
        A = ir.read(0)
        tmpA = _2D_DWT(A)
        L_y = tmpA[0].shape[0]
        L_x = tmpA[0].shape[1]
        pw.write(tmpA, 0)        
        zero_L = np.zeros(tmpA[0].shape, np.uint8)
        zero_H = (zero_L, zero_L, zero_L)
        AL = _2D_iDWT(tmpA[0], zero_H)
        #iw.write(AL, 1)
        AH = _2D_iDWT(zero_L, tmpA[1])
        #iw.write(AH, 1)
        i = 0
        while i < (n//x):
            B = ir.read(x*i+x//2)
            tmpB = _2D_DWT(B)
            BL = _2D_iDWT(tmpB[0], zero_H)
            BH = _2D_iDWT(zero_L, tmpB[1])
            C = ir.read(x*i+x)
            tmpC = _2D_DWT(C)
            pw.write(tmpC, x*i+x)
            CL = _2D_iDWT(tmpC[0], zero_H)
            CH = _2D_iDWT(zero_L, tmpC[1])
            BHA = motion_compensation(BL, AL, AH)
            BHC = motion_compensation(BL, CL, CH)
            rBH = BH - (BHA + BHC) / 2
            rBH = _2D_DWT(rBH)
            #import ipdb; ipdb.set_trace()
            rBH[0][0:L_y,0:L_x,:] = tmpB[0]
            pw.write(rBH, x*i+x//2)
            AL = CL
            AH = CH
            i += 1
            print('i =', i)
        x *= 2

def iMCDWT(input = '../input/', output='../output/', n=5, l=2):
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

         n : int

            Number of pyramids to process.

         l : int

            Number of leves of the MCDWT (temporal scales). Controls
            the GOP size. Examples: `l`=0 -> GOP_size = 1, `l`=1 ->
            GOP_size = 2, `l`=2 -> GOP_size = 4. etc.

    Returns
    -------

        None.

    '''
    ir = ImageReader()
    iw = ImageWritter()
    pr = PyramidReader()
    ir.set_path(input)
    iw.set_path(output)
    pr.set_path(input)
    x = 2**l
    for j in range(l): # Number of temporal scales
        #import ipdb; ipdb.set_trace()
        A = pr.read(0)
        zero_L = np.zeros(A[0].shape, np.uint8)
        zero_H = (zero_L, zero_L, zero_L)
        AL = _2D_iDWT(A[0], zero_H)
        AH = _2D_iDWT(zero_L, A[1])
        A = AL + AH
        iw.write(A, 0)
        i = 0
        while i < (n//x):
            B = pr.read(x*i+x//2)
            BL = _2D_iDWT(B[0], zero_H)
            rBH = _2D_iDWT(zero_L, B[1])
            C = pr.read(x*i+x)
            CL = _2D_iDWT(C[0], zero_H)
            CH = _2D_iDWT(zero_L, C[1])
            C = CL + CH
            iw.write(C, x*i+x)
            BHA = motion_compensation(BL, AL, AH)
            BHC = motion_compensation(BL, CL, CH)
            BH = rBH + (BHA + BHC) / 2
            B = BL + BH
            iw.write(B, x*i+x//2)
            AL = CL
            AH = CH
            i += 1
            print('i =', i)
        x //= 2

MCDWT('../input/','/tmp/',5,1)
iMCDWT('/tmp/','/tmp/res',5,1)
