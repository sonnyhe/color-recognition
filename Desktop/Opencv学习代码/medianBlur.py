import cv2
import numpy as np
img = cv2.imread("my1.png")
h, w = img.shape[0:2]
for i in range(3000):
    x = np.random.randint(0, h)
    y = np.random.randint(0, w)
    img[x, y, :] = 255

result = cv2.medianBlur(img, 5)
cv2.imshow("src", img)
cv2.imshow("midianblur", result)
cv2.waitKey(0)