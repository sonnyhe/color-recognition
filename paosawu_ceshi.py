import cv2
import numpy as np
import datetime
import socket

erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

def Loss_incident(c):# 抛洒物事件
    # init_pic_background = "" 
    # cap = cv2.VideoCapture("rtsp://192.168.9.87:8554/paosa.264")
    img1 = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/masks_test2.png")
    # success, img = cap.read()
    # loss_incident_situ = False
    img = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/paosa_1.png")
    img2 = img
    BLUR_RADIUS = 21
    # print(ids)
    mask = np.zeros((1080, 1920), dtype=np.uint8)
    # pts = np.array([[0, 1080], [0, 965], [1420,300], [1755, 300], [1755, 1080], [1920, 1080]])
    # pts1 = np.array([[360, 1080], [1316, 178], [1367, 178], [1829, 1080]])
    
    pts = np.array([[0, 1080], [0, 965], [1420,300], [1755, 300], [1755, 1080], [1920, 1080]])
    pts1 = np.array([[0, 1080], [398, 1080], [1316, 178], [1367, 178], [1780, 1080], [1920, 1080], [1920, 0], [0,0]])
    pts2 = np.array([[398, 1080], [1316, 178], [1367, 178], [1730, 1080]])
    gray_frame1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_frame1 = cv2.GaussianBlur(gray_frame1, (BLUR_RADIUS, BLUR_RADIUS), 0)
    gray_frame2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    gray_frame2 = cv2.GaussianBlur(gray_frame2, (BLUR_RADIUS, BLUR_RADIUS), 0)
    '''if ids:
        for i in range(len(ids)):
            cv2.rectangle(gray_frame1,ids[i][0],ids[i][1],0,-1)
            cv2.rectangle(gray_frame2,ids[i][0],ids[i][1],0,-1)'''

    while True:
        # success, img = cap.read()
        # loss_incident_situ = False
        img = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/paosa_1.png")
        img2 = img
        BLUR_RADIUS = 21
        # print(ids)
        mask = np.zeros((1080, 1920), dtype=np.uint8)
        # pts = np.array([[0, 1080], [0, 965], [1420,300], [1755, 300], [1755, 1080], [1920, 1080]])
        # pts1 = np.array([[360, 1080], [1316, 178], [1367, 178], [1829, 1080]])
        
        pts = np.array([[0, 1080], [0, 965], [1420,300], [1755, 300], [1755, 1080], [1920, 1080]])
        pts1 = np.array([[0, 1080], [398, 1080], [1316, 178], [1367, 178], [1780, 1080], [1920, 1080], [1920, 0], [0,0]])
        pts2 = np.array([[300, 1080], [1290, 278], [1367, 278], [1730, 1080]])
        gray_frame1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray_frame1 = cv2.GaussianBlur(gray_frame1, (BLUR_RADIUS, BLUR_RADIUS), 0)
        gray_frame2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        gray_frame2 = cv2.GaussianBlur(gray_frame2, (BLUR_RADIUS, BLUR_RADIUS), 0)
        
        diff=cv2.absdiff(gray_frame1,gray_frame2)    # 获得两帧之间的差异
        
        # cv2.imshow('diff',diff)    # 图像处理：灰度，高斯模糊，二值化
        # gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        # _, thresh = cv2.threshold(diff, 20, 60, cv2.THRESH_BINARY)  # 阈值化操作得到黑白图像，（20-60）可以识别出棕色的效果
        _, thresh = cv2.threshold(diff, 20, 100, cv2.THRESH_BINARY)
        # 形态学运算进行平滑处理，便于后续边框的绘制
        cv2.erode(thresh, erode_kernel, thresh, iterations=2)
        cv2.dilate(thresh, dilate_kernel, thresh, iterations=2)
        # 用0填充多边形
        cv2.fillPoly(mask, [pts2], (255), 8, 0)
        # 位与运算
        result = cv2.bitwise_and(thresh, thresh, mask=mask)
        # cv2.imshow('dilated',dilated)    # 获取轮廓
        contours,_ =cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    # 判断矩形是否满足条件
        if contours:
            for contour in contours:
                x,y,w,h=cv2.boundingRect(contour)
                if 50 < cv2.contourArea(contour) < 10000:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
                    # cv2.imshow('image',img1)    # 读下一帧
                    loss_incident_situ = True
            # dt_ms = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') # 获取当前时间
            # path = "/home/HwHiAiUser/mxVision-2.0.4.6/samples/mxVision/python/pic/car/%s.png"%dt_ms
            # cv2.imwrite(path, img)

        cv2.imshow("diff", diff)
        cv2.imshow("thresh", result)
        cv2.imshow("detection", img)
        cv2.waitKey(27)

    # success, frame = cap.read()
    # cv2.flip(frame, 1)

if __name__ == '__main__':
    rtsp_url = "rtsp://192.168.9.87:8554/paosa.264"
    cap = cv2.VideoCapture(rtsp_url)
    # ids = redis()

    Loss_incident(cap)
