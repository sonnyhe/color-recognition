from array import array
import cv2
import numpy as np
import datetime
# 定义运算的核算子
BLUR_RADIUS = 21
erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

# 打开摄像头
rtsp_url = "rtsp://192.168.9.87:8554/mystream"
# cap = cv2.VideoCapture("/Users/sonny_he/Desktop/toss_video/cut_3.mp4")
cap = cv2.VideoCapture(rtsp_url)
success, frame = cap.read()

# 丢弃9帧，让相机有足够时间调整
for i in range(2):
    success, frame = cap.read()
    if not success:
        exit(1)

# 取第十帧，并进行模糊操作，作为背景
frame_test = frame# [100:500, 100:500]
gray_background = cv2.cvtColor(frame_test, cv2.COLOR_BGR2GRAY)
gray_background = cv2.GaussianBlur(gray_background, (BLUR_RADIUS, BLUR_RADIUS), 0)

# 有了背景的参考图像，开始检测物体，对每一帧转成灰度和高斯模糊
success, frame = cap.read()
frame = frame# [100:500, 100:500]
# frame = cv2.flip(frame, 1)
while success:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (BLUR_RADIUS, BLUR_RADIUS), 0)

    # 对两张图片进行差值的绝对值操作
    diff = cv2.absdiff(gray_background, gray_frame)
    _, thresh = cv2.threshold(diff, 80, 255, cv2.THRESH_BINARY)  # 阈值化操作得到黑白图像

    # 形态学运算进行平滑处理，便于后续边框的绘制
    cv2.erode(thresh, erode_kernel, thresh, iterations=2)
    cv2.dilate(thresh, dilate_kernel, thresh, iterations=2)

    # 先寻找轮廓
    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        for i in range(len(hier[0])):
            print(hier[0][i])
            print("hello")
    # a3 = np.array(hier)
    # res = a3
    # print(res)

    # print(contours)
    # print("hello")
    for c in contours:
        # 排除轮廓太小的物体
        print((hier[0][0]))
        if 50 <= cv2.contourArea(c) < 5000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            # cv2.imwrite("/Users/sonny_he/Desktop/opencv_learning/save_file/%s.jpg"%time1, frame)
 
    cv2.imshow("diff", diff)
    cv2.imshow("thresh", thresh)
    cv2.imshow("detection", frame)
 
    if cv2.waitKey(1) == 27:  # 按下esc键退出
        break
 
    success, frame = cap.read()
    # cv2.flip(frame, 1)
 
cap.release()
cv2.destroyAllWindows()