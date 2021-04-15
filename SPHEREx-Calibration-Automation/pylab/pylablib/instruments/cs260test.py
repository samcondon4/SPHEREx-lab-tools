from CS260 import *
import asyncio


exe_path = ".\\CS260-Drivers\\C++EXE.exe"


async def main():
    cs = CS260(exe_path)
    write_task = asyncio.create_task(cs.set_grating(3))
    write_task2 = asyncio.create_task(cs.set_filter(3))
    fib_task = asyncio.create_task(fibonacci(100000))
    #await write_task
    await asyncio.gather(write_task, fib_task, write_task2)


async def fibonacci(nterms):
    n1, n2 = 0, 1
    count = 0
    if nterms <= 0:
        return
    elif nterms == 1:
        print("fib{} = {}".format(count, n1))
    else:
        while count < nterms:
            nth = n1 + n2
            print("fib{} = {}".format(count, nth))
            n2 = n1
            n1 = nth
            count += 1
            await asyncio.sleep(0.0001)


asyncio.run(main())
