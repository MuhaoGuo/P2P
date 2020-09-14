
# WS server example

import asyncio
import websockets
from tkinter import *

def compute_center(screen_w, screen_h, win_w, win_h):
    center_x = screen_w / 2 - win_w / 2
    center_y = screen_h / 2 - win_h / 2
    return center_x, center_y



# async def send():
#     name = input("what is your name")
#     greeting = f"Hello {name}!"
#     await websocket.send(greeting)
#     print(f"> {greeting}")
#
# class ChargePoint:
#     async def send(self):
#         name = input("what is your name")
#         greeting = f"Hello {name}!"
#         await websocket.send(greeting)

async def hello(websocket, path):

    name = input("what is your name")
    greeting = f"Hello {name}!"
    await websocket.send(greeting)
    print(f"> {greeting}")



async def main():

    server = await websockets.serve(hello, "localhost", 8765)

    await server.wait_closed()



# asyncio.run(main())

import threading
def on_main():
    t = threading.Thread(target = asyncio.run(main()))
    t.start()


# async def gui():
root = Tk()
root.title('Server')
# 获取屏幕长、宽
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
# 设置窗口大小
win_w = 600
win_h = 400
# 获取屏幕中心位置，以使窗口位于屏幕中央
center_x, center_y = compute_center(screen_w, screen_h, win_w, win_h)
root.geometry('%dx%d+%d+%d' % (win_w, win_h, center_x, center_y))

Button(root, text="Start", command=lambda: on_main).place(relx=0.2, rely=0.1, anchor=CENTER)
# Button(root, text="remote start", command=lambda: cp.send_remote_start_transaction).place(relx=0.2, rely=0.25, anchor=CENTER)
# Button(root, text="remote stop", command=lambda: cp.send_remote_stop_transaction).place(relx=0.2, rely=0.5, anchor=CENTER)


# asyncio.run(gui())
mainloop()