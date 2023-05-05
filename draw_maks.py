import numpy as np
import cv2


# masks = np.zeros((1080, 1920), np.uint8)
masks = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/15432-0003.png")
# for center in center_together:
'''for i in range(1920):
        for j in range(1080):
            if center[0][0]  < i < center[1][0] & center[1][1] < j < center[0][1]:
                masks[i][j] = 0'''
# 
pts1 = np.array([[0, 1080], [390, 1080], [1215, 278], [1400, 278], [1730, 1080], [1920, 1080], [1920, 0], [0,0]])
pts2 = np.array([[980,1080], [1100, 1080], [1340,178],[1325,178]])
pts3 = np.array([[0, 1080], [1920, 1080], [1920, 980], [0, 980]])
cv2.fillPoly(masks, [pts1], (0,0,0), 8, 0)
cv2.fillPoly(masks, [pts2], (0,0,0), 8, 0)
cv2.fillPoly(masks, [pts3], (0,0,0), 8, 0)
# mask = cv2.rectangle(masks,(100, 100), (200, 200), 255, 1 , 4)


cv2.imwrite('masks_test6.png',masks)