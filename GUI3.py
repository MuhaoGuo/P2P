
from tkinter import *
from tkinter import ttk
def compute_center(screen_w, screen_h, win_w, win_h):
    center_x = screen_w / 2 - win_w / 2
    center_y = screen_h / 2 - win_h / 2
    return center_x, center_y
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
from ocpp.v16.enums import RegistrationStatus, Action, ClearCacheStatus, RemoteStartStopStatus


import json


class GUI(cp):
    # async def send_boot_notification(self):           #
    #     request = call.BootNotificationPayload(
    #         charge_point_model="Optimus",
    #         charge_point_vendor="NOEVmh_vendor"
    #     )
    #
    #     response = await self.call(request)
    #
    #     if response.status ==  RegistrationStatus.accepted:
    #         print("Connected to central system!!!!!!!!.")

    # 8
    async def data_transfer(self):

        # print("message_from_gui is ",message_from_gui)
        # print(json.load(message_from_gui))

        # print ("data_j is" , data_j)


        data = {
            "cp_id": "CP_8",
            "max_watts": 1200,
            "max_current": None,
        }
        data_j = json.dumps(data)

        request = call.DataTransferPayload(
            vendor_id="MOEV_GUI",
            message_id="start remote transaction",
            # message_id="stop remote transaction",
            # message_id="show current evses",
            data=data_j,
        )
        response = await self.call(request)

        # da = response.__dict__["data"]
        #
        # print(da)

        print("response is ", response)

        # if response.status == RegistrationStatus.accepted:
        #     print("server accepted the message from gui")
        #     print("response.data is:", response.data)

    # @on(Action.ClearCache)
    # def clear_cache_notification(self,**kwargs):
    #     print("2.client receive clear cache request and will return accepted")
    #     return call_result.ClearCachePayload(
    #         status=ClearCacheStatus.accepted
    # )
    # #
    # @on(Action.RemoteStartTransaction)  #
    # def remote_start_transaction_notification(self,**kwargs):
    #     print("2.client receive remote start transaction request and will return accepted")
    #     return call_result.RemoteStartTransactionPayload(
    #         status=RemoteStartStopStatus.accepted
    #     )
    # #
    #
    # @on(Action.RemoteStopTransaction)  #
    # def remote_stop_transaction_notification(self, **kwargs):
    #     print("2.client receive remote stop transaction request and will return accepted")
    #     return call_result.RemoteStopTransactionPayload(
    #         status=RemoteStartStopStatus.accepted
    #     )
#
# message_from_gui_list= [
#     # str({"data":"111"}),
#     "show current evses",
#     "start remote transaction",
#     "stop remote transaction",
#     ]
# message = "show current evses"
# # message = (cp_id= 1,  data=start remote transaction)

async def main():
    async with websockets.connect(
        'ws://10.2.38.117:9000/GUI',
         subprotocols=['ocpp1.6']
    ) as ws:
        gui = GUI('GUI', ws)

        # print("please input the id:")
        # id = input()
        # print("please input the command:")
        # command = input()

        # data1 = {"command": "show current evses"}
        # data2 = {"cp_id":"CP_m", "command":"start remote transaction", "current":"100"}
        #
        # data3 = {"cp_id":"CP_m", "command":"stop remote transaction"}
        #


        # print(data)
        # async def send(data):
        # data_j = json.dumps(data1)   # dict(obj) to str       将Python对象编码成 json字符串 都是双引号
        #
        #
        #
        # # 参数 ：
        # command = ["show current evses",
        #            "start remote transaction",
        #            "stop remote transaction",
        #            "clear charging profile",
        #            "change max watts",
        #            ]
        # cp_id =[]
        # max_watts =[]






        #
        # def fun1():
        #     data1 = {"command": "show current evses"}
        #     data_j = json.dumps(data1)
        #     return data_j
        #
        # def fun2():
        #     data1 = {"cp_id":"CP_m", "command": "start remote transaction"}
        #     data_j = json.dumps(data1)
        #     return data_j
        #
        # def fun3():
        #     data1 = {"cp_id":"CP_m", "command": "stop remote transaction"}
        #     data_j = json.dumps(data1)
        #     return data_j
        #
        # def fun4():
        #     data1 = {"cp_id": "CP_m", "command": "clear charging profile"}
        #     data_j = json.dumps(data1)
        #     return data_j
        #
        #
        # def fun5():
        #     data1 = {"cp_id": "CP_m", "command": "change max watts", "max_watts": 1200}
        #     data_j = json.dumps(data1)
        #     return data_j



        # root = Tk()
        # root.title('Server')
        #
        # Button(root, text="show current EVSEs", command=lambda: fun1()).place(relx=0.2, rely=0.1, anchor=CENTER)


        # async def run_tk(root, interval=0.05):
        #     '''
        #     Run a tkinter app in an asyncio event loop.
        #     '''
        #     try:
        #         while True:
        #             root.update()
        #             await asyncio.sleep(interval)
        #     except TclError as e:
        #         if "application has been destroyed" not in e.args[0]:
        #             raise

        # await run_tk(root)


        await asyncio.gather(
                             gui.start(),        #必须先start 的才能发送其他
                             # gui.data_transfer(fun4()),
                             gui.data_transfer(),
                             # gui.data_transfer(fun3())
                             )
        mainloop()
        # asyncio.run(send(data1))


if __name__ == '__main__':
    # try:
    #     # asyncio.run() is used when running this example with Python 3.7 and
    #     # higher.
    asyncio.run(main())
    # except AttributeError:
    #     # For Python 3.6 a bit more code is required to run the main() task on
    #     # an event loop.
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(main())
    #     loop.close(




