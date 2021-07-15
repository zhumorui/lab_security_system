# -*- coding: utf-8 -*-
import cv2
import time
import socket
from PIL import Image
import StringIO

# 获取摄像头
cap = cv2.VideoCapture(0)
# 调整采集图像大小为640*480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

# 这里的HOST对应树莓派的IP地址（自己输入ifconfig查），端口号自己随便定一个即可，但注意后面的程序中要保持统一
HOST, PORT = '192.168.191.2', 47724
# 连接服务器
sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    # 获取一帧图像
    ret, img = cap.read()
    # 如果ret为false，表示没有获取到图像，退出循环
    if ret is False:
        print("can not get this frame")
        continue    

    # 将opencv下的图像转换为PIL支持的格式
    pi = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    buf = StringIO.StringIO()# 缓存对象
    pi.save(buf, format='PNG')# 将PIL下的图像压缩成jpeg格式，存入buf中
    jpeg = buf.getvalue()# 从buf中读出jpeg格式的图像
    buf.close()
    transfer = jpeg.replace('\n', '\-n')# 替换\n为\-n，因为后面传输时，终止的地方会加上\n，可以便于区分
    print len(transfer), transfer[-1]
    sock.sendall(transfer + "\n")# 通过socket传到服务器
    # time.sleep(0.2)

sock.close()
