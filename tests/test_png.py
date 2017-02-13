import cv2
import numpy as np

image = (np.random.rand(256, 256) * 255).astype('uint16')
cv2.imwrite('/tmp/a.png', image)
image2 = cv2.imread('/tmp/a.png', -1)
(image == image2).all()
print(type(image[0][0]))
print(type(image2[0][0]))

image = (np.random.rand(256, 256) * 255).astype('int16')
cv2.imwrite('/tmp/a.png', image)
image2 = cv2.imread('/tmp/a.png',-1)
(image == image2).all()
print(type(image[0][0]))
print(type(image2[0][0]))

