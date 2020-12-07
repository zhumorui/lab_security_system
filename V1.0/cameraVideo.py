# -*- coding: utf-8 -*-
import StringIO

import cv2
import socket
import time
from PIL import Image
import io
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
# 用python2
# 电脑终端
# 注意IP地址和端口号与前面的程序中的保持一致
HOST, PORT = "192.168.1.101", 47724
# 连接到服务器
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
f = sock.makefile()

cv2.namedWindow("camera")

while True:
    # 从服务器读取数据，一行的结尾是'\n'，注意我们前面已经将每一帧数据的'\n'替换成'\-n'，而结尾就是'\n'
    msg = f.readline()
    if not msg:
        break
    print(len(msg), msg[-2])
    # 将'\-n'换回来成'\n'
    jpeg = msg.replace("\-n", "\n")
    buf = StringIO.StringIO(jpeg[0:-1])  # 缓存数据
    buf.seek(0)
    pi = Image.open(buf)  # 使用PIL读取jpeg图像数据
    # img = np.zeros((640, 480, 3), np.uint8)
    img = cv2.cvtColor(np.asarray(pi), cv2.COLOR_RGB2BGR)  # 从PIL的图像转成opencv支持的图像
    buf.close()
    cv2.imshow("camera", img)  # 实时显示
    if cv2.waitKey(10) == 27:
        break

sock.close()
cv2.destroyAllWindows()
