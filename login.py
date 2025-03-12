import os
import socket
import sys
import tkinter as tk
from tkinter import messagebox
import configparser
import pyodbc
import bcrypt
from cryptography.fernet import Fernet
import DatabaseConnection
import EmployeeApp
from EmployeeApp import EmployeeApp


class LoginWindow:
    def get_connection_string(self):
        """خواندن و رمزگشایی `ConnectionString` از فایل تنظیمات"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))

            key_path = os.path.join(base_dir, "secret.key")
            encrypted_config_path = os.path.join(base_dir, "config_encrypted.ini")

            with open(key_path, "rb") as key_file:
                key = key_file.read()

            cipher_suite = Fernet(key)

            with open(encrypted_config_path, "rb") as file:
                encrypted_data = file.read()

            decrypted_data = cipher_suite.decrypt(encrypted_data)
            config_text = decrypted_data.decode()

            config_parser = configparser.ConfigParser()
            config_parser.read_string(config_text)

            return config_parser['Database']['ConnectionString']

        except Exception as e:
            messagebox.showerror("خطا", f"مشکلی در بارگیری تنظیمات رخ داد: {e}")
            sys.exit(1)

    def __init__(self, root):
        self.root = root
        self.root.title("ورود به سامانه")
        self.root.geometry("400x250")  # اندازه ثابت پنجره
        self.root.configure(bg="#c2b9ad")  # رنگ پس‌زمینه

        # **وسط‌چین کردن پنجره**
        self.root.update_idletasks()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        x = (w - 400) // 2
        y = (h - 250) // 2
        self.root.geometry(f"400x250+{x}+{y}")  # تنظیم موقعیت در وسط صفحه

        # **قاب اصلی برای راست‌چین کردن محتوا**
        frame = tk.Frame(root, bg="#c2b9ad")
        frame.pack(expand=True)

        tk.Label(frame, text="نام کاربری:", font=("Helvetica", 12), bg="#c2b9ad").grid(row=0, column=1, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(frame, width=25, font=("Helvetica", 12))
        self.username_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="رمز عبور:", font=("Helvetica", 12), bg="#c2b9ad").grid(row=1, column=1, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(frame, show="*", width=25, font=("Helvetica", 12))
        self.password_entry.grid(row=1, column=0, padx=10, pady=5, sticky="w")


        # دکمه ورود
        login_button = tk.Button(frame, text="ورود", command=self.login, font=("Helvetica", 12), bg="#6d6875",fg="white")
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # اضافه کردن رویداد فشردن Enter در هر جای فرم
        self.root.bind("<Return>", lambda event: self.login())

        # اضافه کردن رویداد دابل کلیک روی دکمه ورود
        login_button.bind("<Double-Button-1>", lambda event: self.login())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("خطا", "نام کاربری و رمز عبور را وارد کنید.")
            return

        try:
            conn = pyodbc.connect(self.get_connection_string())
            cursor = conn.cursor()
            cursor.execute("SELECT PasswordHash FROM Users WHERE Username = ?", (username,))
            user = cursor.fetchone()
            conn.close()

            if user:
                stored_hash = user[0]
                if isinstance(stored_hash, memoryview):
                    stored_hash = stored_hash.tobytes()  # تبدیل `memoryview` به `bytes`

                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    self.open_main_app()
                else:
                    messagebox.showerror("خطا", "رمز عبور اشتباه است.")
            else:
                messagebox.showerror("خطا", "نام کاربری یافت نشد.")

        except Exception as e:
            messagebox.showerror("خطای دیتابیس", f"مشکلی در ارتباط با دیتابیس رخ داد: {e}")

    def open_main_app(self):
        """باز کردن برنامه اصلی فقط اگر ورود موفق باشد"""
        self.root.destroy()
        db_connection = DatabaseConnection.DatabaseConnection()

        try:
            # اجرای برنامه
            import EmployeeApp
            employee_app = EmployeeApp.EmployeeApp(db_connection)
        #finally:
            # آزاد کردن پورت در پایان
        #    instance.close()
        except:
            print("ffff")
            db_connection.connection.close()


        # root = tk.Tk()
        # app = EmployeeApp(root)
        # root.mainloop()



