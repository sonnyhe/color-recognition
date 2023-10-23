import cv2
import numpy as np

# 创建一个空白图像
# image = np.zeros((512, 512, 3), dtype=np.uint8)
image = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/vlc.jpg')

# 存储鼠标点击的坐标
points = []
start_point = None
drawing = False

def draw_line(event, x, y, flags, param):
    global start_point, drawing, points

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        drawing = True
        points.append(start_point)

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.line(image, start_point, (x, y), (0, 0, 255), 2)
        start_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

    # 显示图像
    cv2.imshow('Image', image)

# 创建窗口并绑定鼠标事件
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_line)

# 显示图像
cv2.imshow('Image', image)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
