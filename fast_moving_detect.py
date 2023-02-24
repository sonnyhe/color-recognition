#encoding=utf-8
import cv2
import time
# import winsound

camera = cv2.VideoCapture("/Users/sonny_he/Desktop/toss_video/cut_3.mp4")    # 定义摄像头对象，其参数0表示第一个摄像头（自带摄像头）
if camera is None:
    #如果摄像头打开失败，则输出提示信息
    print('please connect the camera')
    exit()

fps = 25    #帧率 
pre_frame = None    #总是取前一帧做为背景（不用考虑环境影响）
while True:
    start = time.time()
    # 读取视频流
    res, cur_frame = camera.read()
    if res != True:
        break
    end = time.time()
    seconds = end - start
    if seconds < 1.0/fps:
        time.sleep(1.0/fps - seconds)

    cv2.namedWindow('img',0)
    #cv2.imshow('img', cur_frame)

    #检测如何按下Q键，则退出程序
    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break
    #转灰度图
    gray_img = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
    #将图片缩放
    gray_img = cv2.resize(gray_img, (500, 500))
    # 用高斯滤波进行模糊处理
    gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)

    # 如果没有背景图像就将当前帧当作背景图片
    if pre_frame is None:
        pre_frame = gray_img
    else:
        # absdiff把两幅图的差的绝对值输出到另一幅图上面来
        img_delta = cv2.absdiff(pre_frame, gray_img)
        
        #threshold阈值函数(原图像应该是灰度图,对像素值进行分类的阈值,当像素值高于（有时是小于）
        #阈值时应该被赋予的新的像素值,阈值方法)
        thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        #膨胀图像
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # findContours检测物体轮廓(寻找轮廓的图像,轮廓的检索模式,轮廓的近似办法)
        contours, hierarchy =   cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        for c in contours:
            #灵敏度
            if 50 < cv2.contourArea(c) < 10000:	# 1000为阈值
                #框选移动部分
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(cur_frame,(x,y),(x+w,y+h),(0,255,0),2)
 
                print("something is moving!!!")
                flag = True
                # if flag == True:
                    # winsound.Beep(600, 1000)
                # break
                
            else:
                continue

        #显示
        cv2.imshow('img', cur_frame)	
        pre_frame = gray_img
        
# release()释放摄像头 
camera.release()
#destroyAllWindows()关闭所有图像窗口
cv2.destroyAllWindows()