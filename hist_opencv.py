import cv2
import numpy as np
# 读取图像
img1 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/15432-0003.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/paosa_1.png', cv2.IMREAD_GRAYSCALE)

# 计算直方图
hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])

# 比较直方图
diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

# 输出结果
print('直方图差异:', diff)

# 显示原图像
cv2.imshow('img1', img1)
cv2.imshow('img2', img2)

# 保存结果图像
cv2.imwrite('resulrt_diff.png', cv2.vconcat([img1, img2]))

cv2.waitKey(0)
cv2.destroyAllWindows()


