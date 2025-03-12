import os
import sys
import tkinter as tk
import re
from tkinter import messagebox, ttk, simpledialog
import pyodbc
import bcrypt
from cryptography.fernet import Fernet
import configparser


class UserManagement:
    _instance = None  # جلوگیری از باز شدن چندباره

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

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserManagement, cls).__new__(cls)
        return cls._instance

    def __init__(self, master):
        if hasattr(self, "initialized"):
            return

        self.initialized = True
        self.root = tk.Toplevel(master)  # فرم فرعی به جای `Tk()`
        self.root.title("مدیریت کاربران")
        self.root.configure(bg="#c2b9ad")

        # بسته شدن خودکار وقتی پنجره اصلی بسته شود
        master.protocol("WM_DELETE_WINDOW", self.on_main_close)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # ایجاد تب‌ها و UI
        self.setup_ui()

        # تنظیم اندازه مناسب پنجره
        self.auto_resize()

    def setup_ui(self):
        """ایجاد تب‌ها و UI"""
        tab_control = ttk.Notebook(self.root)
        self.tab_add_user = ttk.Frame(tab_control)
        self.tab_edit_user = ttk.Frame(tab_control)

        tab_control.add(self.tab_add_user, text="افزودن کاربر")
        tab_control.add(self.tab_edit_user, text="ویرایش کاربر")
        tab_control.pack(expand=1, fill="both")

        self.setup_add_user_tab()
        self.setup_edit_user_tab()

    def setup_add_user_tab(self):
        """ایجاد فرم افزودن کاربر جدید"""
        frame = tk.Frame(self.tab_add_user, bg="#c2b9ad", padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="نام کاربری (فقط انگلیسی):", font=("Helvetica", 12), bg="#c2b9ad").pack(anchor="e")
        self.username_entry = tk.Entry(frame, width=35, font=("Helvetica", 12), justify="right")
        self.username_entry.pack(pady=2)

        tk.Label(frame, text="رمز عبور (حداقل ۸ کاراکتر):", font=("Helvetica", 12), bg="#c2b9ad").pack(anchor="e")
        self.password_entry = tk.Entry(frame, width=35, font=("Helvetica", 12), show="*", justify="right")
        self.password_entry.pack(pady=2)

        self.role_var = tk.StringVar()
        self.role_var.set("user")
        tk.OptionMenu(frame, self.role_var, "admin", "user").pack(pady=2)

        ttk.Button(frame, text="افزودن کاربر", command=self.add_user).pack(pady=10)

    def setup_edit_user_tab(self):
        """ایجاد لیست کاربران برای ویرایش"""
        frame = tk.Frame(self.tab_edit_user, bg="#c2b9ad", padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="لیست کاربران:", font=("Helvetica", 12, "bold"), bg="#c2b9ad").pack(anchor="e")

        self.tree = ttk.Treeview(frame, columns=("نام کاربری", "نقش"), show="headings")
        self.tree.heading("نام کاربری", text="نام کاربری", anchor="e")
        self.tree.heading("نقش", text="نقش", anchor="e")
        self.tree.column("نام کاربری", width=150, anchor="e")
        self.tree.column("نقش", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True, pady=5)

        ttk.Button(frame, text="ویرایش رمز عبور", command=self.edit_user).pack(pady=5)

        self.load_users()  # 🔥 اضافه کردن اینجا تا کاربران هنگام باز شدن فرم بارگذاری شوند

    def auto_resize(self):
        """تنظیم اندازه پنجره متناسب با محتویاتش"""
        self.root.update_idletasks()  # به‌روزرسانی تا اندازه واقعی المان‌ها محاسبه شود
        width = self.root.winfo_reqwidth() + 20  # گرفتن عرض موردنیاز
        height = self.root.winfo_reqheight() + 20  # گرفتن ارتفاع موردنیاز

        # حداقل و حداکثر اندازه برای جلوگیری از بیش از حد کوچک یا بزرگ شدن
        min_width, min_height = 400, 250
        max_width, max_height = 600, 500

        width = max(min_width, min(width, max_width))
        height = max(min_height, min(height, max_height))

        # تنظیم اندازه و مرکز‌چین کردن پنجره
        self.root.geometry(f"{width}x{height}+{(self.root.winfo_screenwidth() - width) // 2}+{(self.root.winfo_screenheight() - height) // 2}")

    def on_close(self):
        """حذف نمونه و بستن فرم"""
        UserManagement._instance = None
        self.root.destroy()

    def on_main_close(self):
        """وقتی پنجره اصلی بسته شد، این فرم هم بسته شود"""
        self.on_close()


    def setup_edit_user_tab(self):
        """ایجاد لیست کاربران برای ویرایش"""
        frame = tk.Frame(self.tab_edit_user, bg="#c2b9ad", padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="لیست کاربران:", font=("Helvetica", 12, "bold"), bg="#c2b9ad").pack(anchor="e")

        self.tree = ttk.Treeview(frame, columns=("نام کاربری", "نقش"), show="headings")
        self.tree.heading("نام کاربری", text="نام کاربری", anchor="e")
        self.tree.heading("نقش", text="نقش", anchor="e")
        self.tree.column("نام کاربری", width=150, anchor="e")
        self.tree.column("نقش", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True, pady=5)

        ttk.Button(frame, text="ویرایش رمز عبور", command=self.get_connection_string()).pack(pady=5)

        self.load_users()  # 🔥 اضافه کردن اینجا تا کاربران هنگام باز شدن فرم بارگذاری شوند

    def load_users(self):
        conn = pyodbc.connect(self)
        cursor = conn.cursor()
        cursor.execute("SELECT Username FROM Users")
        users = cursor.fetchall()
        conn.close()

        for user in users:
            self.listbox.insert(tk.END, user[0])

            def edit_user(self):
                selected = self.listbox.curselection()
                if not selected:
                    messagebox.showerror("خطا", "یک کاربر را انتخاب کنید!")
                    return
                username = self.listbox.get(selected[0])

                new_password = tk.simpledialog.askstring("ویرایش رمز", f"رمز جدید برای {username}: ", show="*")
                if new_password:
                    conn = pyodbc.connect(self.get_connection_string())
                    cursor = conn.cursor()
                    new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("UPDATE Users SET PasswordHash = ? WHERE Username = ?", (new_hash, username))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("موفقیت", "رمز عبور تغییر کرد!")


