#!/usr/bin/env python3

import os
import sys
import cv2
import numpy as np
import tempfile as tf
#sys.path.insert(0, '../mcdwt')
import duplicator

n = 5
input_path = '../../images'
output_path = tf.gettempdir()

frames = []
for i in range(n):
    path = os.path.join(input_path, '{:03d}.png'.format(i))
    print('Reading frame:', path)
    frames.append(cv2.imread(path))

output = duplicator.framerate_duplicator(frames)

for i in range(len(output)):
    path = os.path.join(output_path, 'duplicator_{:02d}.png'.format(i))
    print('Writing frame:', path)
    cv2.imwrite(path, output[i])
