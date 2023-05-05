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
import json
import math
import os
import sys
import time
import acl

import multiprocessing
from multiprocessing import Process
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
from datetime import datetime
from set_log import log
import requests
import threading
import redis
import socket
from PIL import Image, ImageDraw, ImageFont
# import socket_server

# client = socket.socket()
# client.connect(('localhost', 6969))# 定义socket服务器
# redisPool = redis.ConnectionPool(host='localhost', port=6379, db=0)
# redis_use = redis.Redis(connection_pool=redisPool)
# key_value = "huaweitest"
url_signal = 'http://localhost:8000/api/signal/'
# stop_incident_count = 0
reverse_drive_incident_set_count = 25 # 逆行25帧报警
stop_incident_set_count = 10 #10帧停车报警 
person_incident_set_count = 10 # 10帧报警行人
# car_nixing_incident_set_count = 25 # 逆行25帧报警

# OpenCV内核版本
erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

IDS_list_car = [0]
IDS_list_person = [0]
IDS_list_shili_area_1 = [0]
IDS_list_shili_area_2 = [0]
name_test = []
IDS_msg_about_person = {}
#IDS_msg_about_car_stop = {}
for i in range(10):
    m = f'IDS_msg_about_car_stop{i+1}'
    exec(m + '= %s' %({}))
    
for i in range(10):
    m = f'IDS_msg_about_car_nixing{i+1}'
    exec(m + '= %s' %({}))

Ids_pre_area1 = [0]
Ids_pre_area2 = [0]
Ids_pre_area3 = [0]
Ids_pre_area4 = [0]
Ids_pre_area5 = [0]
Ids_pre_area6 = [0]
Ids_pre_area7 = [0]
Ids_pre_area8 = [0]
Ids_pre_area9 = [0]
Ids_pre_area10 = [0]

# IDS_msg_about_car_nixing = {}

IDS_car_nixing_pre = [False, False,False, False, False, False,False, False, False, False]
IDS_car_stop_pre = [False, False,False, False, False, False,False, False, False, False]
IDS_person_pre = []
IDS_car_left_initial_pre = []
# global IDS_list

IDS_info_pre = {0}
# car_stop_time = 0
# car_nixing_time = 0
# person_detect = 0

def car_stop_area(name, i):
    if eval(f'IDS_msg_about_car_stop{i}'):
        if name in eval(f'IDS_msg_about_car_stop{i}'):
            eval(f'IDS_msg_about_car_stop{i}')[name] += 1
        else:
            eval(f'IDS_msg_about_car_stop{i}')[name] = 0
    else:
        eval(f'IDS_msg_about_car_stop{i}')[name] = 0

def car_nixing_pre(name, i):
    if eval(f'IDS_msg_about_car_nixing{i}'):
        if name in eval(f'IDS_msg_about_car_nixing{i}'):
            eval(f'IDS_msg_about_car_nixing{i}')[name] += 1
        else:
            eval(f'IDS_msg_about_car_nixing{i}')[name] = 0
    else:
        eval(f'IDS_msg_about_car_nixing{i}')[name] = 0

def Detect_object_situation(ids_area_shili_1, ids_area_shili_2, ids, data, IDS_info, IDS_list_area_1, IDS_list_area_2, IDS_list, IDS_list_person_pre, IDS_people, Ids_set_pre_area1, Ids_set_pre_area2, Ids_set_pre_area3,Ids_set_pre_area4,Ids_set_pre_area5,Ids_set_pre_area6,Ids_set_pre_area7,Ids_set_pre_area8,Ids_set_pre_area9,Ids_set_pre_area10):# 车辆的交通事件分类
    car_stop, car_nixing, car_normal, car_leave, person_situation, car_leave_initial_road = False, False, False, False, False, False
    IDS_list_car_stop = []
    IDS_list_person = []
    IDS_list_car_nixing = []
    IDS_list_left_initial = []
    for j in range(len(ids_list_car_result)):
        if ids[j] in Ids_set_pre_area1:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                #IDS_car_stop_pre[i] = car_stop
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 1)

            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                # IDS_car_nixing_pre[i] = car_nixing
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 1)
        elif ids[j] in Ids_set_pre_area2:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 2)
            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 2)
        elif ids[j] in Ids_set_pre_area3:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 3)
            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 3)
        elif ids[j] in Ids_set_pre_area4:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 4)
            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 4)
        elif ids[j] in Ids_set_pre_area5:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 5)
            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 5)
        elif ids[j] in Ids_set_pre_area6:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 6)
            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 6)
        elif ids[j] in Ids_set_pre_area7:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 7)
            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 7)
        elif ids[j] in Ids_set_pre_area8:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 8)
            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 8)
        elif ids[j] in Ids_set_pre_area9:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 9)
            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 9)
        elif ids[j] in Ids_set_pre_area10:# 此次检测到的🚗车辆是否在上一次检测到的名单中，是的话程序继续
            name = '%s'%ids[j]# 车辆ID
            if data["%s"%ids[j]]["center_coord"][1]-1 <= IDS_info["%s"%ids[j]]["center_coord"][1] <= data["%s"%ids[j]]["center_coord"][1]+1:# 是否停车
                car_stop = True# 车辆停止状态为真
                IDS_list_car_stop.append(ids[j])# 将ID添加到所有停车ID中
                car_stop_area(name, 10)
            elif IDS_info["%s"%ids[j]]["center_coord"][1] < data["%s"%ids[j]]["center_coord"][1]:# 是否逆行
                car_nixing = True
                IDS_list_car_nixing.append(ids[j])# 将ID添加到所有逆行ID中
                car_nixing_pre(name, 10)



    for i in range(len(IDS_people)):
        if IDS_people[i] in IDS_list_person_pre:
            name = '%s'%IDS_people[i]
            person_situation = True
            IDS_list_person.append(IDS_people[i])
            if IDS_msg_about_person:
                if name in IDS_msg_about_person:
                    IDS_msg_about_person[name] += 1
                else:
                    IDS_msg_about_person[name] = 0
            else:
                IDS_msg_about_person[name] = 0


# 判断车辆时候驶离原来的车道
    num1 = len(ids_area_shili_1)
    num2 = len(ids_area_shili_2)
    if num1:
        for i in range(num1):
            if ids_area_shili_1[i] in IDS_list_area_2:
                car_leave_initial_road = True
                print("%s"%ids_area_shili_1[i] + " is drive out of the border incident")
                IDS_list_left_initial.append(ids_area_shili_1[i])

    if num2:
        for i in range(num2):
            if ids_area_shili_2[i] in IDS_list_area_1:
                car_leave_initial_road = True
                print("%s"%ids_area_shili_2[i] + " is drive out of the border incident")
                IDS_list_left_initial.append(ids_area_shili_2[i])
                
    # situ = [car_stop, car_nixing, person_situation, car_leave_initial_road]
    # all_id = (IDS_list_car_stop, IDS_list_car_nixing, IDS_list_person, IDS_list_left_initial)

    # log.info(situ)
    # log.warning(all_id)
    # print(IDS_list_car_stop)
    return car_stop, car_nixing, car_normal, car_leave, person_situation, car_leave_initial_road, IDS_list_car_stop, IDS_list_person, IDS_list_car_nixing, IDS_list_left_initial

def Store_det_msg(name, id, cls, center):# 存储检测信息
    det_msg = {}
    dt_ms = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')
    det_msg['camera_name'] = name
    det_msg['ID_num'] = int(id)
    det_msg['class'] = int(cls)
    det_msg['center_coord'] = center
    det_msg['time'] = dt_ms
    # print(det_msg)
    return det_msg
    
def Mask_image(center):# 每个车生成矩阵
    # 生成二维0矩阵
    masks = np.zeros((1080, 1920), np.uint8)
    # for center in center_together:
    '''for i in range(1920):
            for j in range(1080):
                if center[0][0]  < i < center[1][0] & center[1][1] < j < center[0][1]:
                    masks[i][j] = 0'''
    # 
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

def Loss_incident(metadata, ids):# 抛洒物事件
    # while True:
        # init_pic_background = "" 
        # cap = cv2.VideoCapture("rtsp://192.168.9.87:8554/mystream")
        img1 = cv2.imread("/home/HwHiAiUser/mxVision-2.0.4.6/samples/mxVision/python/vlc.jpg")
        # success, img = cap.read()
        loss_incident_situ = False
        ret, img = create_pic(metadata)
        img2 = img
        BLUR_RADIUS = 21
        # print(ids)
        mask = np.zeros((1080, 1920), dtype=np.uint8)
        pts = np.array([[0, 1080], [0, 965], [1420,300], [1755, 300], [1755, 1080], [1920, 1080]])
        
        pts1 = np.array([[360, 1080], [1316, 178], [1367, 178], [1829, 1080]])
        
        gray_frame1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray_frame1 = cv2.GaussianBlur(gray_frame1, (BLUR_RADIUS, BLUR_RADIUS), 0)
        gray_frame2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        gray_frame2 = cv2.GaussianBlur(gray_frame2, (BLUR_RADIUS, BLUR_RADIUS), 0)
        if ids:
            for i in range(len(ids)):
                point1 = (int((ids[i][0][0])*(0.95)), int((ids[i][0][1])*(0.95)))
                point2 = (int((ids[i][1][0])*(1.05)), int((ids[i][1][1])*(1.05)))
                
                cv2.rectangle(gray_frame1,point1,point2,0,-1)
                cv2.rectangle(gray_frame2,point1,point2,0,-1)
            if ret:
                diff=cv2.absdiff(gray_frame1,gray_frame2)    # 获得两帧之间的差异
                # cv2.imshow('diff',diff)    # 图像处理：灰度，高斯模糊，二值化
                # gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(diff, 80, 255, cv2.THRESH_BINARY)  # 阈值化操作得到黑白图像
                # 形态学运算进行平滑处理，便于后续边框的绘制
                cv2.erode(thresh, erode_kernel, thresh, iterations=2)
                cv2.dilate(thresh, dilate_kernel, thresh, iterations=2)
                # 用0填充多边形
                cv2.fillPoly(mask, [pts1], (255), 8, 0)
                # 位与运算
                result = cv2.bitwise_and(thresh, thresh, mask=mask)
                # cv2.imshow('dilated',dilated)    # 获取轮廓
                contours,_ =cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    # 判断矩形是否满足条件
                if contours:
                    for contour in contours:
                        x,y,w,h=cv2.boundingRect(contour)
                        if 50 < cv2.contourArea(contour) < 10000:
                            cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
                            # cv2.imshow('image',img1)    # 读下一帧
                            loss_incident_situ = True
                    dt_ms = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f') # 获取当前时间
                    path = "/usr/digital_twin/digital_twin_django/media/images/pic/car/%s.png"%dt_ms
                    cv2.imwrite(path, img)
                    loss_path = "pic/car/%s.png"%dt_ms
                    # post抛洒物事件,类型为4
                    event_type = 4
                    # post到前段页面
                    post_event(event_type, loss_path) 
                    # exit(0)
                    # continue
        # time.sleep(10)
        return loss_incident_situ

def Area_detect(x, y, id, cls):# 车道区域划分
    ids_area1 = []
    ids_area2 = []
    ids_car_list = []
    ids_person = []
    y1 = 1.9636*x - 2513.4
    y2 = -3*x + 4215
    y3 = -0.939*x + 1417.89

    if y >= y3:
        if y >= y1: # 检测是否在待识别区 
            if cls == 0:
                ids_person.append(id)
            else:
                ids_car_list.append(id)# 所有符合的id集合
            if y >= y2: # 检测具体区域
                ids_area2.append(id)# 区域 2
            else:
                ids_area1.append(id)# 区域 1
        return ids_area1, ids_area2, ids_car_list, ids_person
    else:
        return ids_area1, ids_area2, ids_car_list, ids_person

def DetecFromOneFrame(line_up, line_down, center_together):# 得到车辆与划定区域之间是否相交信息
    # 每个车道通过的车辆数
    # carCount = [0, 0, 0, 0]
    # routeNum = [0,1]
    # 车辆类别，后续可以分类
    index_car = [None, None, None, None]
    # bbox_xcycwh, cls_conf, cls_ids, prediction = predict.detect(frame)  # 获取预测结果
    if center_together:
        # masks = np.zeros((1920, 1080), np.uint8)
        # carCount = [0, 0]  # 车道实时的车数
        # 中心点坐标
        car_bbox_center_down = [None, None, None, None]
        car_bbox_center_up = [None, None, None, None]
        # print(center_together)
        for center in center_together:
            masks= Mask_image(center)
            # routeNum = center[2]
            # print(masks)
            Intersect_up_Flag = [False, False, False, False]  # 与第一根线是否相交标识符
            Intersect_down_Flag = [False, False, False, False]  # 与第二根线是否相交标识符

            routeNum = int(center[2]) - 1
            if routeNum is not None:
                Car_count[routeNum] += 1  # 车道车辆总数加1
                if checkIntersect(masks, line_up):
                    Intersect_up_Flag[routeNum] = True
                    car_bbox_center_up[routeNum] = center[4]
                    # car.Intersect[routeNum] = True
                if checkIntersect(masks, line_down):
                    Intersect_down_Flag[routeNum] = True
                    car_bbox_center_down[routeNum] = center[4]

        return Intersect_up_Flag, Intersect_down_Flag, index_car, car_bbox_center_up, car_bbox_center_down
    else:
        return None, None, None, None, None

def DataCollect(routeNum, Speeds, carCount, car_type): # 每辆车的属性信息，包括车道，车辆类型，车速，实时在途车数，时间等信息
        # 准备发送车道上车辆的速度，数量信息到Kafka
        dt_ms = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f') # 获取当前时间
        camera_data = {} 
        if routeNum==0:        # 0车道信息
            # 左侧车道编码为0
            camera_data['road'] = 0
            camera_data['car_class'] = car_type
            # camera_data['car_color'] = class_car
            # 左侧车道车速
            camera_data['car_speed'] = Speeds[0]
            # 车道总过车车数
            camera_data['car_count'] = carCount
            #车道实时车数
            camera_data['car_realtime_count'] = len(Ids_area1)

        elif routeNum==1:       # 1车道信息
            camera_data['road'] = 1
            camera_data['car_class'] = car_type
            # camera_data['car_color'] = class_car

            camera_data['car_speed'] = Speeds[1]
            # 车道总过车车数
            camera_data['car_count'] = carCount
            #车道实时车数
            camera_data['car_realtime_count'] = len(Ids_area2)
            
        elif routeNum==2:       # 2车道信息
            camera_data['road'] = 2
            camera_data['car_class'] = car_type
            # camera_data['car_color'] = class_car

            camera_data['car_speed'] = Speeds[2]
            # 车道总过车车数
            camera_data['car_count'] = carCount
            #车道实时车数
            camera_data['car_realtime_count'] = len(Ids_area3)
        elif routeNum==3:       # 3车道信息
            camera_data['road'] = 3
            camera_data['car_class'] = car_type
            # camera_data['car_color'] = class_car

            camera_data['car_speed'] = Speeds[3]
            # 车道总过车车数
            camera_data['car_count'] = carCount
            #车道实时车数
            camera_data['car_realtime_count'] = len(Ids_area4)
        # 摄像头编号，收集信息时间
        camera_data['camera'] = 'video_Name'
        camera_data['time'] = dt_ms
        # print(camera_data)
        log.error(camera_data)


def CalCarSpeed(car1, car2, time1, time2):# 计算平均车速
        # points_or = np.float32([[[car1[0], car1[1]], [[car2[0], car2[1]]]]
        # points_perspective = cv2.perspectiveTransform(points_or, np.float32(self.cfg['Matrix_Trans']))
        # distance = math.sqrt(
            # math.pow(points_perspective[0][0][0] - points_perspective[1][0][0], 2) +
            # math.pow(points_perspective[0][0][1] - points_perspective[1][0][1], 2))
        # time = time2 - time1
        # print(type((time)))
        distance = 7
        time_diff = time1 - time2
        print("shijiancha     " + "%s"%time_diff)
        speed = distance / time_diff
        print("sudushi    "+ "%s"%speed)
        # speed = (distance * cfg['Para_Distance'] / 100) //(
                    # time) * 3.6  # 变换后，1像素代表1cm;self.cfg.Para_Distance用于调整距离比例
        return round(int(speed)), time_diff

def Traffic_parameter(Intersect_up_Flag, Intersect_down_Flag, index_car, car_bbox_center_up, car_bbox_center_down):# 计算车辆的交通参数
    for index in [0, 1, 2, 3]:
        global first_Flag
        if Intersect_up_Flag_Last[index] == False and Intersect_up_Flag[index] == True and first_Flag == False:  # 判断上面线是否是上升沿
            # 第二根线过车数量+1
            Car_num_up[index] += 1
            # 根据第一根线数据计算车速等数据
            # 保存时间和坐标信息
            Times_up[index] = time.time()  # .........................待续
            
            # 计算平均车速，车流量，占有率
            if Speeds[index]:
                speed_all += speed_all
                car_amount_all += 1
                Time_plus += Time_plus

            print("i'm here")            

            Speeds[index], Time_plus = CalCarSpeed(car_bbox_center_up[index], car_bbox_center_down[index], Times_up[index],
                                            Times_down[index])  # 计算车速，并返回结果
            DataCollect(index, Speeds, Car_num_down, car_type)
        Intersect_up_Flag_Last[index] = Intersect_up_Flag[index]

        if Intersect_down_Flag_Last[index] == False and Intersect_down_Flag[index] == True:  # 判断下面线是否是上升沿
            # 第一根过车数量+1
            Car_num_down[index] += 1
            first_Flag = False  # 标志不是第一次了
            # 保存时间和坐标信息
            Times_down[index] = time.time()  # .........................待续
            # 车辆类型
            # car_type = index_car[index]
            car_type = 1

        Intersect_down_Flag_Last[index] = Intersect_down_Flag[index] 
        
def Realtime_car_amount(realtime_carCount): # 车道的实时在途数
        # 获取当前时间
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        # 新建一个字典
        realtime_car_amount = {}
        realtime_car_amount['实时在途数'] = realtime_carCount

        # 摄像头编号，收集信息时间
        realtime_car_amount['camera'] = 'video_Name'
        realtime_car_amount['time'] = dt_ms
        print(realtime_car_amount)

        # 将字典转为json文件
        json_str = json.dumps(realtime_car_amount, indent=4)

def Get_event_pic(path, frame, center, name):
    center = (center[0], center[1])
    # name = "haha"
    # cv2.putText(frame, str(name), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)

    frame = cv2ImgAddText(frame, name, center[0], center[1], textColor=(255,0,0), textsize=50)
    # frame = cv2.putText(frame)
    cv2.imwrite(path, frame)

def Get_event_video(path, name):
    frame_count = 0
    center = (100, 200) 
    width = 1920# int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频的宽度
    height = 1080# int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频的高度
    fps = 25# cap.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
    # fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # 视频的编码
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter("%s.mp4"%path, fourcc, fps, (width, height))
    # frame = cv2.putText(frame) 
    # cv2.imwrite(path, frame)
    # path_video = path
    while frame_count <= 125:
        inferResult1 = streamManagerApi.GetResult(streamName, appsink, key_vec, 3000)# get图像信息
        # res=requests.get(url) #返回一个消息实体
        metadata_output_wode = inferResult1.metadataVec
        ret, frame = rtmp_process(metadata_output_wode)
        cv2.putText(frame, str(name), center, cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 3)
        # print(width, height, fps, fourcc)
        # 定义视频对象输出
        
        writer.write(frame)  # 视频保存
        frame_count += 1
    writer.release()
        

def post_event(event, image_path):
    url = 'http://localhost:8000/api/event/'
    
    a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    realtime_car_amount = {}
    realtime_car_amount['create_time'] = a
    realtime_car_amount['ip'] = '192.168.9.87'
    realtime_car_amount['location'] = 'test_came'
    realtime_car_amount['event_type'] = event
    realtime_car_amount['image'] = image_path

    r = requests.post(url, json = realtime_car_amount)
    print(r.json())

def post_param(param_unit, param_value, param_type):
    
    a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    url_param = 'http://localhost:8000/api/param/' 
    
    param_car = {}
    param_car['create_time'] = a
    param_car['ip'] = '192.168.9.87'
    param_car['time_unit'] = '5mins'
    param_car['unit'] = param_unit
    param_car['location'] = 'test_param_location'
    param_car['value'] = param_value
    param_car['param_type'] = param_type
    
    param_send = requests.post(url_param, json = param_car)

    print(param_send.json())

def Incident_Get_pic(ids_car_stop, ids_person, ids_car_nixing, ids_car_left_initial, ids_car_left_initial_pre, metadata, info):
    # print(ids_bbox)
    # ret, out_frame = rtmp_process(metadata)
    if len(ids_car_stop):# 判断是否车辆停车，停车10帧报警
        # if len(ids_car_stop_pre):
        for i in range(len(ids_car_stop)):
            name = '%s'%ids_car_stop[i]
            for m in range(10):
                if name in eval(f'IDS_msg_about_car_stop{m+1}'):
                    if eval(f'IDS_msg_about_car_stop{m+1}')[name] == 20:
                        # car_stop_time = time.time()
                        car_stop_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f') # 获取当前时间
                        ret, out_frame = rtmp_process(metadata)
                        # path_video = "/usr/digital_twin/digital_twin_django/media/images/pic/car_stop/%s"%car_stop_time
                        path = "/usr/digital_twin/digital_twin_django/media/images/pic/car_stop/%s.png"%car_stop_time
                        # cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/car_stop/%s.png"%car_stop_time, out_frame)
                        center = info[name]["center_coord"]
                        # print(center)
                        message = "警告：车辆停车！！！"
                        # frame_count = 0
                        if ret:
                            proc = multiprocessing.Process(target=Get_event_pic(path, out_frame, center, message), args=('car_stop'))
                            # proc_video = multiprocessing.Process(target=Get_event_video(path_video, name))
                            proc.start()
                        else:
                            print("wrong")
                        # proc_video.start()
                        eval(f'IDS_msg_about_car_stop{m+1}')[name] += 1
                        path_test = "pic/car_stop/%s.png"%car_stop_time
                        
                        # 事件类型，类型为1
                        event_type = 1
                        # post到前段页面
                        post_event(event_type, path_test)

    #判断是否逆行，50次累计逆行报警
    if len(ids_car_nixing):
        for i in range(len(ids_car_nixing)):
            name1 = '%s'%ids_car_nixing[i]
            for n in range(10):
                if name1 in eval(f'IDS_msg_about_car_nixing{n+1}'):
                    if eval(f'IDS_msg_about_car_nixing{n+1}')[name1] == 20:
                        eval(f'IDS_msg_about_car_nixing{n+1}')[name1] += 1
                        car_nixing_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f') # 获取当前时间
                        ret, out_frame1 = rtmp_process(metadata)
                        nixing_path = "/usr/digital_twin/digital_twin_django/media/images/pic/car_nixing/%s.png"%car_nixing_time 
                        # cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/car_nixing/%s.png"%car_nixing_time, out_frame)
                        center = info[name1]["center_coord"] 
                        message = "警告：车辆逆行！！！"
                        proc1 = multiprocessing.Process(target=Get_event_pic(nixing_path, out_frame1, center, message), args=("nixing"))
                        proc1.start()
                        # print("")
                        nixing_path_test = "pic/car_nixing/%s.png"%car_nixing_time 

                        # 事件类型，类型为2
                        event_type = 2
                        # post到前段页面
                        post_event(event_type, nixing_path_test)

    # 判断是否有行人，有的话立刻报警
    if len(ids_person):
        # if len(ids_person_pre):
        # print(ids_person)
        for i in range(len(ids_person)):
            name2 = '%s'%ids_person[i]
            if name2 in IDS_msg_about_person:
                if IDS_msg_about_person[name2] == 3:
                    IDS_msg_about_person[name2] += 1
                    person_detect_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f') # 获取当前时间
                    ret, out_frame2 = rtmp_process(metadata)
                    person_path = "/usr/digital_twin/digital_twin_django/media/images/pic/person/%s.png"%person_detect_time 
                    # cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/person/%s.png"%person_detect_time, out_frame) 
                    center = info[name2]["center_coord"]
                    # print(center)
                    message = "警告：有行人！！！"
                    proc2 = multiprocessing.Process(target=Get_event_pic(person_path, out_frame2, center, message), args=("person"))
                    proc2.start()
                    # print("person")
                    person_path_test = "pic/person/%s.png"%person_detect_time  
                    # 事件类型，类型为3
                    event_type = 3
                    # post到前段页面
                    post_event(event_type, person_path_test)



    # 判断机动车是否驶离
    if len(ids_car_left_initial):
        for i in range(len(ids_car_left_initial)):
            name3 = '%s'%ids_car_left_initial[i]
            if info[name3]["class"] == 1:

                # print("person detected")
                # ids_car_left_initial_pre.append(ids_car_left_initial[i])
                # person_detect_time = time.time()
                car_left_initial_road_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')
                ret, out_frame3 = rtmp_process(metadata)
                car_left_initial_path = "/usr/digital_twin/digital_twin_django/media/images/pic/car_wrong_road/%s.png"%car_left_initial_road_time
                # cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/person/%s.png"%person_detect_time, out_frame) 
                center = info[name3]["center_coord"]
                # print(center)
                message = "警告：车辆驶离原车道！！！"
                proc3 = multiprocessing.Process(target=Get_event_pic(car_left_initial_path, out_frame3, center, message), args=("car left"))
                proc3.start()
                car_left_initial_path_test = "pic/car_wrong_road/%s.png"%car_left_initial_road_time
                # 事件类型，类型为5
                event_type = 5
                # post到前段页面
                post_event(event_type, car_left_initial_path_test)
            else:
                print(info[name3]["class"])
    # print("well done") 
    # return ids_car_stop_pre, ids_car_nixing_pre, ids_person_pre, ids_car_left_initial_pre

def draw_image(image, bboxes, confidence, classname, classid):
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

def rtmp_process(metadata_output):
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
        # print("here")
        if item_key == 'MxpiObjectList':
            # print("object")
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
            # print("vision")
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
            # shape = (1080, 1920)

            frame_yuv = frame.reshape(shape)
            frame_bgr = cv2.cvtColor(frame_yuv, cv2.COLOR_YUV2RGB_NV21)
            #            vout_1.write(out_frame)
        elif item_key == 'MxpiTrackLet':
            print("tracking")
    

    out_frame = draw_img_fun(frame_bgr, bbox, confidence, classname, classid)
    # ut_frame_rszed = cv2.resize(out_frame, (960, 640), interpolation=cv2.INTER_LINEAR)
    if classname:
        # cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/cache/{}.png".format("car"), out_frame)
        # out_frame = cv2.imread("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/cache/car.png")
        return True, out_frame
    else:
        return False, None

def create_pic(metadata_output):
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
        # print("here")
        if item_key == 'MxpiObjectList':
            # print("object")
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
            # print("vision")
            visionData = data_parser.visionVec[0].visionData
            # dataPtr = visionData.dataPtr
            # dataSize = visionData.dataSize  # h_Aligned * w_Aligned * 3/2
            dataStr = visionData.dataStr  # yuv data
            # dataType = visionData.dataType
            frame = np.frombuffer(dataStr, dtype=np.uint8)

            visionInfo = data_parser.visionVec[0].visionInfo
            # format = visionInfo.format
            height = visionInfo.height
            # heightAligned = visionInfo.heightAligned
            # keepAspectRatioScaling = visionInfo.keepAspectRatioScaling
            # resizeType = visionInfo.resizeType
            width = visionInfo.width
            # widthAligned = visionInfo.widthAligned

            # shape = (int(height * 1.5), width)
            shape = (int(height*1.5), width)
            # shape = (1080, 1920)

            frame_yuv = frame.reshape(shape)
            frame_bgr = cv2.cvtColor(frame_yuv, cv2.COLOR_YUV2RGB_NV21)
            #            vout_1.write(out_frame)
        elif item_key == 'MxpiTrackLet':
            print("tracking")
    


    # out_frame = draw_img_fun(frame_bgr, bbox, confidence, classname, classid)
    # ut_frame_rszed = cv2.resize(out_frame, (960, 640), interpolation=cv2.INTER_LINEAR)
    out_frame = frame_bgr
    if classname:
        # cv2.imwrite("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/cache/{}.png".format("car"), out_frame)
        # out_frame = cv2.imread("/home/HwHiAiUser/mxVision-2.0.3/mxVision-2.0.2/samples/mxVision/python/pic/cache/car.png")
        return True, out_frame
    else:
        return False, None 

def zhu_program(data):# 主运行程序
    Infer_msg = {}
    ids_car = []
    IDS_person = []
    center_together = []
    center_together_all = []
    ids_area1 = []
    ids_area2 = []
    ids_area3 = []
    ids_area4 = []

    ids_shili_area1 = []
    ids_shili_area2 = []
    
    if data:
        if 'MxpiObject' in data:# 判断是否已经检测到目标
            object_num = int(len(data["MxpiObject"]))# 目标数
            for i in range(object_num):
                # 获得目标框的中心点坐标，以及（x0， y0），（x1， y1）坐标
                center = [round((data["MxpiObject"][i]["x0"] + data["MxpiObject"][i]["x1"]) / 2), round((data["MxpiObject"][i]["y0"] + data["MxpiObject"][i]["y1"]) / 2), (round(data["MxpiObject"][i]["x0"]), round(data["MxpiObject"][i]["y0"])), (round(data["MxpiObject"][i]["x1"]), round(data["MxpiObject"][i]["y1"]))]
                # center = [((x0+x1)/2), (y0+y1)/2), (x0, y0), (x1, y1)]
                # center_box = ((data["MxpiObject"][i]["x0"], data["MxpiObject"][i]["y0"]), (data["MxpiObject"][i]["x1"], data["MxpiObject"][i]["y1"]))
                # 获得目标的种类id
                cls = int(data["MxpiObject"][i]["classVec"][0]["classId"])
                # 获得目标的追踪id
                id = int(data["MxpiObject"][i]["MxpiTrackLet"][0]["trackId"])
                # print(round(center[0],2), round(center[1], 2))
                # 对目标进行区域划分
                # 目标的 x0,y0, x1,y1坐标
                each_object_center = (center[2], center[3])
                # 对每个目标的x0, y0, x1,y1坐标存储
                center_together_all.append(each_object_center)
                # 开始对目标分区域
                if center[1]>= 440:# 比较x，y的底线，先划区域
                    '''if cls == 0:# 发现person
                        name = "camera"
                        IDS_person.append(id)
                        Each_object = Store_det_msg(name, id, cls, center)
                        Infer_msg['%s'%id] = Each_object'''
                    # ids_area1, ids_area2, ids_car, IDS_person = Area_detect(round(center[0], 2), round(center[1], 2),id, cls)
                    x = round(center[0], 2)# 取坐标小数点后2位
                    y = round(center[1], 2)
                    # 划定区域边界线
                    y1 = -1.6*x +1496   # zuo边边界线
                    y2 = -3.879*x + 3252.12         # 中间边界线
                    y3 = 9.846*x - 7289.23  # 左边边界线
                    y4 = 2.032*x - 1317.46
                    y5 = 1.103*x - 608.28

                    if y1 <=y <= y5:
                        if y <= y2: # 检测是否在待识别区
                            ids_area1.append(id)
                        # ids_car.append(id)# 所有符合的汽车id集合
                        # 画区域，分10个区域
                        elif y <= y3:# 区域 1,3,5,7,9
                            ids_area2.append(id)
                        elif y <= y4:
                            ids_area3.append(id)
                        elif y <= y5:
                            ids_area4.append(id)
                                
                    # center = [x, y, w, h]
                    name = "camera"
                    if center[0]:
                        # 存储每个目标的名字，追踪id，类别，中心点坐标以及（x0, y0）(x1, y1)
                        Each_object = Store_det_msg(name, id, cls, center)
                        # 所有目标信息存储到一个字典里
                        Infer_msg['%s'%id] = Each_object
                        # Area_detect(center[0], center[1], id)
                        # 目标框（x0,y0）(x1,y1)以及车道的划分，目标类别，中心点坐标

                        if id in ids_area1:
                            center_box = (center[2], center[3], 1, cls, (center[0], center[1]))# ((x0, y0), (x1, y1), route_id, cls, (x, y))
                            center_together.append(center_box)
                        elif id in ids_area2:
                            center_box = (center[2], center[3], 2, cls, (center[0], center[1]))
                            center_together.append(center_box)
                        elif id in ids_area3:
                            center_box = (center[2], center[3], 3, cls, (center[0], center[1]))
                            center_together.append(center_box)
                        elif id in ids_area4:
                            center_box = (center[2], center[3], 4, cls, (center[0], center[1]))
                            center_together.append(center_box)  
                            
            # 返回车辆的信息，包括（目标框2个坐标，车道，类别，以及中心坐标），返回每个坐标的(x0,y0),(x1,y1),返回所有目标信息的字典，返回区域1，2的car——id，返回car的所有id，返回所有人的id信息
            return center_together, center_together_all, Infer_msg, ids_shili_area1, ids_shili_area2, ids_car, IDS_person, ids_area1, ids_area2,ids_area3, ids_area4
        else:
            return center_together, center_together_all, Infer_msg, [], [], [], [], [], [],[], []
    else:
        # 只跟踪，未检测到车
        return center_together, center_together_all, Infer_msg, [], [], [], [], [], [],[], []

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textsize = 20):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        fontStyle = ImageFont.truetype("/home/HwHiAiUser/mxVision-2.0.4.6/samples/mxVision/python/font/simsun.ttc", textsize, encoding="utf-8")
        draw.text((left, top), text, textColor, font=fontStyle)
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    
if __name__ == '__main__':
    # init stream manager
    streamManagerApi = StreamManagerApi()
    ret = streamManagerApi.InitManager()
    if ret != 0:
        print("Failed to init Stream manager, ret=%s" % str(ret))
        exit()

    # create streams by pipeline config file
    with open("/home/HwHiAiUser/mxVision-2.0.4.6/samples/mxVision/pipeline/yolov5_classification.pipeline", 'rb') as f:
        pipelineStr = f.read()
    ret = streamManagerApi.CreateMultipleStreams(pipelineStr)
    if ret != 0:
        print("Failed to create Stream, ret=%s" % str(ret))
        print("Rtsp url can't connect") #可能是rtsp视频流断掉 ，无法连接
        exit()

    streamName = b'classification'
    uniqueId = 0
    time1 = time.time()
    # 初始化检测参数，包括速度，车流量，占有率
    speed_all = 0
    car_amount_all = 0
    occupancy_all = 0
    car_count_num = 0

    # 初始化矩阵，初始化直线，车辆数等参数
    # H, V = generateNumMatric(img1)
    # 初始化直线矩阵
    line_up = generateLineMatric(Line_k=0, Line_c=600)
    line_down = generateLineMatric(Line_k=0, Line_c=750)
    # 初始化参数信息
    Car_count = [0, 0, 0, 0]
    first_Flag = True
    frame_count = 0
    Intersect_up_Flag_Last = [False, False, False, False]# 4个车道
    Intersect_down_Flag_Last = [False, False, False, False]
    Car_num_up = [0, 0, 0, 0]
    Car_num_down = [0, 0, 0, 0]
    Times_up = [0.0, 0.0, 0.0, 0.0]
    Times_down = [0.0, 0.0, 0.0, 0.0]
    Speeds = [0, 0, 0, 0]
    # 初始化统计参数
    reverse_drive_incident_count = {} # 逆行统计
    stop_incident_count = {} # 停车统计
    person_incident_count = {} # 行人统计
    
    # 代码开始运行时间
    initial_time = time.time()
    Time_plus = [0, 0, 0, 0]
    
    key1 = b'mxpi_videodecoder0'
    key2 = b'mxpi_modelinfer0'
    # key3 = b'mot_test'
    key_vec = StringVector()
    key_vec.push_back(key1)
    key_vec.push_back(key2)
    appsink = b'appsink0'
    
    event_video_play = True
    # 标志位状态
    # res = requests.get(url_signal)
    # 主程序开始，start为True时开始程序
    while 1:
        res = requests.get(url_signal)
        if json.loads(res.text)["start"]:#是否start为True

            # 得到推理结果
            inferResult = streamManagerApi.GetResult(streamName, uniqueId, 3000)
            inferResult1 = streamManagerApi.GetResult(streamName, appsink, key_vec, 3000)# get图像信息
            # res=requests.get(url) #返回一个消息实体
            metadata_output_video = inferResult1.metadataVec
            # print(type(metadata_output_video))
            # print(metadata_output_video)
            if inferResult.errorCode != 0:
                print("error!!!\n\n\n")
                print("GetResultWithUniqueId error. errorCode=%d, errorMsg=%s" % (
                    inferResult.errorCode, inferResult.data.decode()))
                exit()

            # 将推理结果转换成dict 
            infer_info = inferResult.data.decode()
            Data = json.loads(infer_info)# 变成json文件
            # 开始主程序
            center_together_info, center_together_all_center, Infer_msg_now, IDS_shili_area1, IDS_shili_area2, ids_list_car_result, person_ids, Ids_area1, Ids_area2, Ids_area3, Ids_area4 = zhu_program(Data)

            Intersect_up_Flag, Intersect_down_Flag, index_car, car_bbox_center_up, car_bbox_center_down = DetecFromOneFrame(line_up, line_down, center_together_info)
            print(Intersect_up_Flag, Intersect_down_Flag, index_car, car_bbox_center_up, car_bbox_center_down)
            # 开始检测交通参数，车流量，平均速度，占有率
            Traffic_parameter(Intersect_up_Flag, Intersect_down_Flag, index_car, car_bbox_center_up, car_bbox_center_down)
            # 检测是否过了5分钟，5分钟发送一次交通参数
            if (time.time() - initial_time) % 30 <= 0.1:
                print("yaokasihil !!!!!!!!!!!!!!!!!")
                if car_amount_all != 0:
                    occupancy = (Time_plus / car_amount_all) * 100
                    speed_average = int((speed_all / car_amount_all)*(3.6))
                else:
                    occupancy = 0
                    speed_average = 0
                    car_amount_all = 0

                post_param('km/h',speed_average,1)
                post_param('辆',car_amount_all,2)
                post_param('%',occupancy,3)
                #初始化
                Time_plus = 0
                car_amount_all = 0
                speed_all = 0
                
            if event_video_play:
                url = 'http://localhost:8000/api/event/'
                a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                realtime_car_amount = {}
                realtime_car_amount['create_time'] = a
                realtime_car_amount['ip'] = '0.0.0.0'
                realtime_car_amount['location'] = 'test_came'
                realtime_car_amount['event_type'] = 1
                realtime_car_amount['image'] = "car/fdgdfg"
                r = requests.post(url, json = realtime_car_amount)
                print(r.json())
                # time.sleep(1)
                event_video_play = False
        else:
            print("Nothing")
            continue
