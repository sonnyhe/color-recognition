import os
import numpy as np
import cv2

start4 = (0, 777) #area1
end4 = (1920, 777)

end = (0, 618)# (1920, 300)
start = (1920, 618)# (0, 300)y2

end1 = (0, 528)# (1500, 300)
start1 =(1920, 528) # (0, 965)y3

end2 = (0, 462)# (1750, 300)
start2 = (1920, 462)# (1750, 1080)y4

start3 = (0, 416)# y5
end3 = (1920, 416)

start5 = (0, 386)# y5
end5 = (1920, 386)

start6 = (0, 356)# y6
end6 = (1920, 356)

start7 = (0, 335)# y7
end7 = (1920, 335)

start8 = (0, 305)# y8
end8 = (1920, 305)

start9 = (0, 280)# y9
end9 = (1920, 280)




start10 = (1280, 0)# 边界线1
end10 = (1830, 1080)

start11 = (1405, 0)# 边界线2
end11 = (1045, 1080)

start12 = (1510, 0)# 边界线3
end12 = (360, 1080)




# 测速线

point_color = (0, 255, 0)
thickness = 1
linetype = 4

frame = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/15432-0003.png")
frame = cv2.line(frame, start, end, point_color, thickness, linetype)
frame = cv2.line(frame, start1, end1, point_color, thickness, linetype)
frame = cv2.line(frame, start2, end2, point_color, thickness, linetype)
frame = cv2.line(frame, start3, end3, point_color, thickness, linetype)
frame = cv2.line(frame, start4, end4, point_color, thickness, linetype)
frame = cv2.line(frame, start5, end5, point_color, thickness, linetype)
frame = cv2.line(frame, start6, end6, point_color, thickness, linetype)
frame = cv2.line(frame, start7, end7, point_color, thickness, linetype)
frame = cv2.line(frame, start8, end8, point_color, thickness, linetype)
frame = cv2.line(frame, start9, end9, point_color, thickness, linetype)
frame = cv2.line(frame, start10, end10, point_color, thickness, linetype)
frame = cv2.line(frame, start11, end11, point_color, thickness, linetype)
frame = cv2.line(frame, start12, end12, point_color, thickness, linetype)


# cv2.rectangle(frame,(1400,337),(1450,411),0,-1)   #画小矩形
# pts = np.array([[200,100],[200,500],[50,300],[500,200],[500,400]],np.int32)  #构建多边形的顶点
pts = np.array([[0, 1080], [260, 1080], [655, 400], [980,445], [1520, 1080], [1920, 1080], [1920, 0], [0,0]])
# pts1 = np.array([[360, 1080], [1316, 178], [1367, 178], [1829, 1080]])
# cv2.fillPoly(frame,[pts],255, 8,0) 
# frame = cv2.line(frame, start3, end3, point_color, thickness, linetype)

cv2.namedWindow('test')
cv2.imshow('test', frame)
cv2.imwrite("event_line_final.jpg", frame)
cv2.waitKey(100000)
cv2.destroyAllWindows()