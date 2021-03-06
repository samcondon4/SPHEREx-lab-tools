from DPY50601_async import DPY50601
import asyncio
import msvcrt
import time


async def main():
    await asyncio.gather(motor_control(), fibonacci(100000))


async def motor_control():
    d0 = DPY50601(0)
    #run initial home operation for sanity-check
    await d0.home_async(initial=True, forward_first=True)
    #move motor 4000 steps in ccw direction
    await d0.step_async(4000, 0) #
    #move motor 1000 steps cw
    await d0.step_async(1000, 1)
    #move motor 2000 steps ccw
    await d0.step_async(2000, 0)
    #run home operation
    await d0.home_async(forward_first=False)


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


