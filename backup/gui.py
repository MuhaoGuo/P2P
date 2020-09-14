from tkinter import *
from tkinter import ttk
def compute_center(screen_w, screen_h, win_w, win_h):
    center_x = screen_w / 2 - win_w / 2
    center_y = screen_h / 2 - win_h / 2
    return center_x, center_y

# from central_system import *
import websockets
import asyncio
from datetime import datetime
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus, ClearCacheStatus, RemoteStartStopStatus
from ocpp.v16.enums import DataTransferStatus
from ocpp.v16 import call_result
from ocpp.v16 import call


class ChargePoint(cp):                     # 继承 chargePoint 类

    # def __init__(self, id, connection, response_timeout=30):
    #     """
    #     Args:
    #         charger_id (str): ID of the charger.
    #         connection: Connection to CP.
    #         response_timeout (int): When no response on a request is received
    #             within this interval, a asyncio.TimeoutError is raised.
    #     """
    #     self.id = id
    #
    #     self._response_timeout = response_timeout
    #
    #     self._connection = connection
    #
    #     self.route_map = create_route_map(self)
    #
    #     self._call_lock = asyncio.Lock()
    #
    #     self._response_queue = asyncio.Queue()
    #
    #     self._unique_id_generator = uuid.uuid4

    @on(Action.BootNotification)
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



    async def send_clear_cache_request(self):
        print("1.hello, clear cache request send to client")
        request = call.ClearCachePayload(

        )
        response = await self.call(request)
        # print(response)

        if response.status == ClearCacheStatus.accepted:
            print("3.we can Clear cache")
        elif response.status == ClearCacheStatus.rejected:
            print("client rejected to clear cache")

    async def send_remote_start_transaction(self):
        print("1.hello, remote start transaction request send to client")
        request = call.RemoteStartTransactionPayload(
            id_tag="transaction1",
            connector_id=1
        )
        response = await self.call(request)
        if response.status == RemoteStartStopStatus.accepted:
            print("3.we can remote start transaction")
        elif response.status == RemoteStartStopStatus.rejected:
            print("3.client rejected remote start transaction")

    async def send_remote_stop_transaction(self):
        print("1.hello, remote stop transaction request send to client")
        request = call.RemoteStopTransactionPayload(
            transaction_id=111
        )
        response = await self.call(request)
        if response.status == RemoteStartStopStatus.accepted:
            print("3.we can remote stop transaction")
        elif response.status == RemoteStartStopStatus.rejected:
            print("3.client rejected remote stop transaction")

    async def f1(self):
        await asyncio.gather(
                             self.start(),
                             self.send_remote_start_transaction()
        )

# def create_gui(cp):
    # root = Tk()
    # root.title('Server')
    # # 获取屏幕长、宽
    # screen_w = root.winfo_screenwidth()
    # screen_h = root.winfo_screenheight()
    # # 设置窗口大小
    # win_w = 600
    # win_h = 400
    # # 获取屏幕中心位置，以使窗口位于屏幕中央
    # center_x, center_y = compute_center(screen_w, screen_h, win_w, win_h)
    # root.geometry('%dx%d+%d+%d' % (win_w, win_h, center_x, center_y))
    #
    # Button(root, text="Start", command=lambda: f1(cp)).place(relx=0.2, rely=0.1, anchor=CENTER)
    # # Button(root, text="remote start", command=lambda: cp.send_remote_start_transaction).place(relx=0.2, rely=0.25, anchor=CENTER)
    # # Button(root, text="remote stop", command=lambda: cp.send_remote_stop_transaction).place(relx=0.2, rely=0.5, anchor=CENTER)
    # mainloop()


async def on_connect(websocket, path):            # 等待client 链接 传来的参数是charge point传来的
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    charge_point_id = path.strip('/')              #

    cp = ChargePoint(charge_point_id, websocket)   #
    # create_gui(cp)

    # 将每个cp添加到字典里
    EVSE_dict[charge_point_id] = cp
    # print(cp)
    # print(EVSE_dict)

    def which_function_1():
        fun2 = cp.send_remote_start_transaction()

    fun1 = cp.start()
    fun2 = cp.send_remote_start_transaction()

    await asyncio.gather(
                         fun1,
                         fun2,
                         # cp.send_remote_stop_transaction(),
    #                      # cp.send_clear_cache_request()
                         )

EVSE_dict ={}   # store all the EVSEs connected



async def main():

    server = await websockets.serve(
        on_connect,
        '10.2.38.117',
        9000,
        subprotocols=['ocpp1.6']
    )

# 创建服务器界面
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

    def test():
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

    def callbackFunc(event):
        print("select this one")
        print(EVSE_dict[event])

    # show 当前的EVSEs   1. show 当前的evses， 2.加入evse combobox
    def show_current_evses():
        x0 = 0.5
        y0 = 0.1
        #  1. show evses：
        for evse_id in EVSE_dict.keys():
            Label(root, text=evse_id).place(relx=x0, rely=y0, anchor=CENTER)
            x0 += 0.05

        #  2. add evses in combobox
        evse_choosen = ttk.Combobox(root, width=27, textvariable=StringVar)
        evse_choosen.place(relx = 0.5, rely = 0.2, anchor=CENTER)
        # Adding combobox drop down list
        evse_choosen['values'] = tuple(EVSE_dict.keys())
        print(evse_choosen['values'])

        evse_choosen.bind("<<ComboboxSelected>>", callbackFunc)
        # evse_choosen.current()

    rx = 0.9
    ry = 0.1

    def select_one_evse():
        print("select this one")

    Button(root, text="show current EVSEs", command=lambda: show_current_evses()).place(relx=0.2, rely=0.1, anchor = CENTER)
    label1 = Label(root, text = "Please select one EVSE :").place(relx = 0.2, rely = 0.2, anchor=CENTER)
    label2 = Label(root, text = "Please select the command you want to send to the EVSE:").place(relx=0.4, rely=0.3, anchor = CENTER)
    Button(root, text="Send remote start transaction", command=lambda: test()).place(relx= 0.2, rely=0.4, anchor=CENTER)
    Button(root, text="Send remote stop transaction", command=lambda: test()).place(relx= 0.2, rely=0.5, anchor=CENTER)
    Button(root, text="clear cache", command=lambda: test()).place(relx= 0.2, rely=0.6, anchor=CENTER)

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

    await server.wait_closed()



if __name__ == '__main__':
    # try:
    asyncio.run(main())
    # except AttributeError:
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(main())
    #     loop.close()