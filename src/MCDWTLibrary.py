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

    while(cap.isOpened()):

        ret, frame = cap.read()
        if frame is None:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)


        cv2.imwrite('output/PNG/imagen'+str(num_frame)+'.png',image)
        
        num_frame = num_frame + 1


def read_frame(filename):
    '''
    Reads a frame from a filename.
    '''

    # To see it in RGB uncomment the next line
    # image = cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)

    return cv2.imread(filename,1)

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

def forward_MCDWT(imageA, imageB, imageC):

    coeffA=image_to_dwt2d(imageA[:,:,0])
    coeffB=image_to_dwt2d(imageB[:,:,0])
    coeffC=image_to_dwt2d(imageC[:,:,0])
    
    All = coeffA[0]
    Ahl = coeffA[1][0]
    Alh = coeffA[1][1]
    Ahh = coeffA[1][2]

    Bll = coeffB[0]
    Bhl = coeffB[1][0]
    Blh = coeffB[1][1]
    Bhh = coeffB[1][2]

    Cll = coeffC[0]
    Chl = coeffC[1][0]
    Clh = coeffC[1][1]
    Chh = coeffC[1][2]
    
    zeroes = np.zeros((384, 640), dtype="float64")
        
    iAl = dwt2d_to_image((All,(zeroes,zeroes,zeroes)))
    iAh = dwt2d_to_image((zeroes,(Ahl,Alh,Ahh)))


    iBl = dwt2d_to_image((Bll,(zeroes,zeroes,zeroes)))
    iBh = dwt2d_to_image((zeroes,(Bhl,Blh,Bhh)))


    iCl = dwt2d_to_image((Cll,(zeroes,zeroes,zeroes)))
    iCh = dwt2d_to_image((zeroes,(Chl,Clh,Chh)))


    imagenResiduo = iBh-((iAh + iCh)/2)

    coeffR = image_to_dwt2d(imagenResiduo)
    
    Rll = coeffR[0]
    Rhl = coeffR[1][0]
    Rlh = coeffR[1][1]
    Rhh = coeffR[1][2]

    Rll = Bll

    outputA = np.zeros((768, 1280), dtype="int16")
    outputA[0:384, 0:640] = All
    outputA[0:384, 640:1280] = Ahl
    outputA[384:768, 0:640] = Alh
    outputA[384:768, 640:1280] = Ahh

    outputC = np.zeros((768, 1280), dtype="int16")
    outputC[0:384, 0:640] = Cll
    outputC[0:384, 640:1280] = Chl
    outputC[384:768, 0:640] = Clh
    outputC[384:768, 640:1280] = Chh

    outputR = np.zeros((768, 1280), dtype="int16")
    outputR[0:384, 0:640] = Rll
    outputR[0:384, 640:1280] = Rhl
    outputR[384:768, 0:640] = Rlh
    outputR[384:768, 640:1280] = Rhh

    cv2.imwrite('output/PNG/A.png',outputA)
    cv2.imwrite('output/PNG/R.png',outputR)
    cv2.imwrite('output/PNG/C.png',outputC)

        
    
# forward_MCDWT(read_frame('output/PNG/imagen56.png'),read_frame('output/PNG/imagen57.png'),read_frame('output/PNG/imagen58.png'))

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