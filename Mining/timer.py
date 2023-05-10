import time
import asyncio

async def timer(timetime):

    print(time.strftime("%X", time.localtime()), timetime)
    t=time.strftime("%X", time.localtime())
    await  asyncio.sleep(60)
    if int(t.replace(':', '')) <= int(timetime.replace(':', ''))+200 \
            and int(t.replace(':', '')) >= int(timetime.replace(':', ''))-200:
        print('timer return True'+timetime, t, int(timetime.replace(':', '')), int(t.replace(':', '')),int(timetime.replace(':', ''))+100, int(timetime.replace(':', ''))-100)
        return True
    else:
        print('timer return False'+timetime, t, int(timetime.replace(':', '')), int(t.replace(':', '')))


if __name__ == '__main__':
    timer(timetime='16:22:00')

