import cv2
import numpy as np

# 读取图像
image = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/img3.jpg')

# 定义矩形的四个顶点
rect_points = np.array([[100, 100], [100, 200], [200, 200], [200, 100]], np.int32)
rect_points = rect_points.reshape((-1, 1, 2))

# 检测直线
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

# 绘制直线
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# 绘制矩形
cv2.polylines(image, [rect_points], isClosed=True, color=(0, 255, 0), thickness=2)

# 检查直线和矩形是否相交
for line in lines:
    for point in rect_points:
        if cv2.pointPolygonTest(point, (line[0][0], line[0][1]), False) >= 0:
            print("直线和矩形相交")

# 显示图像
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
