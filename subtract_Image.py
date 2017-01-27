import cv2
import numpy as np
#import pywt
#import matplotlib.pyplot as plt

image1 = cv2.imread('01.png')
print(type(image1))
image2 = cv2.imread('02.png')

#image3=np.subtract(image1-image2)
image3=image2-image1

all_zeros=np.count_nonzero(image3)
print(all_zeros)
cv2.imwrite('03.png',image3)


