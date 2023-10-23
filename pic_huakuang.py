import cv2
import numpy as np

def icc_pic(img_gray, template_gray, x, y, img3, num):

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
        print("大于阈值", val)
        # log.error(val)
        # threshold = 0.6
    #  similarity[top_left > threshold] = 1
        # similarity[top_left <= threshold] = 0
        bottom_right = (x + template_gray.shape[1], y + template_gray.shape[0])
        cv2.putText(img3, text, (x +10, y +10), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255), 1)
        cv2.rectangle(img3, (x,y), bottom_right, (0,0,255), 2)
        num += 1
    return num, img3


def pic_fillpoly(img):

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    black_image = np.zeros_like(img) #返回一个跟img相同shape的0矩阵
    pts = np.array([[0, 1080], [390, 1080], [1215,278], [1390, 278], [1630, 1080], [1920, 1080], [1920, 0], [0, 0]])# 圈起来的剩下地方为要使用的地方
    pts3 = np.array([[0, 1080], [1920, 1080], [1920, 980], [0, 980]])# 圈起来的剩下地方为要使用的地方，圈起来的地方为单色，白色或黑色
    pts2 = np.array([[980,1080], [1100, 1080], [1340,178],[1325,178]])# 圈起来的剩下地方为要使用的地方，圈起来的地方为单色，白色或黑色
    pts4 = np.array([[1354,707], [1520, 707], [1520,765],[1354,765]])
    pts5 = np.array([[1489, 633],[1493,661],[1542, 659],[1536,632]])
    pts6 = np.array([[1048,534],[1046,568],[1141,565],[1147,536]])
    pts7 = np.array([[1180,358],[1229,352],[1228,349],[1180,350]])
    pts8 = np.array([[1438,699],[1464,697],[1463,678],[1439,680]])
    pts9 = np.array([[1416,535],[1445,531],[1442,554],[1418,558]])
    pts10 = np.array([[701,765],[1134,786],[1027,1053],[426,1035]])
    pts11 = np.array([[1314,912],[1314,935],[1342,935],[1346,911]])
    pts12 = np.array([[1475,600],[1476,653],[1573,650],[1571,581]])
    pts13 = np.array([[1163,863],[1157,924],[1211,925],[1221,869]])
    pts14 = np.array([[1493,744],[1489,789],[1528,788],[1533,756]])
    pts15 = np.array([[1256,858],[1256,887],[1297,885],[1303,857]])
    # pts16 = np.array([[1048,541],[1045,564],[1099,566],[1102,543]])
    # cv2.fillPoly(black_image, [pts], (255, 255, 255))
    # cv2.fillPoly(black_image, [pts2], (255, 255, 255))
    # cv2.fillPoly(black_image, [pts3], (255, 255, 255))
    
    cv2.fillPoly(black_image, [pts], (255))
    cv2.fillPoly(black_image, [pts2], (255))
    cv2.fillPoly(black_image, [pts3], (255))
    cv2.fillPoly(black_image, [pts4], (255))
    cv2.fillPoly(black_image, [pts5], (255))
    cv2.fillPoly(black_image, [pts6], (255))
    cv2.fillPoly(black_image, [pts7], (255))
    cv2.fillPoly(black_image, [pts8], (255))
    cv2.fillPoly(black_image, [pts9], (255))
    cv2.fillPoly(black_image, [pts10], (255))
    cv2.fillPoly(black_image, [pts11], (255))
    cv2.fillPoly(black_image, [pts12], (255))
    cv2.fillPoly(black_image, [pts13], (255))
    cv2.fillPoly(black_image, [pts14], (255))
    cv2.fillPoly(black_image, [pts15], (255))
    # cv2.fillPoly(black_image, [pts16], (255))
    result = cv2.addWeighted(img, 1, black_image, 1, 0)# 把2张图像按照系数相加
    # cv2.fillPoly(img, [pts1], (0), 8, 0)
    cv2.imwrite("pic_huakuang_fillpoly.png", result)
    return result


paosawu_backgroud = "15432-0003.png"

# 背景图
img1 = cv2.imread(paosawu_backgroud)
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# gray1_now = pic_fillpoly(gray1)

# cv2.imwrite("gray_now.png", gray1_now)
#  cv2.imwrite("img2.png", img_aligned)
# 滑动窗口的大小
win_size = 30
step_size = 20
# 计算图像的大小
h, w = gray1.shape[:2]
# 计算分割成的小块的数量
n_blocks_h = h // win_size
n_blocks_w = w // win_size
img2 = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/2023_10_16_14_06_53_963746.png")
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
img_aligned = pic_fillpoly(gray2)

gray1_after = gray1.copy()
gray1_now = pic_fillpoly(gray1_after)

img3 = img2.copy()
# paosa_data = {}
num = 0
for i in range(n_blocks_h):
    for j in range(n_blocks_w):
        # 计算当前小块的位置
        x = j * win_size
        y = i * win_size
        # 截取小块
        block1 = gray1_now[y:y+win_size, x:x+win_size]
        block2 = img_aligned[y:y+win_size, x:x+win_size]
        # 计算当前小块的相似度
        num, img3 = icc_pic(block1, block2, x, y, img3, num)
if num:
    cv2.imwrite("fill_result.png", img3)