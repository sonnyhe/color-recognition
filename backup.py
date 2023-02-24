#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) Huawei Technologies Co., Ltd. 2020-2021. All rights reserved.
Description: main.
Author: MindX SDK
Create: 2021
History: NA
"""

# import StreamManagerApi.py
import argparse
import ast
import datetime
import json
import math
import os
import sys
import time
from enum import unique
from pickletools import read_string1
from symbol import return_stmt
import MxpiDataType_pb2 as MxpiDataType
# from turtle import distance
import cv2
import numpy as np
from StreamManagerApi import *
from utils import checkIntersect, generateLineMatric, generateNumMatric
from google.protobuf import json_format


stop_incident_count = 0
reverse_drive_incident_count = 0

stop_time_count = 500 #5000帧输出一次相同事件 
person_time_count = 500
car_nixing_count = 500


IDS_list = [0]
IDS_list_area_1 = [0]
IDS_list_area_2 = [0]

# global IDS_list

IDS_info = {0}
# car_stop_time = 0
# car_nixing_time = 0
# person_detect = 0

def Detect_object_situation(ids_area1, ids_area2, ids, data, IDS_info, IDS_list_area_1, IDS_list_area_2, IDS_list):# 车辆的交通事件分类
    car_stop, car_nixing, car_normal, car_leave, person_situation, car_leave_initial_road = None, None, None, None, None, None
    IDS_list_car_stop = []
    IDS_list_person = []
    IDS_list_car_nixing = []
    IDS_list_left_initial = []
    for i in range(len(ids)):
        if ids[i] in IDS_list:
            if IDS_info["%s"%ids[i]]["class"] == 3:
                person_situation = True
                IDS_list_car_stop.append(ids[i])
            if IDS_info["%s"%ids[i]]["center_coord"] == data["%s"%ids[i]]["center_coord"]:
               car_stop = True
               IDS_list_person.append(ids[i])
               # print("%s"%ids[i] + " is stop incident")
            elif IDS_info["%s"%ids[i]]["center_coord"][1] < data["%s"%ids[i]]["center_coord"][1]:
                car_nixing = True
                IDS_list_car_nixing.append(ids[i])
                # print("%s"%ids[i] + " is reverse drive incident")
            else:
                car_normal = True
                # print("%s"%ids[i] + " is normal")
        else:
            car_leave = True
            # print("%s"%ids[i] + " is leave")
    
    num1 = len(ids_area1)
    num2 = len(ids_area2)
    if num1:
        for i in range(num1):
            if ids_area1[i] in IDS_list_area_2:
                car_leave_initial_road = True
                print("%s"%ids_area1[i] + "is drive out of the border incident")
                IDS_list_left_initial.append(ids_area1[i])

    if num2:
        for i in range(num2):
            if ids_area2[i] in IDS_list_area_1:
                car_leave_initial_road = True
                print("%s"%ids_area2[i] + "is drive out of the border incident")
                IDS_list_left_initial.append(ids_area1[i])

    return car_stop, car_nixing, car_normal, car_leave, person_situation, car_leave_initial_road, IDS_list_car_stop, IDS_list_person, IDS_list_car_nixing, IDS_list_left_initial

def Store_det_msg(name, id, cls, center):# 存储检测信息
    det_msg = {}
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    det_msg['camera_name'] = name
    det_msg['ID_num'] = int(id)
    det_msg['class'] = int(cls)
    det_msg['center_coord'] = center
    det_msg['time'] = dt_ms
    # print(det_msg)
    return det_msg
    
def Mask_image(center):# 每个车生成矩阵
    masks = np.ones((1080, 1920), np.uint8)
    # for center in center_together:
    '''for i in range(1920):
            for j in range(1080):
                if center[0][0]  < i < center[1][0] & center[1][1] < j < center[0][1]:
                    masks[i][j] = 0'''
    mask = cv2.rectangle(masks,center[0], center[1], 255, 1 , 4)
    return mask

def Car_speed():
    for index in [0, 1]:
        if Intersect_1_Flag_Last[index] == False and Intersect_1_Flag[index] == True and first_Flag == False:  # 判断第二根线是否是上升沿
            # Car_Num_1[index] += 1
            class_car = self.which_car(index, frame)
            the_num = index_car[index]
            class_num = predictions["instances"].pred_classes.to('cpu')[the_num].item()
            
            if class_num == 3:
                continue
            else:
                self.DataCollect(index, Times_1[index], Speeds[index], Car_Num[index], class_car, class_num)# , producer)
                Car_Num_1[index] += 1
                # self.DetecFromOneFrame(carCount[index])
                # 根据第一根线数据计算车速等数据
                # 保存时间和坐标信息
            if videoMode == DetecConfig.VideoMode['FromFile']:  # 从视频文件读取
                Times_1[index] = 1.0 / fps * frame_count 
            if videoMode == DetecConfig.VideoMode['WebCom']:  # 从IP摄像头读取
                Times_1[index] = time.time()  # .........................待续
            for car in cars:
                if car.Intersect_1[index] == True:
                    Cars_1[index] = car  #
                                                    
            Speeds[index] = self.CalCarSpeed(Cars[index], Cars_1[index], Times[index],
                                            Times_1[index])  # 计算车速，并返回结果


            Intersect_1_Flag_Last[index] = Intersect_1_Flag[index]

            if Intersect_Flag_Last[index] == False and Intersect_Flag[index] == True:  # 判断第一根线是否是上升沿
                Car_Num[index] += 1

                first_Flag = False  # 标志不是第一次了
                    # 保存时间和坐标信息
                if videoMode == DetecConfig.VideoMode['FromFile']:  # 从视频文件读取
                    Times[index] = 1.0 / fps * frame_count  #
                if videoMode == DetecConfig.VideoMode['WebCom']:  # 从IP摄像头读取
                    Times[index] = time.time()  # .........................待续
                for car in cars:
                    if car.Intersect[index] == True:
                        Cars[index] = car  #

                # self.SaveFlowData(index, 1) # 第一根线数据暂不保存
            Intersect_Flag_Last[index] = Intersect_Flag[index]

def Loss_incident(success, cam, img1, img2):# 抛洒物事件
    # init_pic_background = ""
    
    loss_incident_situ = False
    while success:    # 获得两帧之间的差异    
        diff=cv2.absdiff(img1,img2)    
        # cv2.imshow('diff',diff)    # 图像处理：灰度，高斯模糊，二值化    
        gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)    
        blur=cv2.GaussianBlur(gray,(5,5),0)    
        _,th=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)    # 图像膨胀操作    
        dilated=cv2.dilate(th,None,iterations=3)    
        # cv2.imshow('dilated',dilated)    # 获取轮廓        
        contours,_=cv2.findContours(dilated,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    # 判断矩形是否满足条件    
        for contour in contours:        
            (x,y,w,h)=cv2.boundingRect(contour)        
            if cv2.contourArea(contour) <700:            
              continue        
            else:            
                # cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),1)    
                # cv2.imshow('image',img1)    # 读下一帧   
                loss_incident_situ = True 
                img1=img2    
                _,img2=cam.read()    
                flag=cv2.waitKey(100)    
                if flag==ord('q'):        
                    break# 别忘记释放摄像头
    return loss_incident_situ

def Area_detect(x, y, id, ids_area1, ids_area2, ids):# 车道区域划分
    y1 = 1.9636*x - 2513.4
    y2 = -3*x + 4215
    y3 = -0.939*x + 1417.89

    if y >= y3:
            if y >= y1: # 检测是否在待识别区 
                ids.append(id)
                if y >= y2: # 检测具体区域
                    ids_area2.append(id)# 区域 2
                else:
                    ids_area1.append(id)# 区域 1
            return x, y, id, ids_area1, ids_area2, ids
    else:
        return None, None, id, ids_area1, ids_area2, ids

def DetecFromOneFrame(line_up, line_down, center_together,):# 得到车辆与划定区域之间是否相交信息
    carCount = [0, 0]
    # routeNum = [0,1]
    index_car = [None, None]
    # bbox_xcycwh, cls_conf, cls_ids, prediction = predict.detect(frame)  # 获取预测结果
    if center_together:
        masks = np.zeros((1080, 1920), np.uint8)
        # carCount = [0, 0]  # 车道实时的车数
        car_bbox_center_down = None
        car_bbox_center_up = None
        # print(center_together)
        for center in center_together:
            masks= Mask_image(center)
            # routeNum = center[2]
            Intersect_up_Flag = [False, False]  # 与第一根线是否相交标识符
            Intersect_down_Flag = [False, False]  # 与第二根线是否相交标识符
            routeNum = int(center[2]) - 1
            if routeNum is not None:
                carCount[routeNum] += 1  # 车道车辆总数加1
                if checkIntersect(masks, line_up):
                    Intersect_up_Flag[routeNum] = True
                    car_bbox_center_up = center[4]
                    # car.Intersect[routeNum] = True
                if checkIntersect(masks, line_down):
                    Intersect_down_Flag[routeNum] = True
                    car_bbox_center_down = center[4]
                    index_car[routeNum] = center[3]
                    # car.Intersect_1[routeNum] = True

        return carCount, Intersect_up_Flag, Intersect_down_Flag, index_car, car_bbox_center_up, car_bbox_center_down
    else:
        return carCount, None, None, None, None, None

def DataCollect(routeNum, Speeds, carCount, car_type): # 每辆车的属性信息，包括车道，车辆类型，车速，实时在途车数，时间等信息
        # 准备发送车道上车辆的速度，数量信息到Kafka
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') # 获取当前时间
        camera_data = {} 
        if routeNum==0:        # 1车道信息
            # 左侧车道编码为0
            camera_data['road'] = 0
            camera_data['car_class'] = car_type
            # camera_data['car_color'] = class_car
            # 左侧车道车速
            camera_data['car_speed'] = Speeds
            # 左侧车道实时车数
            camera_data['car_count'] = carCount
            # key = "4276adf0-a158-37bd-be4d-71dc6d1fa6f4-L"

        elif routeNum==1:       # 2车道信息
            camera_data['road'] = 1
            camera_data['car_class'] = car_type
            # camera_data['car_color'] = class_car

            camera_data['car_speed'] = Speeds
            # 左侧车道实时车数
            camera_data['car_count'] = carCount
            # key = "4276adf0-a158-37bd-be4d-71dc6d1fa6f4-M"

        # 摄像头编号，收集信息时间
        camera_data['camera'] = 'video_Name'
        camera_data['time'] = dt_ms
        print(camera_data)

def CalCarSpeed(car1, car2, time1, time2):# 计算平均车速
        # points_or = np.float32([[[car1[0], car1[1]], [[car2[0], car2[1]]]]
        # points_perspective = cv2.perspectiveTransform(points_or, np.float32(self.cfg['Matrix_Trans']))
        # distance = math.sqrt(
            # math.pow(points_perspective[0][0][0] - points_perspective[1][0][0], 2) +
            # math.pow(points_perspective[0][0][1] - points_perspective[1][0][1], 2))
        # time = time2 - time1
        # print(type((time)))
        distance = 7
        time_diff = time2 - time1
        speed = distance / time_diff
        # speed = (distance * cfg['Para_Distance'] / 100) //(
                    # time) * 3.6  # 变换后，1像素代表1cm;self.cfg.Para_Distance用于调整距离比例
        return round(int(speed)), time_diff

def Traffic_parameter(Intersect_up_Flag, Intersect_down_Flag, index_car, car_bbox_center_up, car_bbox_center_down, first_Flag, Time_plus):# 计算车辆的交通参数
    for index in [0, 1]:
        if Intersect_down_Flag_Last[index] == False and Intersect_down_Flag[index] == True and first_Flag == False:  # 判断第二根线是否是上升沿

            Car_num_down[index] += 1
            # self.DetecFromOneFrame(carCount[index])
            # 根据第一根线数据计算车速等数据
            # 保存时间和坐标信息
            Times_down[index] = time.time()  # .........................待续
            car_type = index_car[index]
            # for car in cars:
                # if car.Intersect_1[index] == True:
                    # Cars_1[index] = car  #
                    
            Speeds[index], Time_plus[index] = CalCarSpeed(car_bbox_center_up[index], car_bbox_center_down[index], Times_up[index],
                                            Times_down[index])  # 计算车速，并返回结果
            DataCollect(index, Speeds, Car_num_down, car_type)

        Intersect_down_Flag_Last[index] = Intersect_down_Flag[index]

        if Intersect_up_Flag_Last[index] == False and Intersect_up_Flag[index] == True:  # 判断第一根线是否是上升沿
            Car_num_up[index] += 1

            first_Flag = False  # 标志不是第一次了
            # 保存时间和坐标信息
            Times_up[index] = time.time()  # .........................待续
            # for car in cars:
                # if car.Intersect[index] == True:
                    # Cars[index] = car  #
            # self.SaveFlowData(index, 1) # 第一根线数据暂不保存
        Intersect_up_Flag_Last[index] = Intersect_up_Flag[index] 
        
def Realtime_car_amount(realtime_carCount): # 车道的实时在途数
        # 获取当前时间
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 新建一个字典
        realtime_car_amount = {}
        realtime_car_amount['实时在途数'] = realtime_carCount

        # 摄像头编号，收集信息时间
        realtime_car_amount['camera'] = 'video_Name'
        realtime_car_amount['time'] = dt_ms
        print(realtime_car_amount)

        # 将字典转为json文件
        json_str = json.dumps(realtime_car_amount, indent=4)

def Incident_Get_pic(cam, ids_car_stop, ids_person, ids_car_nixing, ids_car_left_initial, ids_car_stop_pre, ids_person_pre, ids_car_nixing_pre, ids_car_left_initial_pre, ids_bbox):
    print(ids_bbox)
    if len(ids_car_stop):# 判断是否车辆停车，停车10帧报警
        # if len(ids_car_stop_pre):
        for i in range(len(ids_car_stop)):
            if ids_car_stop[i] in ids_car_stop_pre:
                # stop_incident_count += 1
                # if stop_incident_count >= 10:
                print("car already stop")
                    # if stop_time_count == 500
            else:
                print("car stop")
                _,img1=cam.read()
                point1 = ids_bbox["%s"%ids_car_stop[i]]["center_coord"][2]
                point2 = ids_bbox["%s"%ids_car_stop[i]]["center_coord"][3]
                img1 = cv2.rectangle(img1, point1, point2, 255, 1)
                car_stop_time = time.time()
                cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/car_stop/%s.png"%car_stop_time, img1)
                        # stop_time_count = 0
                        # stop_time_count += 1
                # else:
                    # stop_incident_count = 0
    #判断是否逆行，50次连续逆行报警
    if len(ids_car_nixing):
        # reverse_drive_incident_count += 1
        # if len(ids_car_nixing_pre):
            # print("car nixing")
        for i in range(len(ids_car_nixing)):
            if ids_car_nixing[i] in ids_car_nixing_pre:
                print("car already nixing")
            else:
                print("car nixing")
                car_nixing_time = time.time()
                _,img3 = cam.read()
                point1 = ids_bbox["%s"%ids_car_nixing[i]]["center_coord"][2]
                point2 = ids_bbox["%s"%ids_car_nixing[i]]["center_coord"][3]
                img3 = cv2.rectangle(img3, point1, point2, 255, 1)
                cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/car_nixing/%s.png"%car_nixing_time, img3)

    # 判断是否有行人，有的话立刻报警
    if len(ids_person):
        # if len(ids_person_pre):
        for i in range(len(ids_person)):
            if ids_person[i] in ids_person_pre:
                print("person already exit")
            else:
                print("person detected")
                person_detect_time = time.time()
                _,img2=cam.read()
                point1 = ids_bbox["%s"%ids_person[i]]["center_coord"][2]
                point2 = ids_bbox["%s"%ids_person[i]]["center_coord"][3]
                img2 = cv2.rectangle(img2, point1, point2, 255, 1)
                cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/person/%s.png"%person_detect_time, img2)
    # 判断机动车是否驶离
    if len(ids_car_left_initial):
        for i in range(len(ids_car_left_initial)):
            if ids_car_left_initial[i] in range(ids_car_left_initial_pre):
                print("car already left")
            else:
                print("person detected")
                # person_detect_time = time.time()
                car_left_initial_road_time = time.time()
                _,img4=cam.read()
                point1 = ids_bbox["%s"%ids_car_left_initial[i]]["center_coord"][2]
                point2 = ids_bbox["%s"%ids_car_left_initial[i]]["center_coord"][3]
                img4 = cv2.rectangle(img4, point1, point2, 255, 1)
                cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/car_left/%s.png"%car_left_initial_road_time, img4) 
                
            # print("well done") 
    # return 

def draw_image(image, bboxes, confidence, classname, classid):
    # 闁告鍠庡ù?
    #    image = cv2.imread(input_image)

    color_index_dict = {
        0: (0, 0, 255),
        1: (0, 255, 0),
        2: (255, 0, 0),
        3: (255, 255, 0),
        4: (255, 0, 255),
        5: (0, 255, 255),
        6: (255, 128, 0),
        7: (128, 128, 255),
        8: (0, 255, 128),
        9: (128, 128, 0),
    }
    for index, bbox in enumerate(bboxes):
        #        color_key = index % 10
        color_key = classid[index]
        color = color_index_dict.get(color_key)
        # Coordinate must be integer.
        bbox = list(map(lambda cor: int(cor), bbox))
        # pdb.set_trace()
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 5)
        cfdence = confidence[index]
        typename = classname[index]
        font = cv2.FONT_HERSHEY_SIMPLEX
        #        imgzi = cv2.putText(image, '{} {:.3f}'.format(typename,cfdence), (420, 50), font, 0.5, (0, 255, 255), 1)
        imgzi = cv2.putText(image, '{} {:.3f}'.format(typename, cfdence), (bbox[0], bbox[1]), font, 0.5, (0, 255, 255),
                            1)

    #    cv2.imwrite(output_img, image)
    return image

def draw_img_fun(input_img, bboxes, confidence, classname, classid):
    # print(classname[0])

    boxed_img = draw_image(input_img, bboxes, confidence, classname, classid)
#    if classname[0]!= None:
 #       cv2.imwrite("output_img/person/{}".format(img_name), boxed_img)
        # with open("output_img/{}.txt".format(classname), "w") as f:
        #     f.write("{}, {}, {}, {}, {}".format(boxed_img, classid, classname, bboxes, confidence))
        #     f.write("\n")

    return boxed_img


# rtmpUrl = "rtmp://10.1.19.128:1935/live/2"

# ffmpeg -y -f rawvideo -vcodec rawvideo -pix_fmt bgr24 -s 1920*1080 -r 25 -i  1.txt -c:v libx264 pix_fmt yuv420p -preset ultrafast -f flv rtmpUrl
def binary2string(string):
    if isinstance(string, str):
        return string

    return string.decode()

def  rtmp_process(metadata_output):
    bbox = []
    confidence = []
    classid = []
    classname = []
    frame_yuv = None
    # frame = None
    frame_bgr = None
    for item in metadata_output:
        if item.errorCode != 0:
            continue
        item_key = binary2string(item.dataType)
        item_value = item.serializedMetadata
        data_parser = getattr(MxpiDataType, item_key)()
        data_parser.ParseFromString(item_value)
        # print(item_key)
        print("here")
        if item_key == 'MxpiObjectList':
            print("object")
            result = json_format.MessageToDict(data_parser, True)
            if result.get("objectVec") is not None:
                # #                    print("\n\n========================================")
                # print(result)
                for object in result["objectVec"]:
                    confidence.append(object["classVec"][0]["confidence"])
                    classid.append(object["classVec"][0]["classId"])
                    classname.append(object["classVec"][0]["className"])
                    if object.get("y0") is not None:
                        bbox.append([object["x0"], object["y0"], object["x1"], object["y1"]])

        #                    print(classname)
        #                    print(confidence)

        elif item_key == 'MxpiVisionList':
            print("vision")
            visionData = data_parser.visionVec[0].visionData
            dataPtr = visionData.dataPtr
            dataSize = visionData.dataSize  # h_Aligned * w_Aligned * 3/2
            dataStr = visionData.dataStr  # yuv data
            dataType = visionData.dataType
            frame = np.frombuffer(dataStr, dtype=np.uint8)

            visionInfo = data_parser.visionVec[0].visionInfo
            format = visionInfo.format
            height = visionInfo.height
            heightAligned = visionInfo.heightAligned
            keepAspectRatioScaling = visionInfo.keepAspectRatioScaling
            resizeType = visionInfo.resizeType
            width = visionInfo.width
            widthAligned = visionInfo.widthAligned

            # shape = (int(height * 1.5), width)
            shape = (int(height*1.5), width)

            frame_yuv = frame.reshape(shape)
            frame_bgr = cv2.cvtColor(frame_yuv, cv2.COLOR_YUV2RGB_NV21)
            #            vout_1.write(out_frame)
        elif item_key == 'MxpiTrackLet':
            print("tracking")
    


    out_frame = draw_img_fun(frame_bgr, bbox, confidence, classname, classid)
    # ut_frame_rszed = cv2.resize(out_frame, (960, 640), interpolation=cv2.INTER_LINEAR)
    if classname:
        # cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/person/{}.png".format("car"), out_frame)
        # out_frame = cv2.imread("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/person/car.png")
        return True, out_frame
    else:
        return False, None

def Main_program(data, Infer_msg, ids, ids_area1, ids_area2, center_together):# 主运行程序
    if data:
        if 'MxpiObject' in data:# 判断是否已经检测到目标
            object_num = int(len(data["MxpiObject"]))
            for i in range(object_num):
                center = [int((data["MxpiObject"][i]["x0"] + data["MxpiObject"][i]["x1"]) / 2), int((data["MxpiObject"][i]["y0"] + data["MxpiObject"][i]["y1"]) / 2), (int(data["MxpiObject"][i]["x0"]), int(data["MxpiObject"][i]["y0"])), (int(data["MxpiObject"][i]["x1"]), int(data["MxpiObject"][i]["y1"]))]
                # center_box = ((data["MxpiObject"][i]["x0"], data["MxpiObject"][i]["y0"]), (data["MxpiObject"][i]["x1"], data["MxpiObject"][i]["y1"]))
                cls = int(data["MxpiObject"][i]["classVec"][0]["classId"])
                id = int(data["MxpiObject"][i]["MxpiTrackLet"][0]["trackId"])
                # print(round(center[0],2), round(center[1], 2))
                # 对目标价进行区域划分
                if center[1]>= 180:
                    x, y, id, ids_area1, ids_area2, ids = Area_detect(round(center[0],2), round(center[1], 2),id, ids_area1, ids_area2, ids)
                    # center = [x, y, w, h]
                    name = "camera"
                    if center[0]:
                        Each_object = Store_det_msg(name, id, cls, center)
                        Infer_msg['%s'%id] = Each_object
                        # Area_detect(center[0], center[1], id)
                        if id in ids_area1:
                            center_box = (center[2], center[3], 1, cls, (center[0], center[1]))# ((x0, y0), (x1, y1), route_id, cls, (x, y))
                            center_together.append(center_box)
                        elif id in ids_area2:
                            center_box = (center[2], center[3], 2, cls, (center[0], center[1]))
                            center_together.append(center_box)
                                
            return center_together, Infer_msg, ids_area1, ids_area2, ids
        else:
            # 只跟踪，未检测到车
            print("Only tracking")
            return None, None, None, None, None

if __name__ == '__main__':
    # init stream manager
    streamManagerApi = StreamManagerApi()
    ret = streamManagerApi.InitManager()
    if ret != 0:
        print("Failed to init Stream manager, ret=%s" % str(ret))
        exit()

    # create streams by pipeline config file
    with open("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/pipeline/yolov5_test.pipeline", 'rb') as f:
        pipelineStr = f.read()
    ret = streamManagerApi.CreateMultipleStreams(pipelineStr)
    if ret != 0:
        print("Failed to create Stream, ret=%s" % str(ret))
        print("Rtsp url can't connect") #可能是rtsp视频流断掉 ，无法连接
        exit()

    streamName = b'classification'
    uniqueId = 0
    time1 = time.time()

    # 检测抛洒物事件，首先初始化
    rtsp_url = "rtsp://192.168.9.87:8554/mystream"
    cam = cv2.VideoCapture(rtsp_url)
    _,img1=cam.read()
    success,img2=cam.read()
    
    # 初始化矩阵，初始化直线，车辆数等参数
    # H, V = generateNumMatric(img1)
    # 初始化直线矩阵
    line_up = generateLineMatric(Line_k=0, Line_c=800)
    line_down = generateLineMatric(Line_k=0, Line_c=700)
    # 初始化参数信息
    Car_count = [0, 0]
    first_Flag = True
    frame_count = 0
    Intersect_up_Flag_Last = [False, False]
    Intersect_down_Flag_Last = [False, False]
    Car_num_up = [0, 0]
    Car_num_down = [0, 0]
    Times_up = [0.0, 0.0]
    Times_down = [0.0, 0.0]
    Speeds = [0, 0]
    
    # 代码开始运行时间
    initial_time = time.time()
    Time_plus = [0, 0]
    
    fo = open("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/test.h264", mode="wb")
    MaxframeCount = 100
    key1 = b'mxpi_videodecoder0'
    key2 = b'mxpi_modelinfer0'
    # key3 = b'mot_test'
    key_vec = StringVector()
    key_vec.push_back(key1)
    key_vec.push_back(key2)
    appsink = b'appsink0'

    # 主程序开始
    while 1:
        # 检测抛洒物
        # loss_incident_status = Loss_incident(success,cam, img1, img2)
        # if loss_incident_status == True:
            # print("Loss incident")
        # 得到推理结果
        inferResult_video = streamManagerApi.GetResult(streamName, appsink, key_vec, 3000)
        inferResult = streamManagerApi.GetResult(streamName, uniqueId, 3000)
        # inferResult1 = streamManagerApi.GetResult(streamName, uniqueId, 200000)
        '''if inferResult.errorCode != 0:
            print("error!!!\n\n\n")
            print("GetResultWithUniqueId error. errorCode=%d, errorMsg=%s" % (
                inferResult.errorCode, inferResult.data.decode()))
            exit()'''
        # print(ast.literal_eval(inferResult.data.decode()))
        # print(inferResult.metadataVec)
        '''bIsIDR = (len(inferResult1.data) > 1)
        if m_bFoundFirstIDR == False :
            if bIsIDR == False :
                continue
            else :
                m_bFoundFirstIDR = True
        if fo.write(inferResult1.data) == 0 :
            print("write frame to file fail")
            break
        
        print("Dealing frame id: %d" % frameCount)
        frameCount = frameCount + 1

        if frameCount > MaxframeCount :
            print("write frame to file done")
            break
        result =  MxpiDataType.MxpiVisionList()
        print(result)
        result.ParseFromString(inferResult[0].messageBuf)
        # fo = open("result.jpg", "wb")
        fo.write(result.visionVec[0].visionData.dataStr)'''

        if inferResult.errorCode != 0:
            print("error!!!\n\n\n")
            print("GetResultWithUniqueId error. errorCode=%d, errorMsg=%s" % (
                inferResult.errorCode, inferResult.metadata_list.decode()))
            exit()
        metadata_output = inferResult_video.metadataVec
        ret, out_frame = rtmp_process(metadata_output)
        Infer_msg_list = {}
        ids_list = []
        ids_area1_list = []
        ids_area2_list = []
        ids_car_stop = []
        ids_person = []
        ids_car_nixing = []
        ids_car_left_initial = []
        ids_car_nixing_pre = []
        ids_car_stop_pre = []
        ids_person_pre = []
        ids_car_left_initial_pre = []
        Infer_msg_ids = {}
        center_together_list = []
        # print(inferResult.data.decode())
        
        # 将推理结果转换成dict 
        data = ast.literal_eval(inferResult.metadata_list.decode())
        print(data)
        center_together, Infer_msg_ids, ids_area1, ids_area2, ids_list_result = Main_program(data, Infer_msg_list, ids_list, ids_area1_list, ids_area2_list, center_together_list)
        # print(Infer_msg_ids)
        
        if center_together:
            Car_count, Intersect_up_Flag, Intersect_down_Flag, index_car, car_bbox_center_up, car_bbox_center_down = DetecFromOneFrame(line_up, line_down, center_together)

            # 开始检测交通参数，车流量，平均速度，占有率
            Traffic_parameter(Intersect_up_Flag, Intersect_down_Flag, index_car, car_bbox_center_up, car_bbox_center_down, first_Flag, Time_plus)
            car_stop, car_nixing, car_normal, car_leave, person_situation, car_left_initial_road, IDS_list_car_stop, IDS_list_person, IDS_list_car_nixing, IDS_list_left_initial = Detect_object_situation(ids_area1, ids_area2, ids_list_result, Infer_msg_ids, IDS_info, IDS_list_area_1, IDS_list_area_2, IDS_list)
        
            IDS_list = ids_area1
            IDS_list_area_1 = ids_area1
            IDS_list_area_2 = ids_area2
            IDS_info = Infer_msg_ids
            
            Incident_Get_pic(cam, IDS_list_car_stop, IDS_list_person, IDS_list_car_nixing, IDS_list_left_initial, ids_car_stop_pre, ids_person_pre, ids_car_nixing_pre, ids_car_left_initial_pre, Infer_msg_ids)
            # 判断是否车辆停车,停车10帧报警
            ids_car_nixing_pre = IDS_list_car_nixing 
            ids_car_stop_pre = IDS_list_car_stop
            ids_car_person_pre = IDS_list_person
            ids_car_left_initial_pre = IDS_list_left_initial
            
        else:
            print("Nothing")
            break