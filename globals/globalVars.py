import asyncio

IMUPACKET_CHECKSUM = 0xAA
OTHERSENSORSPACKET_CHECKSUM = 0x55

SAMPLE_TIME_INTERVAL = 5 #1 data every 5 seconds.

HOST_1 = "192.168.1.150"
SERIAL_1 = '/dev/ttyACM1'
PORT_1 = 8085
PATH_1 = "/home/glstation/BackupFromPi/Documents/Logs/GNSS/RECEIVER1"

HOST_2 = "192.168.1.75"
PORT_2 = 8086
SERIAL_2 = '/dev/ttyACM3'
PATH_2 = "/home/glstation/BackupFromPi/Documents/Logs/GNSS/RECEIVER2"


