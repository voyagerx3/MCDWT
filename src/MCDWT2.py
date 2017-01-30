import cv2
import numpy as np
import pywt

def _2D_DWT(image):
    '''2D DWT of a color image.

    Arguments
    ---------

        image : [y,x,c].

            A color frame.

    Returns
    -------

        (L,H) where L=[y,x,c] and H=(LH, HL, HH) where LH,HL,HH=[y,x,c].

            A color pyramid.

    '''

    y = ceil(image.shape[0]/2)
    x = ceil(image.shape[1]/2)
    LL = np.ndarray(y, x, 3)
    LH = np.ndarray(y, x, 3)
    HL = np.ndarray(y, x, 3)
    HH = np.ndarray(y, x, 3)
    for c in range(3):
        (LL[:,:,c], (LH[:,:,c], HL[:,:,c], HH[:,:,c])) = pywt.dwt2(image[:,:,c], 'db5', mode='per')

    return (LL, (LH, HL, HH))

def _2D_iDWT(LL, (LH, HL, HH)):
    '''2D 1-iteration inverse DWT of a color pyramid.

    Arguments
    ---------

        subband_L : [numpy.ndarray (LL)]*3 structure.

            Low-frequency color subband.

        subbands_H : [numpy.ndarray (LH), numpy.ndarray (HL),
        numpy.ndarray (HH)]*3 structure.

            High-frequency color subbands.

    Returns
    -------

        [numpy.ndarray]*3 structure.

            A color frame.

    '''
    frame = [None]*3
    for c in range(3):
        frame[c] = pywt.idwt2((subband_L[c], subbands_H[c]), 'db5')
    return frame


class InputImageException(Exception):
    pass

class ImageReader:
    '''Read PNG images from disk.
    
    Files should be called something like: "image000.png,
    image001.png, ..."

    '''

    def __init__(self):
        pass

    def set_path(self, path='../input/image'):
        '''Set up the path where the images are.

        Parameters
        ----------

            path : str

                The image path (directory and file prefix). Example:
                'input/image'.

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

            A [numpy.ndarray]*3 structure.

        '''

        file_name = '{}{:03d}.png'.format(self.path, number)
        interlaced_image = cv2.imread(file_name)
        if interlaced_image is None:
            raise InputImageException('{} not found'.format(file_name))
        else:
            deinterlaced_image = []
            deinterlaced_image.append(interlaced_image[:,:,0])
            deinterlaced_image.append(interlaced_image[:,:,1])
            deinterlaced_image.append(interlaced_image[:,:,2])
            return deinterlaced_image

class ImageWritter:
    '''Write PNG images to disk.

    Files should be called something like: "image000.png,
    image001.png, ..."

    '''

    def __init__(self):
        pass

    def set_path(self, path='../output/'):
        '''Set up the path where the images are.

        Parameters
        ----------

            path : str

                The image path (directory and file prefix). Example:
                'output/image'.

        Returns
        -------

            None.

        '''

        self.path = path 

    def write(self, image, number=0):
        '''Write an image to disk.

        Parameters
        ----------

            image : [numpy.ndarray] * 3 structure.

                The image to write.

            number : int.

                Index of the image in the sequence.

        Returns
        -------

            A [numpy.ndarray]*3 structure.

        '''
        file_name = '{}{:03d}.png'.format(self.path, number)
        interlaced_image = np.ndarray((image[0].shape[0], image[0].shape[1], 3), np.uint8)
        interlaced_image[:,:,0] = image[0]
        interlaced_image[:,:,1] = image[1]
        interlaced_image[:,:,2] = image[2]
        cv2.imwrite(file_name, interlaced_image)

class PyramidReader:
    '''Read PNG pyramids from disk.

    Files should be called something like: "pyramid000.png,
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
                'input/pyramid'.

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

            A ([(numpy.ndarray (LL))]*3,[(numpy.ndarray (LH),
            numpy.ndarray (HL), numpy.ndarray (HH))]*3) structure.

                A color pyramid.

        '''

        file_name = '{}{:03d}.png'.format(self.path, number)
        buf = cv2.imread(file_name)
        if interlaced_pyramid is None:
            raise InputImageException('{} not found'.format(file_name))
        else:
            y = buf.shape[0]
            x = buf.shape[1]
            LL = [None]*3
            LH = [None]*3
            HL = [None]*3
            HH = [None]*3
            for c in range(3):
                LL[c] = buf[0::y//2,0::x//2,c]
                LH[c] = buf[0::y//2,x//2::x,c]
                HL[c] = buf[y//2::y,0::x//2,c]
                HH[c] = buf[y//2::y,x//2::x,c]
            return (LL, (LH, HL, HH))
            L = [None]*3
            H = [None]*3
            for c in range(3):
                

class PyramidWritter:
    '''Write PNG pyramids to disk.

    Files should be called something like: "pyramid000.png,
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
                'output/pyramid'.

        Returns
        -------

            None.

        '''

        self.path = path 

    def write(self, pyramid, number=0):
        '''Write a pyramid to disk.

        Parameters
        ----------

            pyramid : A ([(numpy.ndarray (LL))]*3,[(numpy.ndarray (LH),
            numpy.ndarray (HL), numpy.ndarray (HH))]*3) structure.

                The pyramid to write.

            number : int.

                Index of the pyramid in the sequence.

        Returns
        -------

            None.

        '''
        file_name = '{}{:03d}.png'.format(self.path, number)
        y = pyramid[0][0].shape[0]*2
        x = pyramid[0][0].shape[1]*2
        buf = np.ndarray((pyramid[0][0].shape[0]*2, pyramid[0][0].shape[1]*2, 3), np.uint8)
        buf[0::y//2,0::x//2,:] = pyramid[0][:][0] # LL, all components
        buf[0::y//2,x//2::x,:] = pyramid[1][:][0] # LH
        buf[y//2::y,0::x//2,:] = pyramid[1][:][1] # HL
        buf[y//2::y,x//2::x,:] = pyramid[1][:][2] # HH
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
    ir = ImageReader()
    iw = ImageWritter()
    ir.set_path(input)
    iw.set_path(output)
    x = 2
    for j in range(l): # Number of temporal scales
        #import ipdb; ipdb.set_trace()
        A = ir.read(0)
        tmpA = _2D_DWT(A)
        #pw.write(tmpA, 0)        
        zero = np.zeros(tmpA[0][0].shape, np.uint8)
        zero_L = [zero, zero, zero]
        zero_H = [(zero, zero, zero), (zero, zero, zero), (zero, zero, zero)]
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
            #pw.write(tmpC, x*i+x)
            CL = _2D_iDWT(tmpC[0], zero_H)
            CH = _2D_iDWT(zero_L, tmpC[1])
            BHA = AH # No ME (yet)
            BHC = CH # No ME
            rBH = BH - (BHA + BHC) / 2
            rBH = _2D_DWT(rBH)
            rBH[0] = tmpB[0]
            #pw.write(rBH, x*i+x//2)
            AL = CL
            AH = CH
            i += 1
            print('i = ', i)
        x *= 2

        def _L_zero(y, x):
    '''Generates a matrix of (\'y\' * \'x\') unsigned int8 zeros.

    Arguments
    ---------

        y : int

            Number of zeros in the Y dimension.

        x : int

            Number of zeros in the X dimension.

    Returns
    -------

        A np.array structure.

            The matrix.

    '''
    return np.zeros((y, x), np.uint8)

def _H_zero(y, x):
    ''' Generates a tuple of matrices of (\'y \'* \'x\') unsigned int8 zeros.

    Arguments
    ---------

        y : int

            Number of zeros in the Y dimension of each matrix.

        x : int

            Number of zeros in the X dimension of each matrix.

    Returns
    -------

        A (np.array, np.array, np.array) structure.

            The tuple of matrices.
    '''
    return (L_zero, L_zero, L_zero)
