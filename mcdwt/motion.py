#!/usr/bin/env python3

import numpy as np
import cv2

def motion_compensation(curr, next, base):
    estimated = np.zeros(curr.shape, curr.dtype)
    flow = motion_estimation(curr, next)
    
    height = flow.shape[0]
    width = flow.shape[1]

    for i in range(height):
        for j in range(width):
            x = bound_index(apply_flow(i, flow[i][j][1]), height - 1)
            y = bound_index(apply_flow(j, flow[i][j][0]), width - 1)
            estimated[i][j] = base[x][y]

    return estimated

def motion_estimation(curr, next):
    curr_y, _, _ = cv2.split(curr)
    next_y, _, _ = cv2.split(next)

    return cv2.calcOpticalFlowFarneback(next_y, curr_y, None, 0.5, 3, 15, 3, 5, 1.2, 0)

def apply_flow(i, flow):
    return np.round(i + flow).astype(int)

def bound_index(i, maximum):
    return max(min(maximum - 1, i), 0)
