import cv2
import numpy as np
import pywt
#import matplotlib.pyplot as plt

frame = cv2.imread('output/PNG/imagen56.png')
#cv2.imshow('003', frame); cv2.waitKey(0); cv2.destroyAllWindows()
#cv2.imshow('003', frame[:,:,0]); cv2.waitKey(0); cv2.destroyAllWindows()

'''
pyramid = pywt.dwt2(frame, 'db5')
frame2 = pywt.idwt2(pyramid, 'db5')
'''

pyramid = [None]*3
for c in range(3):
    pyramid[c] = pywt.dwt2(frame[:,:,c], 'db5')

tmp = [None]*3
for c in range(3):
    tmp[c] = pywt.idwt2(pyramid[c], 'db5')

frame2 = np.empty((768,1280,3))
for c in range(3):
    frame2[:,:,c] = tmp[c]
frame2 = frame2.astype(int)

#cv2.imshow('003', frame2); cv2.waitKey(0); cv2.destroyAllWindows()
#cv2.imshow('003', frame2[:,:,2]); cv2.waitKey(0); cv2.destroyAllWindows()
print((frame==frame2).all())

cv2.imwrite('test_dwt_output.png',frame2)
