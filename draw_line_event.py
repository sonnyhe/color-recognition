import os
import numpy as np
import cv2

start4 = (660, 440) # y1
end4 = (260, 1080)

end = (725, 440)# (1920, 300)
start = (560, 1080)# (0, 300)y2

end1 = (785, 440)# (1500, 300)
start1 =(850, 1080) # (0, 965)y3

end2 = (865, 440)# (1750, 300)
start2 = (1180, 1080)# (1750, 1080)y4

start3 = (950, 440)# y5
end3 = (1530, 1080)

# 测速线
line1 = 700
line2 = 800

line1_start = (0, line1)
line1_end = (1920, line1)

line2_start = (0, line2)
line2_end = (1920, line2)

point_color = (0, 255, 0)
thickness = 1
linetype = 4

frame = cv2.imread("param.jpg")
frame = cv2.line(frame, start, end, point_color, thickness, linetype)
frame = cv2.line(frame, start1, end1, point_color, thickness, linetype)
frame = cv2.line(frame, start2, end2, point_color, thickness, linetype)
frame = cv2.line(frame, start3, end3, point_color, thickness, linetype)
frame = cv2.line(frame, start4, end4, point_color, thickness, linetype)
frame = cv2.line(frame, line1_start, line1_end, point_color, thickness, linetype)
frame = cv2.line(frame, line2_start, line2_end, point_color, thickness, linetype)
# cv2.rectangle(frame,(1400,337),(1450,411),0,-1)   #画小矩形
# pts = np.array([[200,100],[200,500],[50,300],[500,200],[500,400]],np.int32)  #构建多边形的顶点
# pts = np.array([[0, 1080], [260, 1080], [655, 400], [980,445], [1520, 1080], [1920, 1080], [1920, 0], [0,0]])
# pts1 = np.array([[360, 1080], [1316, 178], [1367, 178], [1829, 1080]])
# cv2.fillPoly(frame,[pts],255, 8,0) 
# frame = cv2.line(frame, start3, end3, point_color, thickness, linetype)

cv2.namedWindow('test')
cv2.imshow('test', frame)
cv2.imwrite("param_line_final.jpg", frame)
cv2.waitKey(100000)
cv2.destroyAllWindows()