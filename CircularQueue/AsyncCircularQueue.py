import asyncio

class AsyncCircularQueue:
    def __init__(self, maxsize):
        self.queue = asyncio.Queue(maxsize=maxsize)
        self.maxsize = maxsize
    
    async def put(self, item):
        if self.queue.full():
            await self.queue.get()
            self.queue.task_done()
        await self.queue.put(item)

    async def get(self):
        item = await self.queue.get()
        self.queue.task_done()
        return item
    
    def __len__(self):
        return self.queue.qsize()