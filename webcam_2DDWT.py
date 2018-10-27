import numpy as np
import cv2
#from filters.copy_frame import process_frame
from transform.dwt import forward, backward
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    LL, H = forward(frame)
    cv2.imshow('LL', LL.astype(np.uint8))
    cv2.imshow('LH', H[0].astype(np.uint8)*16+128)
    cv2.imshow('HL', H[1].astype(np.uint8)*16+128)
    cv2.imshow('HH', H[2].astype(np.uint8)*16+128)
    recons = backward(LL, H)

    # Display the resulting frame
    cv2.imshow('WebCam', recons.astype(np.uint8))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
