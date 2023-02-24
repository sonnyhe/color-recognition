import cv2
import datetime
import numpy as np

# 定义运算的核算子
BLUR_RADIUS = 21
erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

pre_hier = np.array([[[ 0, 0, 0, 0],
        [ 0, 0, 0, 0],
        [0, 0, 0, 0]]])
# print(pre_hier[0][0])
count = []
# 打开摄像头
cap = cv2.VideoCapture("/Users/sonny_he/Desktop/toss_video/cut_3.mp4")
success, frame = cap.read()

# 丢弃9帧，让相机有足够时间调整
for i in range(2):
    success, frame = cap.read()
    if not success:
        exit(1)

# 取第十帧，并进行模糊操作，作为背景
# frame_test = ("/Users/sonny_he/Desktop/opencv_learning/test.png")
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
    cv2.rectangle(thresh,(1200,250),(1450,411),0,-1) 
    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(hier)
    # if contours:
    '''s = len(hier[0])
        print(s)
        for i in range(s):
            count[i] += 1
        for i in range(len(count)):
            if count[i] >= 25:
                for c in contours:
                        # print(c)
                        print("next")
                        # print(contours)
                        print(len(contours))
                        if i < len(contours):
                            # print(contours[i])
                            # 排除轮廓太小的物体
                            if 50 <= cv2.contourArea(contours[i]) < 5000:
                                x, y, w, h = cv2.boundingRect(contours[i])
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                                time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                                # cv2.imwrite("/Users/sonny_he/Desktop/opencv_learning/save_file/%s.jpg"%time1, frame)
                            else:
                                print("something is wrong")
                        else:
                            count[i] = 0
            else:
                continue'''
        # s = len(hier[0])
        # count = np.zeros(s, dtype=int)
        # for i in range(s):
            
    if contours:
        if len(hier[0]) > 20:
            print("error")
        else:
            m = len(hier[0])
            n = len(pre_hier[0])
            if m <= n:
                n = m
            else:
                m = n
            for i in range(n):
                # print("hier")
                # print(len(hier[0])) 
                # print(hier)
                # print(hier[0][i])
                if (pre_hier[0][i] == hier[0][i]).all():
                         #print(len(hier[0]))
                        print("start")
                        # print(pre_hier[0,0])
                        # print(hier[0,0])
                        count[i] += 1
                        if count[i] >= 50:
                            if 100 <= cv2.contourArea(contours[i]) < 100000:
                                x, y, w, h = cv2.boundingRect(contours[i])
                                y1 = 965-0.443*x
                                if x < 1750 & y > 300:
                                    if y > y1:
                                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                                        time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                                    # cv2.imwrite("/Users/sonny_he/Desktop/opencv_learning/save_file/%s.jpg"%time1, frame)
                            else:
                                    print("something is wrong")  
                else:
                        print("not in ")
                        count[i] == 0
                    # if pre_hier[i][0] in hier[...,0]:
                            
                    # else:
                            # print("haha")

            pre_hier = hier

        
    else:
        count = np.zeros(25, dtype=int)
    
    cv2.imshow("diff", diff)
    cv2.imshow("thresh", thresh)
    cv2.imshow("detection", frame)

    if cv2.waitKey(1) == 27:  # 按下esc键退出
        break

    success, frame = cap.read()
    # cv2.flip(frame, 1)

cap.release()
cv2.destroyAllWindows()