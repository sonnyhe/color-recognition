import cv2
import numpy as np
import matplotlib.pyplot as plt

#read first image
img = cv2.imread("/Users/sonny_he/Desktop/1.png")
'''
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.cvtColor(gray,cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.title('gray')
plt.axis('off')
plt.show()'''
'''
h,w = img.shape[0:2]
# 自定义空白单通道图像，用于存放灰度图
gray = np.zeros((h,w),dtype=img.dtype)
#对原图进行遍历，然后分别对B/G/R按比例灰度化
for i in range(h):
    for j in range(w):
        gray[i, j] = 0.11*img[i, j, 0] + 0.59*img[i, j, 1] + 0.3*img[i, j, 2]#Y的物理意义是点的亮度，Y = 0.3R+0.59G+0.11R
gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
plt.imshow(gray)
plt.title("Y-亮度：灰度处理")
plt.axis('off')
plt.show()'''
''' max(B,G,R)
h,w = img.shape[0:2]
gray = np.zeros((h, w),dtype=img.dtype)
# 对原图像进行遍历，然后分别对B/G/R按比例灰度化
for i in range(h):
    for j in range(w):
        gray[i, j] = max(img[i,j,0], img[i,j,1], img[i,j,2])
gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
plt.imshow(gray)
plt.title('max gray')
plt.axis('off')
plt.show()'''

'''
平均值灰度化
gray[i, j] = (int(img[i, j, 0]) + int(img[i, j, 1]) + int(img[i, j, 2]))/3 求3通道平均值
'''
'''
Gamma矫正灰度化
a = img[i, j, 2]**(2,2)+1.5*img[i,j,1]**(2.2)+0.6*img[i,j,0]**(2.2)
b = 1+1.5**(2.2)+0.6**(2.2)
gray[i, j] = pow(a/b, 1.0/2.2)
'''
