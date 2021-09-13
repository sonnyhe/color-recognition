import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("/Users/sonny_he/Desktop/1.png")
h,w = img.shape[0:2]

'''
channel blue
'''
# 获取通道B
B = img[:,:,0]
#将另外2通道设为0
G = np.zeros((h,w), dtype=img.dtype)
R = np.zeros((h,w), dtype=img.dtype)
# 合并通道，只保留蓝色通道，其他通道置为0
img1 = cv2.merge([B, G, R])

'''
channel green
'''
# 获取绿色通道G
B1 = np.zeros((h,w), dtype=img.dtype)
G1 = img[:,:,1]
R1 = np.zeros((h, w), dtype=img.dtype)

img2 = cv2.merge([B1,G1,R1])

'''
channel red
'''
# 获取红色通道
B2 = np.zeros((h,w),dtype=img.dtype)
G2 = np.zeros((h,w),dtype=img.dtype)
R2 = img[:,:,2]
img3 = cv2.merge([B2,G2,R2])

img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)

# show image
titles = ['Btongdao', 'Gtongdao', 'Rtongdao']
images = [img1, img2, img3]
for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.imshow(images[i])
    plt.title(titles[i])
    plt.axis('off')
plt.show()