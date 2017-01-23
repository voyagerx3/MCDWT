import numpy as np
import cv2
import pywt


# Reads a video file frame by frame, convert each frame to YCrCb
# and saves it in the folder /output as a binaryfile with .npy extension

def read_video(filename):

    cap = cv2.VideoCapture(filename)
    num_frame = 0
    while(True):
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

        np.save('output/' + filename + str(num_frame), image)
        num_frame = num_frame + 1

        if ret == False:
            break

# Reads a frame from a filename


def read_frame(filename):

    image = np.load(filename)

    # To see it in RGB uncomment the next line
    # image = cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)

    return image

# Compute the 1-level 2D-DWT of a frame in memory 

def image_to_dwt2d(image):

    coeffs = pywt.dwt2(image, 'haar')
    
    return coeffs

# Compute to a frame the 1-level 2D-DWT

def dwt2d_to_image(coeffs):

    image = pywt.idwt2(coeffs, 'haar')
    
    return image



# read_video('stockholm_1280x768x50x420x578.avi')

# image = read_frame('output/stockholm_1280x768x50x420x578.avi13.npy')   
# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# image = read_frame('output/stockholm_1280x768x50x420x578.avi13.npy') 
# image = dwt2d_to_image(image_to_dwt2d(image))  
# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
