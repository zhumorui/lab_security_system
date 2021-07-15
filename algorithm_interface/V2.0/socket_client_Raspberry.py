import cv2
import io
import socket
import struct
import time
import pickle


class SocketClient(object):
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        print("connect now,wait...")
        self.client_socket.connect((host, port))
        print("connecting successful...")
        connection = self.client_socket.makefile('wb')

    def send_frame(self, frame):
        data = pickle.dumps(frame, 0)
        size = len(data)
        self.client_socket.sendall(struct.pack(">L", size) + data)
