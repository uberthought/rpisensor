#!/usr/bin/python3

import serial, struct, sys, time

DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1

def dump(d, prefix=''):
    print(prefix + ' ' + str(d))

def construct_command(cmd, data=[]):
    assert len(data) <= 12
    data += [0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = chr(0xaa) + chr(0xb4) + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += chr(0xff) + chr(0xff) + chr(checksum) + chr(0xab)

    ret = ret.encode('latin1')

    if DEBUG:
        dump(ret, '> ')

    return ret

def process_data(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(v for v in d[2:8])%256
    return [pm25, pm10]

def process_version(d):
    r = struct.unpack('<BBBHBB', d[3:])
    checksum = sum(v for v in d[2:8])%256
    print("Y: {}, M: {}, D: {}, ID: {}, CRC={}".format(r[0], r[1], r[2], hex(r[3]), "OK" if (checksum==r[4] and r[5]==0xab) else "NOK"))

class SDS011Sensor:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        # ser.open()
        self.ser.flushInput()

    def read_response(self):
        byte = 0
        while byte != b'\xaa':
            byte = self.ser.read(size=1)

        d = self.ser.read(size=9)

        if DEBUG:
            dump(d, '< ')
        return byte + d

    def cmd_set_mode(self, mode=MODE_QUERY):
        self.ser.write(construct_command(CMD_MODE, [0x1, mode]))
        self.read_response()

    def cmd_query_data(self):
        self.ser.write(construct_command(CMD_QUERY_DATA))
        d = self.read_response()
        values = []
        if d[1] == 0xc0:
            values = process_data(d)
        return values

    def cmd_set_sleep(self, sleep=1):
        mode = 0 if sleep else 1
        self.ser.write(construct_command(CMD_SLEEP, [0x1, mode]))
        self.read_response()

    def cmd_set_working_period(self, period):
        self.ser.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
        self.read_response()

    def cmd_firmware_ver(self):
        self.ser.write(construct_command(CMD_FIRMWARE))
        d = self.read_response()
        process_version(d)

    def cmd_set_id(self, id):
        id_h = (id>>8) % 256
        id_l = id % 256
        self.ser.write(construct_command(CMD_DEVICE_ID, [0]*10+[id_l, id_h]))
        self.read_response()

    def read_sensor(self):
        values = None
        self.cmd_set_mode(1);
        for t in range(15):
            values = self.cmd_query_data();
            if values is not None:
                # print("PM2.5: ", values[0], ", PM10: ", values[1])
                break
        self.cmd_set_sleep(0)
        return values


if __name__ == "__main__":
    sensor = SDS011Sensor()

    sensor.cmd_firmware_ver()

    while True:
        values = sensor.read_sensor()
        if values is not None:
            print("PM2.5: ", values[0], ", PM10: ", values[1])
            time.sleep(10)
