import tkinter as tk
import Sreboot
from Sreboot import RestartServer
import netcheck
from netcheck import NetST
# 建立主視窗和 Frame（把元件變成群組的容器）
window = tk.Tk()
top_frame = tk.Frame(window)
window.title("SOMS")
window.geometry('400x300')
# 將元件分為 top/bottom 兩群並加入主視窗
top_frame.pack()
bottom_frame = tk.Frame(window)
bottom_frame.pack(side=tk.BOTTOM)

# 建立事件處理函式（event handler），透過元件 command 參數存取
# def echo_hello():
#     print('hello world :)')

# 以下為 top 群組
left_button = tk.Button(top_frame, text='Red', fg='red')
# 讓系統自動擺放元件，預設為由上而下（靠左）
# left_button.pack(side=tk.LEFT)

# middle_button = tk.Button(top_frame, text='Green', fg='green')
# middle_button.pack(side=tk.LEFT)

right_button = tk.Button(top_frame, text='网络状态测试', fg='black',command=NetST)
right_button.pack(side=tk.LEFT)

# 以下為 bottom 群組
# bottom_button 綁定 echo_hello 事件處理，點擊該按鈕會印出 hello world :)
bottom_button = tk.Button(top_frame, text='重启服务器', fg='black', command=RestartServer)
# 讓系統自動擺放元件（靠下方）
bottom_button.pack(side=tk.LEFT)

# 運行主程式
window.mainloop()