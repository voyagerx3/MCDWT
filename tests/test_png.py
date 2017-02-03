import cv2
import numpy as np

image = (np.random.rand(256, 256) * 255).astype('uint16')
cv2.imwrite('/tmp/a.png', image)
image2=cv2.imread('/tmp/a.png',-1)
(image==image2).all()

