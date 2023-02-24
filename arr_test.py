import cv2

ids_list = {'1': {'camera_name': 'camera', 'ID_num': 1, 'class': 0, 'center_coord': [1391, 719, (1213, 547), (1569, 891)], 'time': '2022-11-10 07:50:11.620946'}, '3': {'camera_name': 'camera', 'ID_num': 3, 'class': 0, 'center_coord': [1278, 251, (1258, 226), (1297, 277)], 'time': '2022-11-10 07:50:11.621120'}}
ids_person = [1, 2, 3]
ids_person_pre = [2]
if len(ids_person):
    # if len(ids_person_pre):
    for i in range(len(ids_person)):
        if ids_person[i] in ids_person_pre:
            print("person already exit")
        else:
            print("person detected")
            
point1 = ids_list["1"]["center_coord"][2]
point2 = ids_list["1"]["center_coord"][3]
img = cv2.imread("/Users/sonny_he/Desktop/opencv_learning/te.jpg")
cv2.rectangle(img, point1, point2, 255, 1)