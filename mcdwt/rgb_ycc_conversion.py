import cv2


class ColorConverter:
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
