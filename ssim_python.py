import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
from skimage.metrics import peak_signal_noise_ratio as compare_psnr

# 读取两张图像
img1 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/paosa_1.png')
img2 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/15432-0003.png')

img1 = cv2.resize(img1, (1920, 1080))
img2 = cv2.resize(img2, (1920, 1080))
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# 计算SSIM
ssim_value = compare_ssim(img1_gray, img2_gray, channel_axis = None)

print('SSIM value:', ssim_value)
