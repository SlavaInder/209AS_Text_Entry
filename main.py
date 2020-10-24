# this file makes use of code presented in this resources
# https://stackoverflow.com/questions/24214643/python-to-automatically-select-serial-ports-for-arduino
import logging
import serial
from serial.tools import list_ports


# connection parameters
ARDUINO_NAME = "seeduino"
BAUD_RATE = 9600
TIME_OUT = 10
NUM_BYTES = 1


# set up log messages for connect
msg_arduino_adapter_connect_start = "Adapter started searching for connected arduino"
msg_arduino_adapter_no_device_found = "Adapter has not found any connected devices"
msg_arduino_adapter_device_found = "Adapter found {name} connected to {port}"
msg_arduino_adapter_connect_failed = "No arduino is found"
msg_arduino_adapter_connect_successful = "Adapter connected to an arduino device on port {port}"


# this class handles connection with arduino:
class ArduinoAdapter(object):
    def __init__(self):
        self.serial = None
        self.port_name = None
        self.baud_rate = BAUD_RATE
        self.time_out = TIME_OUT
        self.num_bytes = NUM_BYTES

    # establishes connection with arduino
    def connect(self):
        # start logging
        logging.info(msg_arduino_adapter_connect_start)
        # get the list of all connected devices
        devices = list_ports.comports()
        # if no device is found raise the warning
        if len(devices) == 0:
            logging.warning(msg_arduino_adapter_no_device_found)
            raise IOError(msg_arduino_adapter_no_device_found)
        # if there are some connected devices
        else:
            for i in range(len(devices)):
                # log the device name
                logging.info(msg_arduino_adapter_device_found.format(name=devices[i][1].lower(), port=devices[i][0]))
                # check if this device is an arduino
                if ARDUINO_NAME in devices[i][1].lower():
                    # if it is, establish connection with it
                    self.serial = serial.Serial(devices[i][0], self.baud_rate)
                    # report successful connection
                    logging.info(msg_arduino_adapter_connect_successful.format(port=devices[i][0]))
                    # exit function
                    return
            # if no arduino was found among devices
            logging.warning(msg_arduino_adapter_connect_failed)
            raise IOError(msg_arduino_adapter_connect_failed)

    # read a symbol from COM port
    def read(self):
        return self.serial.read(self.num_bytes, timeout=self.time_out)


if __name__ == '__main__':
    # setup logging
    logging.basicConfig(filename='logs/main_execution.log', filemode='w', level=logging.DEBUG)
    # init adapter
    my_adapter = ArduinoAdapter()
    # connect adapter and arduino
    my_adapter.connect()

    while True:
        print(my_adapter.read())
