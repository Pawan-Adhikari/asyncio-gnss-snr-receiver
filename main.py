from services.serial_service import serialRead
from services.transmission_service import transmitGP, transmitGL, startClient
from globals.globalVars import HOST, PORT
import asyncio
from CircularQueue.AsyncCircularQueue import AsyncCircularQueue

client = None

async def main():
    global client
    GPQueue = AsyncCircularQueue(256)
    GLQueue = AsyncCircularQueue(256)
    #client = await startClient(HOST, PORT)

    await asyncio.gather(serialRead(GPQueue, GLQueue), startClient(HOST, PORT), transmitGP(GPQueue), transmitGL(GLQueue))

if __name__ == "__main__":
    asyncio.run(main())