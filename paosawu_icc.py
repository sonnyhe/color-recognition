import cv2
import numpy as np
import datetime
import socket

erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))


def pic_fillpoly(img):
    black_image = np.zeros_like(img)
    pts = np.array([[0, 1080], [390, 1080], [1215,278], [1350, 278], [1500, 1080], [1920, 1080], [1920, 0], [0, 0]])
    
    pts3 = np.array([[0, 1080], [1920, 1080], [1920, 980], [0, 980]])
    pts2 = np.array([[980,1080], [1100, 1080], [1340,178],[1325,178]])
    pts4 = np.array([[683*2, 359*2], [675*2, 378*2], [749*2, 378*2], [749*2, 359*2]])
    
    cv2.fillPoly(black_image, [pts], (255, 255, 255))
    cv2.fillPoly(black_image, [pts2], (255, 255, 255))
    cv2.fillPoly(black_image, [pts3], (255, 255, 255))
    cv2.fillPoly(black_image, [pts4], (255, 255, 255))
    
    result = cv2.addWeighted(img, 1, black_image, 1, 0)
    # cv2.fillPoly(img, [pts1], (0), 8, 0)
    return result

def fangshe(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 定义仿射变换矩阵
    warp_mode = cv2.MOTION_TRANSLATION
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    try:
    # 寻找最佳的仿射变换矩阵
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000,  1e-10)
        cc, warp_matrix = cv2.findTransformECC(gray1, gray2, warp_matrix, warp_mode, criteria)
        # cc, warp_matrix = cv2.findTransformECC(gray1, gray2, warp_matrix, warp_mode, criteria)

        # 对图像进行仿射变换
        rows, cols, _ = img2.shape# 彩色图像通道
        img_aligned = cv2.warpAffine(img2, warp_matrix, (cols, rows), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    except:
        img_aligned = img2
    return img_aligned




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
def icc_pic(img_gray, template_gray, x, y, img):

    # 计算匹配结果矩阵
    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_SQDIFF_NORMED)
    # print(img_gray)
    # print(template_gray)
    # print(res)
    # 获取匹配结果的最大值和最小值
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(min_val, max_val, min_loc, max_loc)
    # 在大图像上绘制矩形框标记匹配位置
    top_left = max_loc
    # print(max_val/255)
    threshold = 15
    format_string = "{:.4f}"
    text = "%d"%(max_val*1000)
    val = int(text)
    # list_result.append(max_val)
    # 定义列表
    # 使用.format()方法格式化输出
    # print(' '.join('{:15}'.format(i) for i in list_result))
    # print(max_val)
    # print("\r\n")


    # print(list_result)
    if val > threshold:
        # print("匹配")
        # threshold = 0.6
       #  similarity[top_left > threshold] = 1
        # similarity[top_left <= threshold] = 0
        bottom_right = (x + template_gray.shape[1], y + template_gray.shape[0])
        cv2.putText(img, text, (x +10, y +10), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255), 1)
        cv2.rectangle(img, (x,y), bottom_right, (0,0,255), 2)
        
    return img

def video_loss(img1, cap):


    # 滑动窗口的大小
    win_size = 30
    # 计算图像的大小
    h, w = img1.shape[:2]
    # 计算分割成的小块的数量
    n_blocks_h = h // win_size
    n_blocks_w = w // win_size

    # block_size = (win_size, win_size)
    # step_size = (win_size/2, win_size/2)

    # 分割图像为小块并计算相似度
    frame_count = 0
    similarity = np.zeros((n_blocks_h, n_blocks_w), dtype=np.float32)
    while True:
        ret,img2 = cap.read()
        frame_count+=1
        if ret:
            if frame_count % 5== 0:
                img_aligned = fangshe(img1, img2)
                img3 = img2.copy()
                img1 = pic_fillpoly(img1)
                img_aligned = pic_fillpoly(img2)
                
                for i in range(n_blocks_h):
                    for j in range(n_blocks_w):
                        # 计算当前小块的位置
                        x = j * win_size
                        y = i * win_size

                        # 截取小块
                        block1 = img1[y:y+win_size, x:x+win_size]
                        block2 = img_aligned[y:y+win_size, x:x+win_size]

                        # 计算当前小块的相似度
                        img3 = icc_pic(block1, block2, x, y, img3)

                cv2.imshow("detection", img3)
                cv2.waitKey(27)
        else:
            print("wrong")


if __name__ == '__main__':
    rtsp_url = "/Users/sonny_he/Desktop/Ascend_huawei/视频分析检测系统——送检/车检器视频/test.mp4"
    cap = cv2.VideoCapture(rtsp_url)
    # ids = redis()
    img1 = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/15432-0003.png")
    video_loss(img1, cap)
