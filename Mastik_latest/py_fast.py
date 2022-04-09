# Importing the libraries
import cv2
  
# Reading the image and converting into B/W
image = cv2.imread('house.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
  
# Applying the function
fast = cv2.FastFeatureDetector_create()
fast.setNonmaxSuppression(False)
  
  
# Drawing the keypoints
kp = fast.detect(gray_image, None)
kp_image = cv2.drawKeypoints(image, kp, None, color=(0, 255, 0))
  
#cv2.imshow('FAST', kp_image)
#cv2.waitKey()
