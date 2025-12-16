from services.serial_service import serialRead
from services.transmission_service import transmitGP, transmitGL, startClient
from globals.globalVars import HOST_1, PORT_1, SERIAL_1, HOST_2, PORT_2, SERIAL_2, SAMPLE_TIME_INTERVAL
import asyncio
from CircularQueue.AsyncCircularQueue import AsyncCircularQueue
import multiprocessing as mp
from multiprocessing import Process, Queue
from services.snr_service import getSNR

client = None


def async_main_processed(QP1_GL, QP1_GP, QP2_GL, QP2_GP):
    asyncio.run(main_processed(QP1_GL, QP1_GP, QP2_GL, QP2_GP))

async def main_processed(QP1_GL, QP1_GP, QP2_GL, QP2_GP):
    GPSNRQueue = AsyncCircularQueue(256)
    GLSNRQueue = AsyncCircularQueue(256)
    await asyncio.gather(getSNR(QP1_GL, QP1_GP, QP2_GL, QP2_GP, GPSNRQueue, GLSNRQueue))

def async_main_raw(HOST, PORT, SERIAL, sampleTimePeriod, ProcessQueueGP, ProcessQueueGL):
    asyncio.run(main_raw(HOST, PORT, SERIAL, sampleTimePeriod, ProcessQueueGP, ProcessQueueGL))

async def main_raw(HOST, PORT, SERIAL, sampleTimePeriod, ProcessQueueGP, ProcessQueueGL):
    global client
    GPQueue = AsyncCircularQueue(256)
    GLQueue = AsyncCircularQueue(256)
    #client = await startClient(HOST, PORT)

    await asyncio.gather(serialRead(GPQueue, GLQueue, SERIAL, sampleTimePeriod, ProcessQueueGP, ProcessQueueGL)
                         , startClient(HOST, PORT)
                         , transmitGP(GPQueue, HOST, PORT)
                         , transmitGL(GLQueue, HOST, PORT))

if __name__ == "__main__":
    QP1_GP = Queue()
    QP2_GP = Queue()
    QP1_GL = Queue()
    QP2_GL = Queue()
    P1 = Process(target = async_main_raw, args =(HOST_1, PORT_1, SERIAL_1, SAMPLE_TIME_INTERVAL, QP1_GL, QP1_GP,))
    P2 = Process(target = async_main_raw, args =(HOST_2, PORT_2, SERIAL_2, SAMPLE_TIME_INTERVAL, QP2_GL, QP2_GP))
    #P3 = Process(target = async_main_processed, args = (QP1_GL, QP1_GP, QP2_GL, QP2_GP,))
    P1.start()
    P2.start()
    