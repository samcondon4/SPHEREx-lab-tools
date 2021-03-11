from DPY50601_async import DPY50601
import asyncio

d0 = DPY50601(0)


async def main():
    await d0.home_async(initial=True, forward_first=False)
    #await asyncio.gather(reset_enc(), motor_control())


async def motor_control():
    await d0.step_async(4000, 0)


async def reset_enc():
    await asyncio.sleep(0.25)
    d0.reset_encoder()


asyncio.run(main())

