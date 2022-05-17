
# importing the libraries
import cv2
import numpy as np
 
# Setup camera
cap = cv2.VideoCapture(0)
#cap1 = cv2.VideoCapture(0)

 
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    #ret1, frame1 = cap1.read()
 
    cv2.imshow('WebCam0', frame)
    cv2.imshow('WebCam1', frame)
    if cv2.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
#cap1.release()
cv2.destroyAllWindows()
