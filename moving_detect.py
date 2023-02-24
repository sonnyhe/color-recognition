import cv2
cam= cv2.VideoCapture('/Users/sonny_he/Desktop/toss_video/cut_3.mp4')
# 先读取视频的前2帧
_,img1=cam.read()
_,img2=cam.read()
while cam.isOpened():    # 获得两帧之间的差异    
    diff=cv2.absdiff(img1,img2)    
    cv2.imshow('diff',diff)    # 图像处理：灰度，高斯模糊，二值化    
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)    
    blur=cv2.GaussianBlur(gray,(5,5),0)    
    _,th=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)    # 图像膨胀操作    
    dilated=cv2.dilate(th,None,iterations=3)    
    cv2.imshow('dilated',dilated)    # 获取轮廓        
    contours,_=cv2.findContours(dilated,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    # 判断矩形是否满足条件    
    for contour in contours:        
        (x,y,w,h)=cv2.boundingRect(contour)        
        if cv2.contourArea(contour) < 700:            
            continue        
        else:            
            cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),1)    
            cv2.imshow('image',img1)    # 读下一帧    
            img1=img2    
            _,img2=cam.read()    
            flag=cv2.waitKey(100)
            if flag==ord('q'):        
                break# 别忘记释放摄像头
cam.release()
cv2.destroyAllWindows()