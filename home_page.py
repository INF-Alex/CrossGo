import tkinter as tk
from tkinter import simpledialog

def home(winner):
    choice = None
    def on_button_click():
        nonlocal choice
        result = simpledialog.askstring("开始游戏", "请选择：\n1:先手\n2:后手\n0:退出")
        if result is not None:
            choice = result
            window.destroy()

    def quit_application():
        exit()

    window = tk.Tk()
    window.title("井字棋游戏")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = 400
    window_height = 200

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    button = tk.Button(window, text="开始游戏", font=("微软雅黑", 16, "bold"), command=on_button_click, width=20, height=2)

    quit_button = tk.Button(window, text="退出", font=("微软雅黑", 16, "bold"), command=quit_application, width=20, height=2)

    button.grid(row=0, column=0, padx=5, pady=5)
    quit_button.grid(row=0, column=1, padx=5, pady=5)

    if winner:
        label = tk.Label(window, text=f"{winner}", font=("微软雅黑", 32, "bold"))
        label.grid(row=1, column=0, columnspan=2, pady=10)
    else:
        label = tk.Label(window, text="井字棋是一种简单而经典的策略游戏，据说在双方都采取最佳的行动的情况下，游戏最终会以平局结束。快来试试吧！", font=("微软雅黑", 16), wraplength=380)
        label.grid(row=1, column=0, columnspan=2, pady=10)
        

    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    window.mainloop()

    return choice

if __name__ == "__main__":
    home('')