import cv2
import os
# cap = cv2.VideoCapture("rtsp://192.168.9.87:8554/mystream")
cap = cv2.VideoCapture(0)
# 设置编码类型为mp4
path = "/Users/sonny_he/Desktop/opencv_learning/save_file/"
filelist = os.listdir(path)
filelist = sorted(filelist)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# 得到摄像头拍摄的视频的宽和高
# 创建对象，用于视频的写出
videoWrite = cv2.VideoWriter('test1.avi', fourcc, 25, (640, 640))
 
'''for item in filelist:
    if item.endswith('.jpg'):
        # 将图片写入视频
        item = os.path.join(path, item)
        img = cv2.imread(item)
        videoWrite.write(img)'''
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if frame_count >= 2000:
        videoWrite.release()
        cap.release()
        cv2.destroyAllWindows() 
    if not ret:
        break
    frame_count += 1
    videoWrite.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break


# 刷新，释放资源
videoWrite.release()
cap.release()
cv2.destroyAllWindows()
