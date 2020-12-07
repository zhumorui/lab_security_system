import io
import time
import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
import socket
import pickle
import numpy as np
import struct

#
# from pydub import AudioSegment
# from pydub.playback import play
from PIL import Image


class Interface:
    def __init__(self):
        # self.alert_sound = AudioSegment.from_wav('./assets/alert.wav')
        self.host = '192.168.43.52'
        self.port = 24485
        '''
        转移识别功能⬇
        '''
        self.fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
        self.out = cv2.VideoWriter('py3_Video.avi', cv2.VideoWriter_fourcc(*'JPEG'), 24,
                                   (640, 480))  # 'I', '4', '2', '0'

    def play_alert(self):
        pass
        # play(self.alert_sound)

    def add_img(self, name):
        window = tkinter.Tk()
        window.title(name)

        cv_img = cv2.cvtColor(cv2.imread(name), cv2.COLOR_BGR2RGB)
        height, width, no_channels = cv_img.shape
        canvas = tkinter.Canvas(window, width=width, height=height)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
        canvas.pack()
        self.play_alert()

        window.mainloop()

    def run_socket_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        print('Server started')

        conn, addr = s.accept()
        print("connected by :", addr)
        data = b""
        payload_size = struct.calcsize(">L")

        while True:
            while len(data) < payload_size:
                print("Recv: {}".format(len(data)))
                data += conn.recv(4096)

            print("Done Recv: {}".format(len(data)))
            packed_msg_size = data[:payload_size]  # 包头
            data = data[payload_size:]  # 真实数据
            msg_size = struct.unpack(">L", packed_msg_size)[0]  # 真实数据的长度
            print("msg_size: {}".format(msg_size))
            # 如果丢包，直接接收后来的数据包
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]  # 抓取真实的数据长度
            data = data[msg_size:]  # 剩余数据下次循环

            frame = pickle.loads(
                frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            '''
            根据frame识别结果，触发
            '''
            #做一个缓冲的转化
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)#COLOR_BGR2GRAY
            pi = Image.fromarray(gray)
            buf = io.BytesIO()
            pi.save(buf, format='JPEG')
            pi = Image.open(buf)
            img = cv2.cvtColor(np.asarray(pi), cv2.COLOR_RGB2BGR)
            buf.close()
            #缓冲转化结束
            fire = self.fire_cascade.detectMultiScale(img, 1.2, 5)#frame
            for (x, y, w, h) in fire:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)#frame
                # font = cv2.FONT_HERSHEY_SIMPLEX
                # roi_gray = gray[y:y + h, x:x + w]
                # roi_color = frame[y:y + h, x:x + w]
                time.sleep(0.2)
                print('Detected')
                image_name = "img{}.jpg".format(addr[0])
                cv2.imwrite(image_name, img)#frame
            '''
            以上是加入部分
            '''
            self.out.write(img)#frame
            cv2.imshow("video", img)#frame
            # image_name = "img{}.jpg".format(addr[0])
            # cv2.imwrite(image_name, frame)
            # self.add_img(image_name)
            cv2.waitKey(1)


if __name__ == "__main__":
    interface = Interface()

    interface.run_socket_server()
