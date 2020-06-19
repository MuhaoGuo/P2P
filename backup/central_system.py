import asyncio
from datetime import datetime

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
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus, ClearCacheStatus
from ocpp.v16.enums import DataTransferStatus
from ocpp.v16 import call_result
from ocpp.v16 import call


class ChargePoint(cp):                     # chargePoint 类

    @on(Action.BootNotification)           #  BootNotification 函数
    def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
    )


    @on(Action.Authorize)  #
    def on_authorize_notification(self, **kwargs):
        return call_result.AuthorizePayload(
            id_tag_info={'expiryDate':datetime.utcnow().isoformat(),
                         'parentIdTag':'123hhh',
                         'status':AuthorizationStatus.accepted
                         }
    )

    @on(Action.Heartbeat)  #
    def heartbeat_notification(self, **kwargs):
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
    )
    #
    # @on(Action.Heartbeat)  #
    # def heartbeat_notification(self, **kwargs):
    #     return call_result.HeartbeatPayload(
    #         current_time=datetime.utcnow().isoformat()
    # )


    @on(Action.StartTransaction)  #
    def start_transaction_notification(self, **kwargs):
        return call_result.StartTransactionPayload(
            transaction_id=111,
            id_tag_info={'expiryDate':datetime.utcnow().isoformat(),
                         'parentIdTag':'123hhh',
                         'status':AuthorizationStatus.accepted}

    )


    @on(Action.StopTransaction)  #
    def stop_transaction_notification(self, **kwargs):
        return call_result.StopTransactionPayload(
            id_tag_info={'expiryDate':datetime.utcnow().isoformat(),
                         'parentIdTag':'123hhh',
                         'status':AuthorizationStatus.accepted}
    )


    @on(Action.MeterValues)  # ???????????
    def meter_values_notification(self, **kwargs):
        return call_result.MeterValuesPayload(

    )

    @on(Action.StatusNotification)  #
    def status_notification(self, **kwargs):
        return call_result.StatusNotificationPayload(

        )


    @on(Action.DataTransfer)  #
    def data_transfer_notification(self, **kwargs):
        return call_result.DataTransferPayload(
            status = DataTransferStatus.accepted
        )


    async def send_clear_cache_request(self):           # 发送 请求 send_boot_notification
        print("hello")
        request = call.ClearCachePayload(

        )
        response = await self.call(request)


        if response.status == ClearCacheStatus.accepted:
            print("Clear cache Done!!!!!!!!.")
        print("it works")




async def on_connect(websocket, path):           # 等待client 链接
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    charge_point_id = path.strip('/')              # 获得client 编号 
    cp = ChargePoint(charge_point_id, websocket)   #创建ChargerPoint 实例化 记为 cp

    print("cp start")


    await cp.start()                               # cp启动  内置函数 start

    await cp.send_clear_cache_request()


async def main():
    print("hi main")
    server = await websockets.serve(               # server 启动事件， 等待clinet 函数， ip地址， 端口号， usbprotocols
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )
    # self.send_clear_cache_request()

    await server.wait_closed()                     #  等server 启动事件 结束, 就结束server  wait_closed() methods for terminating the server and cleaning up its resources.


if __name__ == '__main__':
    try:
        # asyncio.run() is used when running this example with Python 3.7 and
        # higher.
        asyncio.run(main())                 
    except AttributeError:
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop()     #得到目前的事件循环
        loop.run_until_complete(main())     #此事件一直 运行，直到main结束
        loop.close()                        #关闭事件循环
