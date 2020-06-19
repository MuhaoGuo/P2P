from tkinter import *
def compute_center(screen_w, screen_h, win_w, win_h):
    center_x = screen_w / 2 - win_w / 2
    center_y = screen_h / 2 - win_h / 2
    return center_x, center_y

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

    cp = ChargePoint(root)
    Button(root, text="选择模板文件夹", command=lambda: cp.send_clear_cache_request()).place(relx=0.2, rely=0.25,  anchor=CENTER)
    mainloop()