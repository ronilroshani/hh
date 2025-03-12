#pyinstaller --onefile --noconsole F:\app\HumanResource\main.py
import configparser
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import logging
import pyodbc
from ttkthemes import ThemedTk
from DatabaseManager import DatabaseManager
from FormManager import FormManager
import socket
import sys
from tkinter import PhotoImage
#from test import EmployeeDetail  # Import the EmployeeDetail class
import os
from cryptography.fernet import Fernet
import configparser
import login

# Define colors
FIRST_COLOR = "#90f6d7"
SECOND_COLOR = "#35bcbf"
THIRD_COLOR = "#41506b"
FOURTH_COLOR = "#263849"

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
import pyodbc
import bcrypt
from getpass import getpass

class DatabaseConnection:
    # تابع برای هش کردن رمز عبور
    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed
    def add_admin(self):
        # اتصال به دیتابیس
        conn = pyodbc.connect(self.get_connection_string())
        cursor = conn.cursor()

        # دریافت نام کاربری و رمز از کاربر
        username = input("نام کاربری جدید: ")
        password = getpass("رمز عبور: ")  # برای مخفی کردن ورودی رمز عبور

        # هش کردن رمز عبور
        password_hash = self.hash_password(password)

        # افزودن کاربر به دیتابیس
        try:
            cursor.execute("INSERT INTO Users (Username, PasswordHash, Role) VALUES (?, ?, ?)",
                           (username, password_hash, 'admin'))
            conn.commit()
            print("✅ کاربر با موفقیت اضافه شد!")
        except Exception as e:
            print(f"❌ خطا در افزودن کاربر: {e}")

        conn.close()

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

    def __init__(self):
        self.connection = pyodbc.connect(self.get_connection_string())
        #self.add_admin()
    def fetch_data(self, query, params=()):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
            return rows
        except Exception as e:
            raise e
