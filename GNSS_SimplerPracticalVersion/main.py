import threading
import serial
import queue
from services.serial_service import serialRead


GPQueue = queue.Queue(256)
GLQueue = queue.Queue(256)

serialRead(GPQueue, GLQueue, "/dev/ttyACM1", 5) 