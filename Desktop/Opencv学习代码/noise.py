import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("/Users/sonny_he/Desktop/1.png")
h,w = img.shape[0:2]
for i in range(3000):
    x = np.random.randint(0, h)
    y = np.random.randint(0, w)
    img[x, y, :] = 255

img  = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.axis('off')
plt.savefig('my1.png')
plt.show()