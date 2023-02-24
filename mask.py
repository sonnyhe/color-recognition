import cv2 as cv
import numpy as np
src = cv.imread("/Users/sonny_he/Desktop/line.jpg")
cv.imshow("input", src)
 
# 生成mask区域
mask = np.zeros((1080, 1920), dtype=np.uint8)
# pts = np.array([[0, 965], [1420,300], [1755, 300], [1755, 1080], [1920, 1080], [1920, 0], [0, 0]])

pts = np.array([[0, 1080], [0, 965], [1420,300], [1755, 300], [1755, 1080], [1920, 1080]])
cv.fillPoly(mask, [pts], (255), 8, 0)
cv.imshow("mask", mask)

# 提取ROI区域，根据mask
result = cv.bitwise_and(src, src, mask=mask)
cv.imshow("result", result)
cv.waitKey(0)