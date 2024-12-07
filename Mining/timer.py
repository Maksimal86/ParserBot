import time
import asyncio

async def timer(timetime):

    print(time.strftime("%X", time.localtime()), timetime)
    t=time.strftime("%X", time.localtime())
    # asyncio.sleep(60)
    if int(t.replace(':', '')) <= int(timetime.replace(':', ''))+100 \
            and int(t.replace(':', '')) >= int(timetime.replace(':', ''))-100:
        print('timer return True'+timetime, t, int(timetime.replace(':', '')), int(t.replace(':', '')),int(timetime.replace(':', ''))+1000, int(timetime.replace(':', ''))-1000)
        return True
    else:
        print('timer return False '+timetime, t, int(timetime.replace(':', '')), int(t.replace(':', '')))


if __name__ == '__main__':
    asyncio.run(timer(timetime='11:28:00'))


