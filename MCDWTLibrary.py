import numpy as np
import cv2
import pywt

def split_video_in_frames_to_disk(filename):
    '''
    Reads a video file frame by frame, convert each frame to
    YCrCb and saves it in the folder /output as a binaryfile with
    .npy extension.
    '''
    cap = cv2.VideoCapture(filename)
    num_frame = 0
    while(True):
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

        np.save('output/' + filename + str(num_frame), image)
        num_frame = num_frame + 1

        if ret == False:
            break

def read_frame(filename):
    '''
    Reads a frame from a filename.
    '''
    image = np.load(filename)

    # To see it in RGB uncomment the next line
    # image = cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)

    return image

def image_to_dwt2d(image):
    '''
    Compute the 1-level 2D-DWT of a frame in memory.
    '''
    coeffs = pywt.dwt2(image, 'haar')
    
    return coeffs



def dwt2d_to_image(coeffs):
    '''
    Compute to a frame the 1-level 2D-DWT
    '''
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
