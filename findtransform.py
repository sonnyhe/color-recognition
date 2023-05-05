
import cv2
import numpy as np

# 读取大图像和小模板图像
img = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/xaingsi.png')
template = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/xaingsi.png')

# 将大图像和小模板图像转为灰度图像
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# 计算匹配结果矩阵
res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# 获取匹配结果的最大值和最小值
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
print(min_val, max_val, min_loc, max_loc)
# 在大图像上绘制矩形框标记匹配位置
top_left = max_loc
bottom_right = (top_left[0] + template_gray.shape[1], top_left[1] + template_gray.shape[0])
cv2.rectangle(img, top_left, bottom_right, (0,0,255), 2)

# 显示匹配结果
cv2.imshow('Matching Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()