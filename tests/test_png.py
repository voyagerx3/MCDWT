import mcdwt.image_io as img
import numpy as np
import unittest


class TestImageMethods(unittest.TestCase):
    def test_read_write(self):
        reader = img.ImageReader()
        writer = img.ImageWritter()

        # Create a random 'image'
        im_uint = (np.random.rand(256, 256) * 255).astype('uint16')
        im_int = (np.random.rand(256, 256) * 255).astype('int16')

        # Write the image
        writer.write(im_uint, 0, '../images/output/uint_')
        writer.write(im_int, 0, '../images/output/int_')

        # Read the image
        im_rd_uint = reader.read(0, '../images/output/uint_')
        im_rd_int = reader.read(0, '../images/output/int_')

        # Assert
        self.assertIsNotNone(im_rd_uint, msg="Fail to read the image")
        self.assertIsNotNone(im_rd_int, msg="Fail to read the image")
        self.assertEquals(im_uint.all(), im_rd_uint.all(), msg="Fail to check image integrity")
        self.assertEquals(im_int.all(), im_rd_int.all(), msg="Fail to check image integrity")

    def test_color_convert(self):
        reader = img.ImageReader()
        writer = img.ImageWritter()
        cvt = img.ImageColorConverter()

        # Read image in YCbCr
        im_ycc = reader.read(0, '../images/')

        # Convert to RGB
        im_rgb = cvt.ycc2rgb(im_ycc)

        # Convert back
        im_back = cvt.rgb2ycc(im_rgb)

        # Write images
        writer.write(im_rgb, 0, '../images/output/rgb_')
        writer.write(im_ycc, 0, '../images/output/ycc_')
        writer.write(im_back, 0, '../images/output/back_')

        # Assert
        self.assertEqual(im_ycc.all(), im_back.all(), msg="Fail to convert YCbCr to RGB and back")

if __name__ == '__main__':
    unittest.main()

