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

            A color pyramid.

    '''
    pyramid = []
    for component in image:
        pyramid.append(pywt.dwt2(component, 'db5'))
    return pyramid

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
    frame = []
    for component in pyramid:
        frame.append(pywt.idwt2(component, 'db5'))
    return frame

def L_zero(y, x):
    '''Generates a matrix of (y * x) unsigned int8 zeros.

    Arguments
    ---------

        y : int

            Number of zeros in the \'y\' dimension.

        x : int

            Number of zeros in the \'x\' dimension.

    Returns
    -------

        A np.array structure.

            The matrix.

    '''
    return np.zeros((y, x), np.uint8)

def H_zero(y, x):
    ''' Generates a tuple of matrices of (y * x) unsigned int8 zeros.

    Arguments
    ---------

        y : int

            Number of zeros in the \'y\' dimension of each matrix.

        x : int

            Number of zeros in the \'x\' dimension of each matrix.

    Returns
    -------

        A (np.array, np.array, np.array) structure.

            The tuple of matrices.
    '''
    return (L_zero, L_zero, L_zero)

class InputImageException(Exception):
    pass

class ImageReader:
    '''A image handler.

    Helps to read the images from disk, which must be enumerated using
    3 digits.
    '''

    def __init__(self):
        '''ImageReader constructor.'''
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

            image: a string with the path to the image in disk.

        Returns
        -------

            A 3 * 2D numpy.ndarray, one for each color component.

        '''
        image_name = '{}{image_number:03d}.png'.format(self.image_path,image_number=0)
        image_interlaced = cv2.imread(image_name)
        if image is None:
            raise InputImageException('{} not found'.format(image_name))
        else:
            deinterlaced_image = []
            deinterlaced_image.append(image[:,:,0])
            deinterlaced_image.append(image[:,:,1])
            deinterlaced_image.append(image[:,:,2])
            return deinterlaced_image

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
    ir.set_path(input)
    x = 2
    for j in range(l): # Number of temporal scales
        tmp = _2D_DWT(ir.read(0))
        import ipdb; ipdb.set_trace()
        AL = _2D_iDWT(tmp[:][0], H_zero(tmp[:][0].shape))
        i = 0
        while i < (n//x):
            print('A = ', x*i)
            print('B = ', x*i+x//2)
            print('C = ', x*i+x)
            i += 1
            print('i = ', i)
        x *= 2
