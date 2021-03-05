from DPY50601_async import DPY50601
import asyncio
import msvcrt
import time


async def main():
    d0 = DPY50601(0)
    await d0.home_async()


asyncio.run(main())
