from DPY50601_async import DPY50601
import asyncio
import time


async def main():
    d0 = DPY50601(0)
    d0.slew(0)
    time.sleep(2)
    d0.stop()

asyncio.run(main())
