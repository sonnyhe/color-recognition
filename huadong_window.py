from PIL import Image
from scipy.signal import convolve2d
import numpy as np

# 读取图片
img1 = Image.open("/Users/sonny_he/Desktop/opencv_learning/15432-0002.jpg")
img2 = Image.open("/Users/sonny_he/Desktop/opencv_learning/15432-0003.png")

# 将图片转换为灰度图像
img1_gray = img1.convert('L')
img2_gray = img2.convert('L')

# 将图像转换为numpy数组
arr1 = np.array(img1_gray)
arr2 = np.array(img2_gray)

# 定义卷积核
kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])

# 使用卷积核对两张图片进行卷积运算，得到两张图片的区别
result = np.abs(convolve2d(arr1, kernel) - convolve2d(arr2, kernel))

# 将结果转换为PIL Image对象，并保存为图片
result_img = Image.fromarray(result.astype('uint8'))

result_img.save('result.png')