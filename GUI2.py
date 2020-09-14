import asyncio
import threading
try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

# from ocpp.routing import on
# from ocpp.v16 import call
# from ocpp.v16 import call_result
# from ocpp.v16 import ChargePoint as cp
# from ocpp.v16.enums import RegistrationStatus, Action, ClearCacheStatus, RemoteStartStopStatus
#
#
# class ChargePoint(cp):                               # cp 作为 ocpp 的 实例
#     async def send_boot_notification(self):           #
#         request = call.BootNotificationPayload(
#             charge_point_model="Optimus",
#             charge_point_vendor="NOEVmh_vendor"
#         )
#
#         response = await self.call(request)
#
#         if response.status ==  RegistrationStatus.accepted:
#             print("Connected to central system!!!!!!!!.")
#
#     #
#     @on(Action.ClearCache)
#     def clear_cache_notification(self,**kwargs):
#         print("2.client receive clear cache request and will return accepted")
#         return call_result.ClearCachePayload(
#             status=ClearCacheStatus.accepted
#     )
#     #
#     @on(Action.RemoteStartTransaction)  #
#     def remote_start_transaction_notification(self,**kwargs):
#         print("2.client receive remote start transaction request and will return accepted")
#         return call_result.RemoteStartTransactionPayload(
#             status=RemoteStartStopStatus.accepted
#         )
#     #
#
#     @on(Action.RemoteStopTransaction)  #
#     def remote_stop_transaction_notification(self, **kwargs):
#         print("2.client receive remote stop transaction request and will return accepted")
#         return call_result.RemoteStopTransactionPayload(
#             status=RemoteStartStopStatus.accepted
#         )


# class Gui():
#     def __init__(self):
#
#     def remote_start_transcation(self):

from tkinter import *
from tkinter import ttk

def compute_center(screen_w, screen_h, win_w, win_h):
    center_x = screen_w / 2 - win_w / 2
    center_y = screen_h / 2 - win_h / 2
    return center_x, center_y


class SEND():

    def __init__(self,root):
        self.root = root


    def test(self):
        print("wwwwww")

    # def show_current_evses(rx,ry):
    #
    #     print(EVSE_dict)
    #     for evse_id in EVSE_dict:
    #         rb = Radiobutton(root, text=evse_id, variable=StringVar, value=EVSE_dict[evse_id], command=lambda: test)
    #         print("?????????")
    #         print(evse_id)
    #         print(EVSE_dict[evse_id])
    #         print(rx)
    #         print(ry)
    #         rb.place(relx=rx, rely=ry)
    #         ry += 0.07

    def callbackFunc(self,event):
        print("select this one")
        # print(EVSE_dict[event])

    # show 当前的EVSEs   1. show 当前的evses， 2.加入evse combobox
    def show_current_evses(self, ws):
        ws.send("give me current evses")

        x0 = 0.5
        y0 = 0.1
        #  1. show evses：
        # for evse_id in EVSE_dict.keys():
        #     Label(root, text=evse_id).place(relx=x0, rely=y0, anchor=CENTER)
        #     x0 += 0.05

        #  2. add evses in combobox
        # evse_choosen = ttk.Combobox(root, width=27, textvariable=StringVar)
        # evse_choosen.place(relx = 0.5, rely = 0.2, anchor=CENTER)
        # # Adding combobox drop down list
        # evse_choosen['values'] = tuple(EVSE_dict.keys())
        # print(evse_choosen['values'])

        # evse_choosen.bind("<<ComboboxSelected>>", callbackFunc)
        # # evse_choosen.current()

    rx = 0.9
    ry = 0.1

    def select_one_evse(self):
        print("select this one")



async def main():

    async with websockets.connect(                   # 链接
        'ws://10.2.38.117:9000/***gui',                # 目的地址  +  序号
         # subprotocols=['ocpp1.6']
    ) as ws:

        # cp = ChargePoint('CP_m', ws)          #  实例化cp 包含名字和 ws 协议

    # ws = await websockets.connect('ws://10.2.38.117:9000/***GUI',subprotocols=['ocpp1.6'])

    # def _asyncio_thread(loop):
    #     loop.run_until_complete(fun1(ws))
    #
    # def do_tasks(loop):
    #     threading.Thread(target=_asyncio_thread, args=(loop,)).start()

        async def fun1(ws):
            await ws.send("give me current evses")

        # async def main():
        #     ws = await websockets.connect('ws://10.2.38.117:9000/***GUI',subprotocols=['ocpp1.6'])  # connect Object 必须是async， 不然没有send方法
        #     # async with websockets.connect('ws://10.2.38.117:9000/***GUI',subprotocols=['ocpp1.6']) as ws:
        #         # cp = ChargePoint('CP_m', ws)          #  实例化cp 包含名字和 ws 协议
        #
        #     msg = '{"jsonrpc": "2.0","method": "call","params": [0, "get_full_accounts", [["gxcdac"],false]],"id": 1}'
        #     await ws.send(msg)

                # response = await ws.recv()
                # print(response)
                # await asyncio.gather(
                #                      # cp.start(),        #必须先start 的才能发送其他
                #                      # cp.send_boot_notification(),
                #                      # cp.clear_cache_notification()
                #                      )   #先start ，在发送

        # await fun1(ws)

        root = Tk()
        root.title('Server')
        # 获取屏幕长、宽
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        # 设置窗口大小
        win_w = 1000
        win_h = 700
        # 获取屏幕中心位置，以使窗口位于屏幕中央
        center_x, center_y = compute_center(screen_w, screen_h, win_w, win_h)
        root.geometry('%dx%d+%d+%d' % (win_w, win_h, center_x, center_y))

        fun = SEND(root)

        # async def show_current_evses(ws):
        #     await ws.send("give me current evses")

        Button(root, text="show current EVSEs", command=lambda:fun1(ws)).place(relx=0.2, rely=0.1, anchor = CENTER)

    # label1 = Label(root, text = "Please select one EVSE :").place(relx = 0.2, rely = 0.2, anchor=CENTER)
    # label2 = Label(root, text = "Please select the command you want to send to the EVSE:").place(relx=0.4, rely=0.3, anchor = CENTER)
    # Button(root, text="Send remote start transaction", command=lambda: fun.test()).place(relx= 0.2, rely=0.4, anchor=CENTER)
    # Button(root, text="Send remote stop transaction", command=lambda: fun.test()).place(relx= 0.2, rely=0.5, anchor=CENTER)
    # Button(root, text="clear cache", command=lambda: fun.test()).place(relx= 0.2, rely=0.6, anchor=CENTER)



        async def run_tk(root, interval=0.05):
            '''
            Run a tkinter app in an asyncio event loop.
            '''
            try:
                while True:
                    root.update()
                    await asyncio.sleep(interval)
            except TclError as e:
                if "application has been destroyed" not in e.args[0]:
                    raise

        await run_tk(root)
        # mainloop()

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # main(loop)
    # main()
    asyncio.run(main())
    # try:
    #     # asyncio.run() is used when running this example with Python 3.7 and
    #     # higher.
    #     asyncio.run(main())
    # except AttributeError:
    #     # For Python 3.6 a bit more code is required to run the main() task on
    #     # an event loop.
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(main())
    #     loop.close()
