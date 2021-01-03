import time
from Talos import Tello


class Test:
    def __init__(self):
        self.drone = Tello.Tello()

    def connection_test(self):
        self.drone.send_command('command')
        # time.sleep(2)
        self.drone.send_command('takeoff')
        time.sleep(1)
        self.drone.send_command('land')


Test1 = Test()
Test1.connection_test()
Test1.drone.get_status()
#exit()
