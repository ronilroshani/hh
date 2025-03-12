import tkinter as tk
from tkinter import messagebox
import pyodbc
import bcrypt
import os
import sys
import tkinter as tk
from tkinter import messagebox

import configparser
import pyodbc
import bcrypt
from cryptography.fernet import Fernet

class AddUserForm:
    def get_connection_string(self):
        """
        این تابع `ConnectionString` را از فایل `config_encrypted.ini` خوانده و رمزگشایی می‌کند.
        """
        try:
            # گرفتن مسیر فولدری که اسکریپت در آن قرار دارد
            base_dir = os.path.dirname(os.path.abspath(__file__))

            # مسیرهای نسبی به فایل‌های تنظیمات
            key_path = os.path.join(base_dir, "secret.key")
            encrypted_config_path = os.path.join(base_dir, "config_encrypted.ini")

            # خواندن کلید رمزنگاری
            with open(key_path, "rb") as key_file:
                key = key_file.read()

            cipher_suite = Fernet(key)

            # خواندن و رمزگشایی فایل تنظیمات
            with open(encrypted_config_path, "rb") as file:
                encrypted_data = file.read()

            decrypted_data = cipher_suite.decrypt(encrypted_data)
            config_text = decrypted_data.decode()

            # پردازش رشته اتصال از داده‌های رمزگشایی‌شده
            config_parser = configparser.ConfigParser()
            config_parser.read_string(config_text)

            # برگرداندن `ConnectionString`
            return config_parser['Database']['ConnectionString']

        except FileNotFoundError as e:
            print(f"❌ فایل یافت نشد: {e}")
            sys.exit(1)
        except KeyError as e:
            print(f"❌ کلید تنظیمات یافت نشد: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ خطای غیرمنتظره: {e}")
            sys.exit(1)

    def __init__(self, root):
        self.root = root
        self.root.title("ایجاد کاربر جدید")
        self.root.geometry("300x250")
        self.root.configure(bg="#f4f4f4")

        # نام کاربری
        tk.Label(root, text="نام کاربری:", bg="#f4f4f4").pack(pady=5)
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack(pady=5)

        # رمز عبور
        tk.Label(root, text="رمز عبور:", bg="#f4f4f4").pack(pady=5)
        self.password_entry = tk.Entry(root, width=30, show="*")  # مخفی کردن رمز عبور
        self.password_entry.pack(pady=5)

        # انتخاب نقش کاربر (ادمین یا کاربر عادی)
        tk.Label(root, text="نقش کاربر:", bg="#f4f4f4").pack(pady=5)
        self.role_var = tk.StringVar()
        self.role_var.set("user")  # مقدار پیش‌فرض
        tk.OptionMenu(root, self.role_var, "admin", "user").pack(pady=5)

        # دکمه ثبت کاربر
        tk.Button(root, text="ثبت کاربر", command=self.add_user, bg="#4CAF50", fg="white").pack(pady=10)

    def add_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("خطا", "نام کاربری و رمز عبور را وارد کنید.")
            return

        # هش کردن رمز عبور (به صورت `bytes`)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = pyodbc.connect(self.get_connection_string())
            cursor = conn.cursor()

            # بررسی نوع داده `PasswordHash` در دیتابیس
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Users' AND COLUMN_NAME = 'PasswordHash' AND DATA_TYPE = 'varbinary')
                BEGIN
                    ALTER TABLE Users ALTER COLUMN PasswordHash VARBINARY(255);
                END
            """)

            # درج کاربر با `VARBINARY` برای رمز عبور
            cursor.execute("INSERT INTO Users (Username, PasswordHash, Role) VALUES (?, ?, ?)",
                           (username, password_hash, role))
            conn.commit()
            conn.close()
            messagebox.showinfo("موفقیت", "✅ کاربر با موفقیت اضافه شد!")
            self.root.destroy()

        except Exception as e:
            print(str(e))
            messagebox.showerror("❌ خطا در افزودن کاربر", str(e))


# اجرای فرم
if __name__ == "__main__":
    root = tk.Tk()
    AddUserForm(root)
    root.mainloop()
