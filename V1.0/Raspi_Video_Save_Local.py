#!/usr/bin/python3
# -*- coding:utf-8 -*-
 
#保存一段视频到本地
 
import cv2
import numpy
 
#初始化摄像头
camera = cv2.VideoCapture(0)
 
# 设置编码格式
fourcc = cv2.VideoWriter_fourcc(*'XVID') # mpeg4编码
#设置帧频
fps =24
#设置分辨率
framesize = (640,480)
#设置摄像头输出
out = cv2.VideoWriter('output.avi',fourcc,fps,framesize)
 
while True:
        ret , frame = camera.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #写数据到本地
        out.write(frame)
        if cv2.waitKey(1) & 0xff == ord('q') : # 按下q退出循环
            break
#释放资源
camera.release()
out.release()
cv2.destroyAllWindows()