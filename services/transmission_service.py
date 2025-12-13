import asyncio
from packets.structs import lineData
import socket
from CircularQueue.AsyncCircularQueue import AsyncCircularQueue

client = None
reconnect_lock = asyncio.Lock()

async def transmitGP(GPQueue, HOST, PORT):
    global client
    while True:
        currentGPData: lineData = await GPQueue.get()
        currentGPData.display()
        try:
            client.sendall(currentGPData.returnCSV().encode())
        except (Exception):
            print("Server disconnected! Retrying connection in 2seconds.")
            await asyncio.sleep(2)
            await startClient(HOST, PORT)

        
async def transmitGL(GLQueue, HOST, PORT):

    global client
    while True:
        currentGLData: lineData = await GLQueue.get()
        currentGLData.display()
        try:
            client.sendall(currentGLData.returnCSV().encode())
        except (Exception):
            print("Server disconnected! Retrying connection in 2seconds.")
            await asyncio.sleep(2)
            await startClient(HOST, PORT)




async def startClient(host, port):
    #print("Iwascalled")
    global client
    loop = asyncio.get_event_loop()

    async with reconnect_lock:
        if client:
            try:
                client.getpeername()
                return client
            except Exception:
                print("Reconnect lock exception.")
                client = None
        
        print("Finished reconnect lock exception")

        while True:
            try:
                temp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_client.setblocking(False)
                #client.connect((host, port))
                print("Trying to connect to server!")
                await asyncio.wait_for(loop.sock_connect(temp_client, (host, port)), timeout=2)
                client = temp_client
                print(f"Connected to server {host}:{port}")
                break
            except:
                print("Couldn't connect to server. Maybe server's down! Retrying in 5 seconds")
                #time.sleep(5)
                await asyncio.sleep(5)
    return client
