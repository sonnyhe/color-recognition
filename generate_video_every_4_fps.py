import cv2

# 打开视频文件
cap = cv2.VideoCapture('rtsp://192.168.9.87:8554/person.264')

# 获取帧率和总帧数等信息
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 创建 VideoWriter 对象，保存处理后的视频
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 25, (width, height))

# 处理视频每一帧
count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    count += 1
    # 只保留每4帧
    if count % 4 == 0:
        out.write(frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关闭所有对象
cap.release()
out.release()
cv2.destroyAllWindows()
