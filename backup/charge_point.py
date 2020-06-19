import asyncio

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp.routing import on
from ocpp.v16 import call
from ocpp.v16 import call_result
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus, Action, ClearCacheStatus


class ChargePoint(cp):                               # cp 作为 ocpp 的 实例
    async def send_boot_notification(self):           # 发送 请求 send_boot_notification
        request = call.BootNotificationPayload(  
            charge_point_model="Optimus",
            charge_point_vendor="NOEVmh_vendor"
        )

        response = await self.call(request)      

        if response.status ==  RegistrationStatus.accepted:
            print("Connected to central system!!!!!!!!.")


    @on(Action.ClearCache)
    def clear_cache_notification(self):
        print("clear cache")
        return call_result.ClearCachePayload(
            status=ClearCacheStatus.accepted
    )





async def main():
    async with websockets.connect(                 # 链接
        'ws://localhost:9000/CP_1',                # 目的地址  +  序号 
         subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_1', ws)          #  实例化cp 包含名字和 ws 协议

        await asyncio.gather(cp.start(),
                             cp.send_boot_notification(),
                             # cp.clear_cache_notification()
                             )   #先start ，在发送

if __name__ == '__main__':
    try:
        # asyncio.run() is used when running this example with Python 3.7 and
        # higher.
        asyncio.run(main())
    except AttributeError:
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
