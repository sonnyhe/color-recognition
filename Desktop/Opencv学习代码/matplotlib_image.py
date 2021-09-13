import cv2
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] #显示中文
# 读取图像
img = cv2.imread("my.jpg")
# 图像格式转换
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)# BGR转换为RGB显示格式
# 显示图像
plt.imshow(img1)
plt.axis("off")
plt.title('sonny')# 图像标题
plt.show()
# 注意：OpneCv读取的图像格式是BGR格式的，而matplotlib显示图像是以RGB格式进行显示，
# 所以，我们需要对图像进行格式转化，从BGR通道转为RGB通道格式，这样显示出来才不会有色差

# 图像保存函数cv2.imwrite(filepath, img, num)
import cv2
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] #显示中文
# 读取图像
img = cv2.imread("my.jpg")
# 保存图像
cv2.imwrite("1.jpg", img)
# 读取保存后的图像
a = cv2.imwrite("1.jpg")
# 图像格式转换
img1 = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
plt.imshow(img1)
plt.axis('off')# 关闭坐标轴，设置为on则表示开启坐标轴
plt.title('sonny')
plt.show()