#!/usr/bin/env python3

import numpy as np
import itertools

import motion
import image_io

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def framerate_duplicator(frames):
    ''' Generates n-1 interpolated frames from n base frames.

    Arguments
    ---------

        frames : [[:,:,:]]
            
            List of base frames.

    Returns
    -------

        List of frames including interleaved interpolated frames.

    '''

    output = []

    for curr, next in pairwise(frames):
        output.append(curr)
        flow = motion.motion_estimation(curr, next)
        output.append(motion.estimate_frame(curr, flow / 2))
    output.append(frames[-1])

    return output
