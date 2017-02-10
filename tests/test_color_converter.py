import mcdwt.rgb_ycc_conversion as rycvt
import mcdwt.image_io as img_io
import unittest


class TestColorConvertMethods(unittest.TestCase):
    def test_color_convert(self):
        reader = img_io.ImageReader()
        writer = img_io.ImageWritter()
        cvt = rycvt.ColorConverter()

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
