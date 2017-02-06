import math
import cv2
import numpy as np

class InputFileException(Exception):
    pass

class PyramidReader:
    '''Read PNG pyramids from disk.

    Pyramids should be enumerated. Example: "pyramid000.png,
    pyramid001.png, ..."

    '''

    def __init__(self):
        pass

    def read(self, number=0, path='./'):
        '''Read a pyramid from disk.

        Parameters
        ----------

            number : int.

                Index of the pyramid in the sequence.

            path : str.

                Path to the pyramid.

        Returns
        -------

            (L,H) where L=[:,:,:] and H=(LH,HL,HH), where LH,HL,HH=[:,:,:].

                A color pyramid.

        '''

        file_name = '{}{:03d}L.png'.format(path, number)
        LL = cv2.imread(file_name, -1).astype('float64')
        LL -= 128
        if LL is None:
            raise InputFileException('{} not found'.format(file_name))
        file_name = '{}{:03d}H.png'.format(path, number)
        buf = cv2.imread(file_name, -1).astype('float64')
        if buf is None:
            raise InputFileException('{} not found'.format(file_name))
        else:
            y = math.ceil(buf.shape[0]/2)
            x = math.ceil(buf.shape[1]/2)
            LH = buf[0:y,x:buf.shape[1],:]
            LH -= 128
            HL = buf[y:buf.shape[0],0:x,:]
            HL -= 128
            HH = buf[y:buf.shape[0],x:buf.shape[1],:]
            HH -= 128
            return (LL, (LH, HL, HH))
        
class PyramidWritter:
    '''Write PNG pyramids to disk.

    Pyramids must be enumerated. Example: "pyramid000{L|H}.png,
    pyramid001{L|H}.png, ...", being 'L' used for the low-frequency
    subband LL and H for the subbands LH, HL and HH.

    '''

    def __init__(self):
        pass

    def write(self, pyramid, number=0, path='./'):
        '''Write a pyramid to disk.

        Parameters
        ----------

            L : [:,:,:].

                LL subband.

            H : (LH, HL, HH), where LH,HL,HH=[:,:,:].

                H subbands.

            number : int.

                Index of the pyramid in the sequence.

            path : str.

                Path to the pyramid.

        Returns
        -------

            None.

        '''
        #import ipdb; ipdb.set_trace()
        file_name = '{}{:03d}L.png'.format(path, number)
        LL = pyramid[0]
        LL += 128
        LL = LL.astype('uint16')
        cv2.imwrite(file_name, LL)
        y = pyramid[0].shape[0]
        x = pyramid[0].shape[1]
        buf = np.full((y*2, x*2, 3), 32768, np.uint16)
        #buf[0:y,x:x*2,:] = np.round(pyramid[1][0] + 128)
        #buf[y:y*2,0:x,:] = np.round(pyramid[1][1] + 128)
        #buf[y:y*2,x:x*2,:] = np.round(pyramid[1][2] + 128)
        LH = pyramid[1][0] + 128
        buf[0:y,x:x*2,:] = LH.astype('uint16')
        HL = pyramid[1][1] + 128
        buf[y:y*2,0:x,:]= HL.astype('uint16')
        HH = pyramid[1][2] + 128
        buf[y:y*2,x:x*2,:] = HH.astype('uint16')
        file_name = '{}{:03d}H.png'.format(path, number)
        cv2.imwrite(file_name, buf)
