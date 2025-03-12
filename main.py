import tkinter as tk
import logging
import login
FIRST_COLOR = "#90f6d7"
SECOND_COLOR = "#35bcbf"
THIRD_COLOR = "#41506b"
FOURTH_COLOR = "#263849"
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


# کد اصلی برنامه
if __name__ == "__main__":

    try:
        root = tk.Tk()
        login = login.LoginWindow(root)
        root.mainloop()
    finally:
        # آزاد کردن پورت در پایان
        print("finish")



