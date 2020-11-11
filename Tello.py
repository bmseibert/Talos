import threading
import socket
import cv2
import time
from Talos import TelloState


class Tello:
    def __init__(self):
        self.host = ''
        self.port = 9000
        self.locaddr = (self.host, self.port)
        self.tello_address = ('192.168.10.1', 8889)
        self.speed = 0
        self.battery = 0
        self.current_time = 0
        self.height = 0
        # Video Streaming Parameters
        self.stream_state = True
        self.last_frame = None
        self.State = TelloState.TelloState()
        # Create a UDP socket
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as err:
            print(err)
            exit()
        self.sock.bind(self.locaddr)
        self.begin_recv()
        # Send Initialization command 'command' to Tello
        try:
            self.send_command('command')
            time.sleep(5)
            self.stream_video()
        except socket.error as err:
            print(err)

    def recv(self):
        count = 0
        while True:
            try:
                data, server = self.sock.recvfrom(1518)
                # print("Command Status: " + data.decode(encoding="utf-8"))
                self.send_command('speed?')
                data, server = self.sock.recvfrom(1518)
                self.speed = data.decode(encoding="utf-8")
                self.send_command('battery?')
                data, server = self.sock.recvfrom(1518)
                self.battery = data.decode(encoding="utf-8")
                # self.send_command('time?')
                # data, server = self.sock.recvfrom(1518)
                # self.current_time = data.decode(encoding="utf-8")
                self.send_command('height?')
                data, server = self.sock.recvfrom(1518)
                self.height = data.decode(encoding="utf-8")
            except Exception:
                print('\nExit . . .\n')
                break

    def begin_recv(self):
        recv_thread = threading.Thread(target=self.recv)
        recv_thread.start()

    def stream_video(self):
        self.send_command('streamon')
        self.stream_state = True
        self.video_thread = threading.Thread(target=self._video_thread)
        self.video_thread.daemon = True
        self.video_thread.start()

    def _video_thread(self):
        # Creating stream capture object
        cap = cv2.VideoCapture('udp://' + self.tello_address[0] + ':11111')
        # Runs while 'stream_state' is True
        while self.stream_state:
            ret, self.last_frame = cap.read()
            cv2.imshow('DJI Tello', self.last_frame)

            # Video Stream is closed if escape key is pressed
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    def send_command(self, command):
        msg = command.encode(encoding="utf-8")
        self.sock.sendto(msg, self.tello_address)

    def get_status(self):

        print('-----------Informaiton------------')
        print('Speed: %f cm/s' % float(self.speed))
        print('Battery: %f %%' % float(self.battery))
        print('Time: %f' % float(self.current_time))
        # print('Height: ' + self.height)