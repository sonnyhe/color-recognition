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

# diff = cv2.filter2D(img2, -1, kernel)
# Apply threshold to convert to binary image
threshold_value = 50
retval, binary_image = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)

# Smooth image using median blur
smoothed_image = cv2.medianBlur(binary_image, 5)

# Save smoothed image
cv2.imwrite('result_diff_conv.png', smoothed_image)
