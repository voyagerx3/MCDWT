#!/usr/bin/env python3

import numpy as np
import cv2
import itertools

import motion
import image_io

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def framerate_duplicator(frames):
    output = []

    for curr, next in pairwise(frames):
        output.append(curr)
        flow = motion.motion_estimation(curr, next)
        output.append(motion.estimate_frame(curr, flow / 2))
    output.append(frames[-1])

    return output

if __name__ == '__main__':

    n = 5
    input_path = '../images/'
    output_path = '/tmp/duplicator'

    ir = image_io.ImageReader()
    ir.set_path(input_path)
    frames = []
    for i in range(n):
        frames.append(ir.read(i))

    output = framerate_duplicator(frames)

    iw = image_io.ImageWritter()
    iw.set_path(output_path)
    for i in range(len(output)):
        iw.write(output[i], i)
