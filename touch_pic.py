import cv2

# 创建一个回调函数，用于鼠标点击事件
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"坐标：({x}, {y})")

# 读取图像
image = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/vlc.jpg')

# 显示图像
cv2.imshow('Image', image)

# 设置鼠标事件回调
cv2.setMouseCallback('Image', mouse_callback)

# 等待用户关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
