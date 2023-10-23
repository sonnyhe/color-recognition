import cv2 
import numpy as np

def three_frame_differencing(videopath):
    cap = cv2.VideoCapture(videopath)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    one_frame = np.zeros((height, width), dtype=np.uint8)
    two_frame = np.zeros((height, width), dtype=np.uint8)
    three_frame = np.zeros((height, width), dtype=np.uint8)
    frame_count = 0
    
    paosawu_situation = False
    
    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1
        if frame_count % 2 == 0:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if not ret:
                break
            one_frame, two_frame, three_frame = two_frame, three_frame, frame_gray
            abs1 = cv2.absdiff(one_frame, two_frame)
            _, thresh1 = cv2.threshold(abs1, 40, 255, cv2.THRESH_BINARY)
            
            abs2 = cv2.absdiff(two_frame, three_frame)
            _, thresh2 = cv2.threshold(abs2, 40, 255, cv2.THRESH_BINARY)
            
            binary = cv2.bitwise_and(thresh1, thresh2)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
            erode = cv2.erode(binary, kernel)
            dilate = cv2.dilate(erode, kernel)
            dilate = cv2.dilate(dilate, kernel)
            
            contours, hei = cv2.findContours(dilate.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if 100 < cv2.contourArea(contour) < 40000:
                    x,y,w,h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255))
                    paosawu_situation = True
            if paosawu_situation:
                print("hahaha")
                cv2.namedWindow("binary", cv2.WINDOW_NORMAL)
                cv2.namedWindow("dilate", cv2.WINDOW_NORMAL)
                cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
                cv2.imshow("binary", binary)
                cv2.imshow("dilate",dilate)
                cv2.imshow("frame",frame)
            if cv2.waitKey(50)&0xFF==ord("q"):
                break
        
    cap.release()
    cv2.destoryAllWindows()

def gaosi(videopath):
    cap = cv2.VideoCapture(videopath)
    kernel =cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    fgbg =cv2.createBackgroundSubtractorMOG2()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    frame1 = np.zeros((640,480))
    # out = cv2.VideoWriter("test424.avi",fourcc,10,(640,480))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    while cap.isOpened():
        ret,frame =cap.read()
        if not ret:
            break
        cv2.imshow("1",frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
 
        fgmask =fgbg.apply(frame)
        mask = cv2.morphologyEx(fgmask,cv2.MORPH_OPEN,kernel)
        cv2.imshow("2",mask)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        contours,_ = cv2.findContours(fgmask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if 100<cv2.contourArea(c)<40000:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
            # out.write(frame)
    # out.release()
    cap.release()
    cv2.destoryAllWindows()



if __name__ == "__main__":
    # gaosi("/Users/sonny_he/Desktop/旸谷项目/事件分析仪/无法检测视频分析/视频备份/paosa.264")
    three_frame_differencing("/Users/sonny_he/Desktop/旸谷项目/事件分析仪/无法检测视频分析/视频备份/paosa.264")