import cv2

# 回调函数，用于处理鼠标点击事件
def mouse_callback(event, x, y, flags, param):
    global last_click_x, last_click_y

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"点击坐标: ({x}, {y})")
        if last_click_x is not None and last_click_y is not None:
            cv2.line(image, (last_click_x, last_click_y), (x, y), (0, 0, 255), 2)
        last_click_x, last_click_y = x, y
        cv2.imshow("Image", image)

# 创建一个空白图像
image = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/2023_10_16_14_06_53_963746.png')
last_click_x, last_click_y = None, None

# 创建窗口并设置鼠标回调函数
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)

while True:
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == 27:  # 按ESC键退出
        break

cv2.destroyAllWindows()
