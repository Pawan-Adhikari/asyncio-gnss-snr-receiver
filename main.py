from services.serial_service import serialRead
from services.transmission_service import transmitGP, transmitGL, startClient
from globals.globalVars import HOST_1, PORT_1, SERIAL_1, HOST_2, PORT_2, SERIAL_2, SAMPLE_TIME_INTERVAL
import asyncio
from CircularQueue.AsyncCircularQueue import AsyncCircularQueue
import multiprocessing as mp
from multiprocessing import Process

client = None

def async_main(HOST, PORT, SERIAL, sampleTimePeriod):
    asyncio.run(main(HOST, PORT, SERIAL, sampleTimePeriod))

async def main(HOST, PORT, SERIAL, sampleTimePeriod):
    global client
    GPQueue = AsyncCircularQueue(256)
    GLQueue = AsyncCircularQueue(256)
    #client = await startClient(HOST, PORT)

    await asyncio.gather(serialRead(GPQueue, GLQueue, SERIAL, sampleTimePeriod)
                         , startClient(HOST, PORT)
                         , transmitGP(GPQueue, HOST, PORT)
                         , transmitGL(GLQueue, HOST, PORT))

if __name__ == "__main__":
    P1 = Process(target = async_main, args =(HOST_1, PORT_1, SERIAL_1, SAMPLE_TIME_INTERVAL))
    P2 = Process(target = async_main, args =(HOST_2, PORT_2, SERIAL_2, SAMPLE_TIME_INTERVAL))
    P1.start()
    P2.start()
    