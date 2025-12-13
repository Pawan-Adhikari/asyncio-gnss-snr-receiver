
'''
from pathlib import Path 
import asyncio
import time
from packets.structs import IMUData, OtherSensorsData


def getIMUFileName():
    filename = f"IMUData_{int(time.time())}.csv"
    return filename

def getOtherSensorsFileName():
    filename = f"OtherSensorsData_{int(time.time())}.csv"
    return filename


async def SaveLocallyIMU(savePath: Path, IMUQueue_SD):
    savePath = Path(savePath)
    savePath.mkdir(parents=True, exist_ok=True)
    filePath = savePath / getIMUFileName()
    count = 0
    buffer = []

    with open(filePath, 'w') as file:
        while True:
            currentIMUData: IMUData = await IMUQueue_SD.get()
            buffer.append(currentIMUData.returnCSV())
            if len(buffer) >= 100:
                print("Added 100 lines!")
                file.writelines(buffer)
                file.flush()
                buffer.clear()


async def SaveLocallyOtherSensors(savePath: Path, OtherSensorsQueue_SD):
    savePath = Path(savePath)
    savePath.mkdir(parents=True, exist_ok=True)
    filePath = savePath / getOtherSensorsFileName()
    count = 0
    buffer = []

    with open(filePath, 'w') as file:
        while True:
            currentOtherSensorsData: OtherSensorsData = await OtherSensorsQueue_SD.get()
            buffer.append(currentOtherSensorsData.returnCSV())
            if len(buffer) >= 10:
                file.writelines(buffer)
                file.flush()
                buffer.clear()

'''





