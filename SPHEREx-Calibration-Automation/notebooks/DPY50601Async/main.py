from DPY50601_async import DPY50601
import asyncio


async def main():
    d0 = DPY50601(0)
    print("encoder position = {}".format(d0.enc_pos))
    await d0.step_async(4000, 0)
    print("encoder position = {}".format(d0.enc_pos))
    await d0.step_async(4000, 0)
    print("encoder position = {}".format(d0.enc_pos))
    await d0.home_async()
    print("encoder position = {}".format(d0.enc_pos))

asyncio.run(main())



