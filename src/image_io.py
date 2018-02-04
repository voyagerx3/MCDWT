import cv2
import numpy as np

class InputFileException(Exception):
    pass

class ImageReader:
    '''Read 16-bit PNG images from disk.
    
    Images must be enumerated (image000.png, image001.png, ...).

    '''

    def __init__(self):
        pass

    def read(self, number, path='./'):
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
        image = cv2.imread(file_name, -1)
        if image is None:
            raise InputFileException('{} not found'.format(file_name))
        else:
            image -= 32768
            return image

class ImageWritter:
    '''Write 16-bit PNG images to disk.

    Images should be enumerated (image000.png, image001.png, ...).

    '''

    def __init__(self):
        pass

    def write(self, image, number=0, path='./'):
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

        image += 32768
        
        assert (np.amax(image) < 65536), '16 bit unsigned int range overflow'
        assert (np.amin(image) >= 0), '16 bit unsigned int range underflow'
        
        cv2.imwrite(file_name, np.rint(image).astype(np.uint16))
