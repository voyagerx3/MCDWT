import cv2
import numpy as np
import pywt

def _2D_DWT(image):
    '''2D DWT of a color image.

    Arguments
    ---------

        image : [numpy.ndarray]*3 structure.

            A color frame.

    Returns
    -------

        [(numpy.ndarray (LL), (numpy.ndarray (LH), numpy.ndarray (HL),
        numpy.ndarray (HH)))]*3 structure.
        ([(numpy.ndarray (LL))]*3,[(numpy.ndarray (LH), numpy.ndarray (HL),
        numpy.ndarray (HH))]*3) structure.

            A color pyramid.

    '''
    L = [None]*3
    H = [None]*3
    for c in range(3):
        tmp = pywt.dwt2(image[c], 'db5')
        L[c] = tmp[0]
        H[c] = tmp[1]
    return (L, H)

def _2D_iDWT(subband_L, subbands_H):
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

class InputImageException(Exception):
    pass

class ImageReader:
    '''An image reader.

    Read PNG mages from disk, which must be enumerated using 3 digits.

    '''

    def __init__(self):
        pass

    def set_path(self, path='../input/'):
        '''Set up the path where the images are.

        Parameters
        ----------

            path : str

                The image path (directory and image prefix). Example:
                'input/image'.

        Returns
        -------

            None.

        '''

        self.image_path = path 

    def read(self, image_number):
        '''Read a image from disk.

        Parameters
        ----------

            image_number : int.

                Index of the image to read.

        Returns
        -------

            A [numpy.ndarray]*3 structure.

        '''
        image_name = '{}{image_number:03d}.png'.format(self.image_path,image_number=0)
        image_interlaced = cv2.imread(image_name)
        if image_interlaced is None:
            raise InputImageException('{} not found'.format(image_name))
        else:
            deinterlaced_image = []
            deinterlaced_image.append(image_interlaced[:,:,0])
            deinterlaced_image.append(image_interlaced[:,:,1])
            deinterlaced_image.append(image_interlaced[:,:,2])
            return deinterlaced_image

class ImageWritter:
    '''An image writter.

    Write PNG images to disk, which must be enumerated using 3 digits.

    '''

    def __init__(self):
        pass

    def set_path(self, path='../output/'):
        '''Set up the path where the images are.

        Parameters
        ----------

            path : str

                The image path (directory and image prefix). Example:
                'output/image'.

        Returns
        -------

            None.

        '''

        self.image_path = path 

    def write(self, image, image_number):
        '''Write a image to disk.

        Parameters
        ----------

            image : [numpy.ndarray] * 3 structure.

                The image to write.

            image_number : int.

                Index of the image to write.

        Returns
        -------

            A 3 * 2D numpy.ndarray, one for each color component.

        '''
        image_name = '{}{image_number:03d}.png'.format(self.image_path,image_number=0)
        interlaced_image[:,:,0] = image[0]
        interlaced_image[:,:,1] = image[1]
        interlaced_image[:,:,2] = image[2]
        image_interlaced = cv2.imwrite(image_name, interlaced_image)

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
        A = ir.read(0)
        iw.write(A)
        tmp = _2D_DWT(A)
        zero = np.zeros(tmp[0][0].shape, np.uint8)
        zero_L = [zero, zero, zero]
        zero_H = [(zero, zero, zero), (zero, zero, zero), (zero, zero, zero)]
        import ipdb; ipdb.set_trace()
        AL = _2D_iDWT(tmp[0], zero_H)
        i = 0
        while i < (n//x):
            print('A = ', x*i)
            print('B = ', x*i+x//2)
            print('C = ', x*i+x)
            i += 1
            print('i = ', i)
        x *= 2
