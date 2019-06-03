import serial
import time


class LegoSerial:
    def __init__(self, port_name):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.port = port_name
        self.ser.timeout = 1

    def open_serial(self):
        try:
            self.ser.open()
        except (OSError, serial.SerialException):
            pass

    def close_serial(self):
        self.ser.close()

    def send_data(self, data, simulating=False):

        if not self.ser.is_open and not simulating:
            return

        data_str = ''
        for byte in data:
            data_str = data_str + chr(byte)

        if not simulating:
            self.ser.write(data_str.encode('latin_1'))
        else:
            print('Data length is: ' + str(len(data_str)))
            print(data_str)

    def get_response(self, data, send_delay=0, timeout=0.15):
        """Sends data and waits a little while for a response. Then encodes to an int array"""

        time.sleep(send_delay)

        if not self.ser.is_open:
            return

        self.ser.read(self.ser.inWaiting())  # Clear out what is currently waiting.

        self.send_data(data)
        time.sleep(timeout)  # The microcontroller should reply within 10 ms. 150 ms is plenty of time.

        in_data = self.ser.read(self.ser.inWaiting())
        values = []

        for char in in_data:
            values.append(char)

        return values
