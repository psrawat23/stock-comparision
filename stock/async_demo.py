import _asyncio, asyncio
import time

import asyncio
from threading import Thread

async def sample_coroutine():
    print("I am hee")
    await asyncio.sleep(1)
    return 1


async def sample_coroutine1():
    print("I am not")
    await asyncio.sleep(1)
    return 1
range()
async def main():
    # Start a few coroutines
    loop = asyncio.get_running_loop()
    print(loop)

    loop.create_task(sample_coroutine())
    loop.create_task(sample_coroutine1())

    # await asyncio.gather(sample_coroutine(),sample_coroutine())

    print("Ending the loop")
    
    # Get all tasks in the current event loop
    tasks = asyncio.all_tasks()
    
    for task in tasks:
        print(f"Task: {task}, State: {task._state}")

# Run the main function in the event loop
asyncio.run(main())



# asyncio.run(demo())

# asyncio.run(demo(start=10,end=20))
# with open("/Users/purushottamsingh/Desktop/DJANGO_API/Stock Trading/stock/async_demo.py") as file:
#     exec(file.read())