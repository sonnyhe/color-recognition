import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
# Load images as grayscale
img1 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/15432-0003.png')
img2 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/13409.jpg')


img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

pts1 = np.array([[0, 1080], [390, 1080], [1215, 278], [1400, 278], [1730, 1080], [1920, 1080], [1920, 0], [0,0]])
pts2 = np.array([[980,1080], [1100, 1080], [1340,178],[1325,178]])
pts3 = np.array([[0, 1080], [1920, 1080], [1920, 980], [0, 980]])

cv2.fillPoly(img1, [pts2], (255), 8, 0)
cv2.fillPoly(img1, [pts1], (255), 8, 0)

cv2.imwrite("img1.png", img1)
cv2.fillPoly(img2, [pts2], (255), 8, 0)
cv2.fillPoly(img2, [pts1], (255), 8, 0)

cv2.imwrite("img2.png", img2)
img3 = img2
# 滑动窗口的大小
win_size = 30
# 计算图像的大小
h, w = img1.shape
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
        block2 = img2[y:y+win_size, x:x+win_size]

        # 计算当前小块的相似度
        # diff = cv2.absdiff(block1, block2)
        hist1 = cv2.calcHist([block1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([block2], [0], None, [256], [0, 256])
        # similarity[i, j] = compare_ssim(block1, block2, channel_axis = None)
        similarity[i, j] = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        print(similarity[i,j])
        # similarity[i, j] = (similarity[i, j] + 1) * 0.5
        # print(similarity[i, j])

# 将相似度大于0.5的小块设为1，否则设为0
threshold = 0.87
similarity[similarity > threshold] = 1
similarity[similarity <= threshold] = 0

# 拼接小块得到整个图像
result = np.zeros((h, w), dtype=np.uint8)
for i in range(n_blocks_h):
    for j in range(n_blocks_w):
        # 计算当前小块的位置
        x = j * win_size
        y = i * win_size

        # 将当前小块的值拷贝到整个图像中
        result[y:y+win_size, x:x+win_size] = similarity[i, j] * 255

contours,_ =cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    # 判断矩形是否满足条件
if contours:
    for contour in contours:
        x,y,w,h=cv2.boundingRect(contour)
        if 50 < cv2.contourArea(contour) < 10000:
            cv2.rectangle(img3,(x,y),(x+w,y+h),(255,255,0),2)
            # cv2.imshow('image',img1)    # 读下一帧

# 输出结果图像
cv2.imwrite('result——hist_init.png', result)
cv2.imwrite('result——hist_img2.png', img3)