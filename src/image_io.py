import cv2
import numpy as np

class InputFileException(Exception):
    pass

class ImageReader:
    '''Read 16-bit PNG images from disk.
    
    Images must be enumerated (image000.png, image001.png, ...).

    '''

    def __init__(self):
        '''Default constructor.

        Parameters
        ----------

            None.

        Returns
        -------

            None.

        '''
        pass

    def read(self, number, path='../images/'):
        '''Read an image from disk.

        Parameters
        ----------

            number : int.

                Index of the image in the sequence.

            path : str.

                Image path.

        Returns
        -------

            [:,:,:].

                A color image.

        '''

        file_name = '{}{:03d}.png'.format(path, number)
        image = cv2.imread(file_name, -1).astype(np.float64)
        if image is None:
            raise InputFileException('{} not found'.format(file_name))
        else:
            image -= 32768
            assert (np.amax(image) < 32767), 'range overflow'
            assert (np.amin(image) >= -32768), 'range underflow'
            return image

class ImageWritter:
    '''Write 16-bit PNG images to disk.

    Images should be enumerated (image000.png, image001.png, ...).

    '''

    def __init__(self):
        '''Default constructor.

        Parameters
        ----------

            None.

        Returns
        -------

            None.

        '''
        pass

    def write(self, image, number=0, path='/tmp/'):
        '''Write an image to disk.

        Parameters
        ----------

            image : [:,:,:].

                The color image to write.

            number : int.

                Index of the image in the sequence.

            path : str.

                Path to the image.

        Returns
        -------

            None.

        '''

        file_name = '{}{:03d}.png'.format(path, number)

        tmp = np.copy(image)
        tmp += 32768
        
        assert (np.amax(tmp) < 65536), '16 bit unsigned int range overflow'
        assert (np.amin(tmp) >= 0), '16 bit unsigned int range underflow'
        
        cv2.imwrite(file_name, np.rint(tmp).astype(np.uint16))
        #cv2.imwrite(file_name, tmp.astype(np.uint16))