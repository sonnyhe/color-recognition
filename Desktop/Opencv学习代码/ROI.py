import cv2
import matplotlib.pyplot as plt

img = cv2.imread("/Users/sonny_he/Desktop/1.png")
# cv2.imshow('initial',img)
# 3 通道获取
B = img[:,:,0]
G = img[:,:,1]
R = img[:,:,2]
#打印3通道
print('B',B)
print('G', G)
print("R",R)

#通道合并
img2 = cv2.merge([B,G,R ])
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
plt.imshow(img2)
plt.title('tongaohebing')
plt.axis('off')
plt.show()
# 获取图像的尺寸和通道数
h,w,channel=img.shape
print(h,w,channel)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
B =cv2.cvtColor(B, cv2.COLOR_BGR2RGB)
G = cv2.cvtColor(G, cv2.COLOR_BGR2RGB)
R = cv2.cvtColor(R, cv2.COLOR_BAYER_BG2BGR)

img1 = img[200:400, 200:500]
# img[:200,:300]=img1

titles = ['initial imag', 'ROI region', 'Btongdao', 'Gtongdao', 'Rtongdao']
images = [img, img1, B,G,R]
for i in range(2):
    plt.subplot(1,2,i+1)
    plt.imshow(images[i])
    plt.title(titles[i])
    plt.axis('off')
plt.show()