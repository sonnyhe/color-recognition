import cv2
from datetime import datetime
import numpy as np



def icc_pic(img_gray, template_gray, x, y, img, num):

    # 计算匹配结果矩阵
    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_SQDIFF_NORMED)
    # 获取匹配结果的最大值和最小值
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #(min_val, max_val, min_loc, max_loc)
    # 在大图像上绘制矩形框标记匹配位置
    top_left = max_loc
    # print(max_val/255)
    threshold = 10
    format_string = "{:.4f}"
    text = "%d"%(max_val*1000)
    val = int(text)
    # list_result.append(max_val)
    paosa_data = {}
    # print(list_result)
    if val > threshold:
        # print("匹配")
        # threshold = 0.6
    #  similarity[top_left > threshold] = 1
        # similarity[top_left <= threshold] = 0
        bottom_right = (x + template_gray.shape[1], y + template_gray.shape[0])
        cv2.putText(img, text, (x +10, y +10), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255), 1)
        cv2.rectangle(img, (x,y), bottom_right, (0,0,255), 2)
        num += 1
    return num, img

def pic_fillpoly(img):
    black_image = np.zeros_like(img) #返回一个跟img相同shape的0矩阵
    pts = np.array([[0, 1080], [390, 1080], [1215,278], [1350, 278], [1500, 1080], [1920, 1080], [1920, 0], [0, 0]])# 圈起来的剩下地方为要使用的地方
    pts3 = np.array([[0, 1080], [1920, 1080], [1920, 980], [0, 980]])# 圈起来的剩下地方为要使用的地方，圈起来的地方为单色，白色或黑色
    pts2 = np.array([[980,1080], [1100, 1080], [1340,178],[1325,178]])# 圈起来的剩下地方为要使用的地方，圈起来的地方为单色，白色或黑色
    
    # cv2.fillPoly(black_image, [pts], (255, 255, 255))
    # cv2.fillPoly(black_image, [pts2], (255, 255, 255))
    # cv2.fillPoly(black_image, [pts3], (255, 255, 255))
    
    cv2.fillPoly(black_image, [pts], (255))
    cv2.fillPoly(black_image, [pts2], (255))
    cv2.fillPoly(black_image, [pts3], (255))
    result = cv2.addWeighted(img, 1, black_image, 1, 0)# 把2张图像按照系数相加
    # cv2.fillPoly(img, [pts1], (0), 8, 0)
    return result


def two_pic_compare(gray1, gray1_after, img2, n_blocks_h, n_blocks_w, win_size):
    
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # 定义仿射变换矩阵
    warp_mode = cv2.MOTION_TRANSLATION
    warp_matrix = np.eye(2, 3, dtype=np.float32)

    # 寻找最佳的仿射变换矩阵
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000,  1e-10)
    print("paosawu is running")
    # try:
    if True:
        cc, warp_matrix = cv2.findTransformECC(gray1, gray2, warp_matrix, warp_mode, criteria)
        num = 0
        # 对图像进行仿射变换
        # rows, cols, _ = img2.shape# 彩色图像通道
        rows, cols = gray2.shape[:2]
        # img_aligned = cv2.warpAffine(img2, warp_matrix, (cols, rows), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        img_aligned = cv2.warpAffine(gray2, warp_matrix, (cols, rows),  flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)#灰度图
        img_aligned = pic_fillpoly(img_aligned)
        ids = [((1570, 683), (1733, 1080)), ((1329, 187), (1345, 219)), ((1, 584), (326, 843)), ((1298, 328), (1466, 475))]
        print(ids)
        if ids:
            for i in range(len(ids)):
                point1 = (int((ids[i][0][0])*(0.9)), int((ids[i][0][1])*(0.9)))
                point2 = (int((ids[i][1][0])*(1.1)), int((ids[i][1][1])*(1.1)))
                
                cv2.rectangle(gray1_after,point1,point2,1,-1)
                cv2.rectangle(img_aligned,point1,point2,1,-1)
        # cv2.imwrite("img_aligned.png", img_aligned)
        # point1 = (100,200)
        # point2 = (200,300)
        # cv2.rectangle(gray1_after,point1,point2,0,-1)
        # cv2.rectangle(img_aligned,point1,point2,0,-1)
        cv2.imwrite("gray1_after.png", gray1_after)
        cv2.imwrite("img_aligned.png", img_aligned)
        img3 = img2.copy()
        # paosa_data = {}
        for i in range(n_blocks_h):
            for j in range(n_blocks_w):
                # 计算当前小块的位置
                x = j * win_size
                y = i * win_size
                # 截取小块
                block1 = gray1_after[y:y+win_size, x:x+win_size]
                block2 = img_aligned[y:y+win_size, x:x+win_size]
                # 计算当前小块的相似度
                num , img3 = icc_pic(block1, block2, x, y, img3, num)

        if True:
            # paosa_data["paosawu"] = 20
            # paosa_data["camera"] = "road1"
            # paosa_data["ip"] = "192.168.1.1"
            dt_ms = datetime.now().strftime('%Y-%m-%d-%H_%M_%S_%f')# 获取当前时间
            # paosa_data["send_time"] = dt_ms
            # client_loss_incident_data(str(paosa_data))
            # image_path = "/home/digital/digital_twin_django/media/images/"
            # video_path = "/home/digital/digital_twin_django/media/videos/192_168_9_204/"
            # paosa_path = image_path + "pic/paosawu/%s.png"%dt_ms
            name = "警告！！！有抛洒物"
            print("warning")
            # img = cv2ImgAddText(img3, name, 1000, 249, textColor=(255,0,0), textsize=50)
            # img = cv2.resize(img, (960, 640), interpolation=cv2.INTER_LINEAR)
            
            cv2.imwrite("haha.png", img3)
            cv2.imshow("test", img3)
            # cv2.waitKey(100)


    # except:
    #     # print("warning: ecc did not converge")
    #     log.warning("warning: ecc did not converge")


def Loss_incident_new():

    paosawu_backgroud = "/Users/sonny_he/Desktop/opencv_learning/15432-0003.png"
    
    # 背景图
    img1 = cv2.imread(paosawu_backgroud)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # img1 = pic_fillpoly(img1)

    gray1_after = pic_fillpoly(gray1)

    # cv2.imwrite("img1.png", img1)
    #  cv2.imwrite("img2.png", img_aligned)
    # 滑动窗口的大小
    win_size = 30
    step_size = 20
    # 计算图像的大小
    h, w = gray1.shape[0], gray1.shape[1]
    # h, w, _ = img1.shape
    # 计算分割成的小块的数量
    n_blocks_h = h // win_size
    n_blocks_w = w // win_size

    # 分割图像为小块并计算相似度
    # similarity = np.zeros((n_blocks_h, n_blocks_w), dtype=np.float32)
    # while True:
        # if all_dict_from_url:
            # id_list = []
            # for i in range(len(all_dict_from_url["from_url"])): # 当前共有几个id
            #     id_list.append(all_dict_from_url["from_url"][i]["id"])# 访问字典对象中的值
            # if post_id in id_list: # 是否在上一秒的id组中
            #     # print("normal\n\n\n")
            #     # print("post_id is :", post_id)
            #     position = id_list.index(post_id)# 计算在当前列表中的序号

            #     if all_dict_from_url["from_url"][position]["enable"]:# 获取当前id的算法运算状态，true或false
            #         data = False
                    # while True:
                        # if "inference_pic" in all_items:# 判断是否有数据
                            # print(all_items)
    print("runing")
    img2_path = "/Users/sonny_he/Desktop/opencv_learning/15432.png"
    img2 = cv2.imread(img2_path)
    two_pic_compare(gray1, gray1_after, img2, n_blocks_h, n_blocks_w, win_size)


if __name__ == "__main__":
    Loss_incident_new()