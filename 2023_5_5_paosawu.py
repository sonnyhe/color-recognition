import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
# Load images as grayscale
list_result = []
def icc_pic(img_gray, template_gray, x, y, img):

    # 计算匹配结果矩阵
    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_SQDIFF_NORMED)
    # 获取匹配结果的最大值和最小值
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val, min_loc, max_loc)
    # 在大图像上绘制矩形框标记匹配位置
    top_left = max_loc
    # print(max_val/255)
    threshold = 10
    format_string = "{:.4f}"
    text = "%d"%(max_val*1000)
    val = int(text)
    list_result.append(max_val)

    # print(list_result)
    if val > threshold:
        # print("匹配")
        # threshold = 0.6
       #  similarity[top_left > threshold] = 1
        # similarity[top_left <= threshold] = 0
        bottom_right = (x + template_gray.shape[1], y + template_gray.shape[0])
        cv2.putText(img, text, (x +10, y +10), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255), 1)
        cv2.rectangle(img, (x,y), bottom_right, (0,0,255), 2)

def ssim_pic(img1_gray, img2_gray):

    ssim_value = compare_ssim(img1_gray, img2_gray, channel_axis = None)
    return ssim_value

def mse_pic(img1, img2):

    mse = ((img1 - img2) ** 2).mean()
    return mse

# 定义滑动窗口分块函数
def sliding_window(image, block_size, step_size):
    # 获取图像的宽度和高度
    h, w = image.shape[:2]
    # 定义一个空列表，用于保存所有分块图像块
    blocks = []

    # 通过两重循环遍历整个图像，每次截取一个分块大小的图像块，将其保存到列表中
    for y in range(0, h - block_size[1] + 1, step_size[1]):
        for x in range(0, w - block_size[0] + 1, step_size[0]):
            block = image[y:y + block_size[1], x:x + block_size[0]]
            blocks.append(block)

    # 返回所有分块图像块的列表
    return blocks

def hist(block1, block2):
            # 计算当前小块的相似度
        # diff = cv2.absdiff(block1, block2)
        hist1 = cv2.calcHist([block1], [0], None, [8], [0, 256])
        hist2 = cv2.calcHist([block2], [0], None, [8], [0, 256])
        # similarity[i, j] = compare_ssim(block1, block2, channel_axis = None)
def pic_fillpoly(img):
    black_image = np.zeros_like(img)
    pts = np.array([[0, 1080], [390, 1080], [1215,278], [1350, 278], [1500, 1080], [1920, 1080], [1920, 0], [0, 0]])
    
    pts3 = np.array([[0, 1080], [1920, 1080], [1920, 980], [0, 980]])
    pts2 = np.array([[980,1080], [1100, 1080], [1340,178],[1325,178]])
    
    
    cv2.fillPoly(black_image, [pts], (255, 255, 255))
    cv2.fillPoly(black_image, [pts2], (255, 255, 255))
    cv2.fillPoly(black_image, [pts3], (255, 255, 255))
    result = cv2.addWeighted(img, 1, black_image, 1, 0)
    # cv2.fillPoly(img, [pts1], (0), 8, 0)
    return result

img1 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/15432-0003.png')
img2 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/15432.png')


gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# 定义仿射变换矩阵
warp_mode = cv2.MOTION_TRANSLATION
warp_matrix = np.eye(2, 3, dtype=np.float32)

# 寻找最佳的仿射变换矩阵
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000,  1e-10)
cc, warp_matrix = cv2.findTransformECC(gray1, gray2, warp_matrix, warp_mode, criteria)
# cc, warp_matrix = cv2.findTransformECC(gray1, gray2, warp_matrix, warp_mode, criteria)

# 对图像进行仿射变换
rows, cols, _ = img2.shape# 彩色图像通道
img_aligned = cv2.warpAffine(img2, warp_matrix, (cols, rows), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
# img_aligned = cv2.warpAffine(img2, warp_matrix, (img1.shape[0], img1.shape[1]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)灰度图
img_aligned = pic_fillpoly(img_aligned)
# cv2.imwrite("img_aligned.png", img_aligned)
img1 = pic_fillpoly(img1)
img3 = img2.copy()

cv2.imwrite("img1.png", img1)
cv2.imwrite("img2.png", img_aligned)
# 滑动窗口的大小
win_size = 30
step_size = 20
# 计算图像的大小
h, w = img1.shape[:2]
# 计算分割成的小块的数量
n_blocks_h = h // win_size
n_blocks_w = w // win_size

# 分割图像为小块并计算相似度
similarity = np.zeros((n_blocks_h, n_blocks_w), dtype=np.float32)

for i in range(n_blocks_h):
    for j in range(n_blocks_w):
        # 计算当前小块的位置
        x = j * win_size
        y = i * win_size
        # 截取小块
        block1 = img1[y:y+win_size, x:x+win_size]
        block2 = img_aligned[y:y+win_size, x:x+win_size]
        # 计算当前小块的相似度
        icc_pic(block1, block2, x, y, img3)

cv2.imshow(img3)
cv2.waitKey(0)