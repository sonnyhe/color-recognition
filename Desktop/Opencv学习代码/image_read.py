# image read
# img = cv2.imread(filepath, flags)
# flags = -1 8位深度， 原通道
# flags = 0 8位深度， 1通道
# flags = 1 8位深度， 3通道
# flags = 2 原深度， 1通道
# flags = 3 原深度， 3通道
# 导入Opencv库
# cv2.IMREAD_COLOR:默认参数，读入一副彩色图像，忽略alpha通道
# cv2.IMREAD_GRAYSCALE:读入灰度图片
# cv2.IMREAD_UNCHANGED:读入完整图片，包括alpha通道
import cv2
# 读取图像
img = cv2.imread("my.jpg", cv2.IMREAD_COLOR)
# 打印图像数组
print(img)

# 图像显示函数cv2.imshow(Name, img)
# Name显示框的名字
# 一般来说，imshow()需要配合cv2.waitKey(0)使用，因为该图像进行显示是一瞬间，
# 所以需要键值等待函数来固定显示，待键盘输入值或者鼠标点击关闭才能继续执行代码！
import cv2
img = cv2.imread("my.jpg", cv2.IMREAD_UNCHANGED)
cv2.imshow("sonny", img)
cv2.waitKey(0)
# cv2.waitKey(a)
# a = 0, 函数无限延长，必须有键按下才可以运行
# a > 0，函数返回值为按下键的ASCII码值，超时则返回-1，同时图像显示a秒