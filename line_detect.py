from statistics import mean
import cv2
import numpy as np
import matplotlib.pyplot as plt

img=cv2.imread('/home/sunrise/Desktop/opencv_learning/te.jpg', cv2.IMREAD_GRAYSCALE)
img0 = cv2.imread('/home/sunrise/Desktop/opencv_learning/te.jpg', cv2.IMREAD_COLOR)
edge_img = cv2.Canny(img, 210, 300)

# plt.imshow(img)

mask = np.zeros_like(edge_img)
mask = cv2.fillPoly(mask, np.array([[[0, 460], [1150, 470], [780, 0], [650, 0]]]), color=255)
cv2.namedWindow('mask', 0)
cv2.resizeWindow('mask', 800, 1200)
cv2.imshow('mask', mask)
cv2.waitKey(0)

print("hello")
masked_edge_img = cv2.bitwise_and(edge_img, mask)


def calculate_slope(line):
    x_1, y_1, x_2, y_2 = line[0]
    return (y_2-y_1)/(x_2-x_1)

lines = cv2.HoughLinesP(masked_edge_img, 1, np.pi/180, 15, minLineLength=50, maxLineGap=20)
left_lines = [line for line in lines if calculate_slope(line)>0]
right_lines = [line for line in lines if calculate_slope(line)<0]

def reject_abnormal_lines(lines, threshold):
    slopes = [calculate_slope(line) for line in lines]
    while len(lines)>0:
        mean=np.mean(slopes)
        diff = [abs(s-mean) for s in slopes]
        idx = np.argmax(diff)
        if diff[idx] > threshold:
            slopes.pop(idx)
            lines.pop(idx)
        else:
            break
    return lines
print(len(left_lines), len(right_lines))

reject_abnormal_lines(left_lines, threshold=0.1)
reject_abnormal_lines(right_lines, threshold=0.1)
print(len(left_lines), len(right_lines))

def least_squares_fit(lines):
    x_coords = np.ravel([[line[0][0], line[0][2]] for line in lines])
    y_coords = np.ravel([[line[0][1], line[0][3]] for line in lines])
    poly = np.polyfit(x_coords, y_coords, deg=1)
    point_min = (np.min(x_coords), np.polyval(poly, np.min(x_coords)))
    point_max = (np.max(x_coords), np.polyval(poly, np.max(x_coords)))
    return np.array([point_min, point_max], dtype=np.int64)

left_lines = least_squares_fit(left_lines)
right_lines = least_squares_fit(right_lines)

cv2.line(img0, tuple(left_lines[0]), tuple(left_lines[1]), color = (0, 255, 255), thickness=5)
cv2.line(img0, tuple(right_lines[0]), tuple(right_lines[1]), color=(0, 255, 255), thickness=5)

cv2.namedWindow('lane', 0)
cv2.resizeWindow('lane', 800, 1200)
cv2.imshow('lane', img0)
cv2.waitKey(0)