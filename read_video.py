import numpy as np 
import cv2 
cap = cv2.VideoCapture("rtsp://192.168.9.37:8554/all_video.264") 
while(cap.isOpened()): 
	ret, frame = cap.read() 
	cv2.imshow('frame', frame) 
	c = cv2.waitKey(1) 
	if c==27:   #ESC键 
		break 
cap.release() 
cv2.destroyAllWindows() 
