import unittest
import sys
sys.path.append('../mcdwt')
import MCDWTLibrary.py as ML
import MCDWT.py as M


class Test_Video_MCDWT(unittest.TestCase)

def test_video(filename):
    '''
    Compare output video after running MCDWT and iMCDWT are working properly.
    '''
	ML.split_video_in_frames_to_disk(filename)
	M.MCDWT(input='images/', output='images/output0/', n=5, l=2)
	M.iMCDWT(input='images/output0/', output='images/output1/', n=5, l=2)

    diff_total000 = cv2.absdiff('images/output0/000.png', 'images/output1/000.png')
    diff_total001 = cv2.absdiff('images/output0/001.png', 'images/output1/001.png')
    diff_total002 = cv2.absdiff('images/output0/002.png', 'images/output1/002.png')
    diff_total003 = cv2.absdiff('images/output0/003.png', 'images/output1/003.png')
    diff_total004 = cv2.absdiff('images/output0/004.png', 'images/output1/004.png')

    value0 = assertIs(diff_total000, 0)
    value1 = assertIs(diff_total001, 0)
    value2 = assertIs(diff_total002, 0)
    value3 = assertIs(diff_total003, 0)
    value4 = assertIs(diff_total004, 0)

    print(str(value0))
    print(str(value1))
    print(str(value2))
    print(str(value3))
    print(str(value4))

if __name__== '__main__':
	unittest.main()
