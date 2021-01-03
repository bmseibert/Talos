from datetime import datetime
import threading
import socket
import time
import curses


class TelloState:
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8890
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_adderss = (self.tello_ip, self.tello_port)
        self.socket.sendto('command'.encode('utf-8'), self.tello_adderss)
        # State contains [pitch, roll, yaw, vgx, vgy, vgz, templ, temph, tof, h, bat, baro, time, agx, agy, agz]
        self.state = []

        self.begin_recv()

    def recv(self):
        index = 0
        while True:
            index += 1
            response, ip = self.socket.recvfrom(1024)
            if response == 'ok':
                continue
            out = response.decode('utf-8')
            out_split = out.split(';')
            self.report(out_split)
            time.sleep(0.2)

    def begin_recv(self):
        recv_thread = threading.Thread(target=self.recv)
        recv_thread.start()

    def report(self, raw_str):
        result = []
        for i in range(len(raw_str) - 1):
            temp = raw_str[i].split(':')
            if temp != 'ok':
                result.append(temp[1])
        self.state = result
        print([s for s in raw_str])
