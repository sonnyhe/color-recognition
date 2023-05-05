import cv2
import numpy as np

# Load images as grayscale
img1 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/15432-0003.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('/Users/sonny_he/Desktop/opencv_learning/paosa_1.png', cv2.IMREAD_GRAYSCALE)


# Define kernel for convolution
kernel = np.ones((3,3), np.float32) / 9

# Convolve images with kernel
convolved1 = cv2.filter2D(img1, -1, kernel)
convolved2 = cv2.filter2D(img2, -1, kernel)

# Compute absolute difference between convolved images
diff = cv2.absdiff(convolved1, convolved2)

# Apply threshold to convert to binary image
threshold_value = 30
retval, binary_image = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)
# 腐蚀操作
erosion_size = 2
erosion_kernel = np.ones((erosion_size, erosion_size), np.uint8)
erosion = cv2.erode(binary_image, erosion_kernel, iterations=1)

# 膨胀操作
dilation_size = 2
dilation_kernel = np.ones((dilation_size, dilation_size), np.uint8)
dilation = cv2.dilate(erosion, dilation_kernel, iterations=1)

# 滤波操作
filtered = cv2.filter2D(dilation, -1, kernel)
# Smooth image using Gaussian blur
smoothed_image = cv2.GaussianBlur(filtered, (5,5), 0)
mask = np.zeros((1080, 1920), dtype=np.uint8)

# pts = np.array([[0, 1080], [0, 965], [1420,300], [1755, 300], [1755, 1080], [1920, 1080]])
# pts1 = np.array([[360, 1080], [1316, 178], [1367, 178], [1829, 1080]])
pts = np.array([[0, 1080], [390, 1080], [1215,278], [1400, 278], [1730, 1080], [1920, 1080], [1920, 0], [0, 0]])

pts1 = np.array([[390, 1080], [1215, 278], [1400, 278], [1730, 1080]])
cv2.fillPoly(mask, [pts1], (255), 8, 0)
cv2.fillPoly(mask, [pts], (255), 8, 0)
while True:

        # 用0填充多边形
        # cv2.fillPoly(mask, [pts2], (255), 8, 0)
        # 位与运算
        result = cv2.bitwise_and(smoothed_image, smoothed_image, mask=mask)
        # cv2.imshow('dilated',dilated)    # 获取轮廓
        contours,_ =cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    # 判断矩形是否满足条件
        if contours:
            for contour in contours:
                x,y,w,h=cv2.boundingRect(contour)
                if 100 < cv2.contourArea(contour) < 5000:
                    cv2.rectangle(img2,(x,y),(x+w,y+h),(255,255,0),2)
                    # cv2.imshow('image',img1)    # 读下一帧
                    loss_incident_situ = True
            # dt_ms = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') # 获取当前时间
            # path = "/home/HwHiAiUser/mxVision-2.0.4.6/samples/mxVision/python/pic/car/%s.png"%dt_ms
            # cv2.imwrite(path, img)

        cv2.imshow("diff", diff)
        cv2.imshow("thresh", result)
        cv2.imshow("detection", img2)
        cv2.waitKey(27)
        # Save smoothed image
        # cv2.imwrite('result_opencv.png', smoothed_image)
