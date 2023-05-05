import cv2
import numpy as np

# 读取图片
img1 = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/15432-0003.png")
img2 = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/15432-0002.png")


win_size = 30
# 计算图像的大小
h, w = 1080, 1920
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

        # 计算直方图
        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

        # 计算相似度
        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        print(similarity)
# 将相似度映射到0到1之间
similarity = 0.5 * (similarity + 1)

print("Similarity:", similarity)
