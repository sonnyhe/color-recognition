import os
import numpy as np
import cv2

start = (0, 300)
end = (1920, 300)

start1 = (0, 965)
end1 = (1500, 300)

start2 = (1750, 1080)
end2 = (1750, 300)

start3 = ()
end3 = ()

point_color = (0, 255, 0)
thickness = 1
linetype = 4

frame = cv2.imread("vlc.jpg")
frame = cv2.line(frame, start, end, point_color, thickness, linetype)
frame = cv2.line(frame, start1, end1, point_color, thickness, linetype)
frame = cv2.line(frame, start2, end2, point_color, thickness, linetype)
cv2.rectangle(frame,(1400,337),(1450,411),0,-1)   #画小矩形
pts = np.array([[200,100],[200,500],[50,300],[500,200],[500,400]],np.int32)  #构建多边形的顶点
cv2.fillPoly(frame,[pts],(0, 0, 0)) 
# frame = cv2.line(frame, start3, end3, point_color, thickness, linetype)

cv2.namedWindow('test')
cv2.imshow('test', frame)
cv2.waitKey(100000)
cv2.destroyAllWindows()