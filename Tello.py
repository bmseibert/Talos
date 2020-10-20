import threading
import socket
import sys
import time
import platform


class Tello:
    def __init__(self):
        self.host = ''
        self.port = 9000
        self.locaddr = (self.host, self.port)
        self.tello_address = ('192.168.10.1', 8889)
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
        except socket.error as err:
            print(err)

    def recv(self):
        count = 0
        while True:
            try:
                data, server = self.sock.recvfrom(1518)
                print("Command Status: " + data.decode(encoding="utf-8"))
            except Exception:
                print('\nExit . . .\n')
                break

    def begin_recv(self):
        recv_thread = threading.Thread(target=self.recv)
        recv_thread.start()

    def send_command(self, command):
        msg = command.encode(encoding="utf-8")
        sent = self.sock.sendto(msg, self.tello_address)
        return sent

    def get_status(self):
        speed = self.send_command('speed?')
        battery = self.send_command('battery?')
        current_time = self.send_command('time?')
        height = self.send_command('height?')

        print('-----------Informaiton------------')
        print('Speed: %f cm/s' % float(speed))
        print('Battery: %f %%' % float(battery))
        print('Time: %f' % float(current_time))
        print('Height: %f' % float(height))