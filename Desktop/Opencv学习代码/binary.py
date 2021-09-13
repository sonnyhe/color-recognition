import cv2
import numpy as py

# global threshold
def threshold_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("before", gray)

    # 大律法，全局自适应阈值，参数0可改为任意数字但不起作用
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print("yuzhi: %s" % ret)
    cv2.imshow("OTSU", binary)

    # TRIANGLE法，全局自适应阈值，参数0可改为任意数字但不起作用，适用于单个波峰
    ret, binary = cv2.threshold(gray, 0 ,255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    print("yuzhi:% s" % ret)
    cv2.imshow("TRIANGLE", binary)

    #自定义阈值为150，大于150的是白色 小于的是黑色
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    print("yuzhi: %s" % ret)
    cv2.imshow("define_yuzhi", binary)

    #自定义阈值为150，大于150的是黑色，小于150的是白色
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    print("yuzhi: %s" % ret)
    cv2.imshow("define_rev", binary)
    #截断，大于150的是改为150，小于150的保留
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_TRUNC)
    print("yuzhi: %s" % ret)
    cv2.imshow("jieduan1", binary)

    #截断小于150的是改为150， 大于150的保留
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_TOZERO)
    print("yuzhi: %s" % ret)
    cv2.imshow("jieduan2",binary)


src = cv2.imread("/Users/sonny_he/Desktop/1.png")
threshold_image(src)
cv2.waitKey(0)
cv2.destroyAllWindows()