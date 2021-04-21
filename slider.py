
# import important liabraries 
import cv2 
import numpy as np
import argparse
# defining function
def nothing(x):
    pass
# creating trackbar (setting up the pixel contrast limits) ( GUI)
cv2.namedWindow("Tracking")
cv2.createTrackbar("lower_R", "Tracking", 0, 255, nothing)
cv2.createTrackbar("lower_G", "Tracking", 0, 255, nothing)
cv2.createTrackbar("lower_B", "Tracking", 0, 255, nothing)
cv2.createTrackbar("upper_R", "Tracking", 255, 255, nothing)
cv2.createTrackbar("upper_G", "Tracking", 255, 255, nothing)
cv2.createTrackbar("upper_B", "Tracking", 255, 255, nothing)

while True:
    
    # setting command line arguments 
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help = "path to the image file")
    args = vars(ap.parse_args())
    # reading the image 
    frame = cv2.imread(args["image"])
    
    # converting the BGR to RGB contrast  
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Setting trackbar limits 
    l_r = cv2.getTrackbarPos("lower_R", "Tracking") 
    l_g = cv2.getTrackbarPos("lower_G", "Tracking") 
    l_b = cv2.getTrackbarPos("lower_B", "Tracking") 
    u_r = cv2.getTrackbarPos("upper_R", "Tracking")
    u_g = cv2.getTrackbarPos("upper_G", "Tracking")
    u_b = cv2.getTrackbarPos("upper_B", "Tracking")
    
    lower_bound = np.array([l_r, l_g, l_b])
    upper_bound = np.array([u_r, u_g, u_b])
    # creating mask 
    mask = cv2.inRange(rgb, lower_bound, upper_bound)
    # overlapping mask and image for seperating particles 
    res = cv2.bitwise_and(frame, frame, mask=mask)
    # displaying images 
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cv2.destroyallWindows()

  