import cv2
import numpy as np
img = cv2.imread("my1.png")
h,w = img.shape[0:2]
for i in range(3000):
    x = np.random.randint(0, h)
    y = np.random.randint(0, w)
    img[x, y,:] = 255
result = cv2.boxFilter(img, -1, (5, 5), normalize=1)
result1 = cv2.boxFilter(img, -1, (5, 5), normalize=0)
cv2.imshow("src", img)
cv2.imshow("junyihua", result)
cv2.imshow("meijuniyhua", result1)
cv2.waitKey(0)