import cv2
import numpy as np


class InputFileException(Exception):
    pass


class ImageReader:
    '''Read PNG images from disk.
    
    Images must be enumerated. Example: "image000.png, image001.png,
    ..."

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
            return image


class ImageWritter:
    '''Write PNG images to disk.

    Images should be enumerated. Example: "image000.png, image001.png, ..."

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
        cv2.imwrite(file_name, image)


class ImageColorConverter:
    '''Convert PNG image color from YCbCr to RGB and vice versa.


    '''

    def __init__(self):
        pass

    def rgb2ycc(self, image):
        '''Convert YCbCr to RGB

            Parameters
            ----------

                image : [:,:,:].

            Returns
            -------

                image : [:,:,:].

                A image in YCbCr.
        '''

        imYCC = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        return imYCC

    def ycc2rgb(self, image):
        '''Convert YCbCr to RGB

            Parameters
            ----------

                image : [:,:,:].

            Returns
            -------

                image : [:,:,:].

                A image in RGB.
        '''

        imRGB = cv2.cvtColor(image, cv2.COLOR_YCR_CB2BGR)
        return imRGB
