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
import user_management

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

class EmployeeApp:
    _instance = None  # جلوگیری از باز شدن چندباره‌ی فرم

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EmployeeApp, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_connection):
        if hasattr(self, "initialized"):
            return  # جلوگیری از مقداردهی چندباره

        self.connection = pyodbc.connect(self.get_connection_string())

        self.root = ThemedTk(theme="arc")  # ایجاد پنجره اصلی
        self.root.title("کارمندان")  # تنظیم عنوان پنجره
        self.root.configure(bg='#c2b9ad')
        # ایجاد نوار ابزار در بالای صفحه
        self.toolbar = tk.Frame(self.root, bg="#9b9184")  # رنگ پس‌زمینه
        self.toolbar.pack(fill="x", padx=5, pady=5)  # پر کردن عرض صفحه

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_dir, "photo", "resources-icon-png.ico")
            self.root.iconbitmap(icon_path)

        except Exception as e:
            print(f"خطای بارگذاری آیکون فرم کارمندان: {e}")

        self.db_connection = db_connection
        self.records_per_page = tk.IntVar(value=10)
        self.current_page = tk.IntVar(value=1)
        self.total_records = 0

        # تنظیمات سبک‌ها
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), padding=10, background='#c2b9ad', foreground='#1b1a17')
        style.configure('TLabel', font=('Helvetica', 12), background='#c2b9ad', foreground='#1b1a17', padding=10)
        style.configure('TEntry', font=('Helvetica', 12), background='#c2b9ad', foreground='#1b1a17', padding=10)
        style.configure('TCombobox', font=('Helvetica', 12))
        style.configure('TLabelframe', font=('Helvetica', 12))

        # تنظیم فرم فیلتر
        self.filter_frame = FilterForm(self.root, self.get_column_names(), self.apply_filters)
        self.filter_frame.configure(bg='#c2b9ad')
        self.filter_frame.pack(fill="x", padx=20, pady=10)

        # تنظیم جدول با اسکرول‌بار
        self.table_frame = EmployeeTable(self.root, self.get_column_names(), self.on_row_click)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)


        # تنظیم گزینه‌های صفحه‌بندی
        options_frame = tk.Frame(self.root, bg="#c2b9ad")
        options_frame.pack(pady=10, fill="x")
        tk.Label(options_frame, text="تعداد سطر در هر صفحه :", font=('Helvetica', 12), bg="#c2b9ad").pack(
            side="left", padx=10)
        records_combo = ttk.Combobox(options_frame, textvariable=self.records_per_page, values=[10, 25, 50, 100],
                                     width=5)
        records_combo.pack(side="left", padx=10)
        records_combo.bind("<<ComboboxSelected>>", self.on_records_per_page_change)

        # نمایش اطلاعات صفحه
        self.page_info = tk.Label(options_frame, text="", font=('Helvetica', 12), bg="#c2b9ad")
        self.page_info.pack(side="left", padx=10)

        # دکمه‌های ناوبری
        self.prev_button = tk.Button(options_frame, text=" قبلی ", command=self.previous_page, bg='#9b9184',
                                     fg='#1b1a17', width=10)
        self.prev_button.pack(side="left", padx=5)
        self.next_button = tk.Button(options_frame, text=" بعدی ", command=self.next_page, bg='#9b9184',
                                     fg='#1b1a17', width=10)
        self.next_button.pack(side="left", padx=5)

        self.manage_users_button = tk.Button(self.toolbar, text="مدیریت کاربران", command=self.open_user_management,
                                             bg='#6d6875', fg='white')
        self.manage_users_button.pack(side="left", padx=5, pady=2)

        self.create_new_user = tk.Button(self.toolbar, text="ایجاد کاربر جدید", command=self.create_new_users,
                                         bg='#6d6875', fg='white')
        self.create_new_user.pack(side="left", padx=5, pady=2)


        # دکمه تازه‌سازی
        # self.create_new_user = tk.Button(options_frame, text=" ایجاد کاربر جدید ", command=self.create_new_users, bg='#9b9184',
        #                              fg='#1b1a17', width=10)
        # self.create_new_user.pack(side="right",padx=20)

        self.refresh_button = tk.Button(self.root, text="بروزرسانی", command=self.display_data, bg='#9b9184',
                                        fg='#1b1a17', width=10)
        self.refresh_button.pack(pady=20)

        # تنظیم منو
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        # منو زبان
        #language_menu = tk.Menu(menu_bar, tearoff=0)
        #menu_bar.add_cascade(label="Language", menu=language_menu)
        #language_menu.add_command(label="English", command=lambda: self.change_language('en'))
        #language_menu.add_command(label="فارسی", command=lambda: self.change_language('fa'))

        # نمایش داده‌ها
        self.display_data()

        tk.Label(self.root, text=f" تعداد کل کارمندان  {self.total_records}", font=('Helvetica', 12),
                 bg="#c2b9ad").pack(side="left", padx=10)
        self.is_form_manager_open = False
        self.root.mainloop()  # اجرای حلقه اصلی پنجره
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

    def open_user_management(self):
        #user_window = tk.Toplevel(self.root)
        user_management.UserManagement(self.root)

    def on_records_per_page_change(self, event):
        self.display_data()

    def get_column_names(self):

        return [
             "کد ملی", "نام", "نام خانوادگی", "تاریخ تولد",
             "جنسیت",
             "تاهل", "موبایل"
        ]

    def display_data(self, filtered_rows=None):
        query = ('SELECT COUNT(*) FROM [PersonalInfo]')  # تغییر جهت محاسبه تعداد رکوردها
        try:
            self.total_records = int(self.db_connection.fetch_data(query)[0][0])  # تبدیل به عدد صحیح
        except Exception as e:
            self.handle_error("Error", "Error fetching total record count", str(e))
            return

        start_index = (self.current_page.get() - 1) * self.records_per_page.get()
        end_index = start_index + self.records_per_page.get()

        query = f'''
        SELECT NationalCode, FirstName, LastName, BirthDate, Gender, MaritalStatus, Mobile  FROM [PersonalInfo] p
                        LEFT JOIN [Gender] g ON p.GenderID = g.GenderID
                        LEFT JOIN [MaritalStatus] m ON p.MaritalStatusID = m.MaritalStatusID WHERE 1=1 
        ORDER BY NationalCode
        OFFSET {start_index} ROWS FETCH NEXT {self.records_per_page.get()} ROWS ONLY
        '''

        if filtered_rows is None:
            try:
                rows = self.db_connection.fetch_data(query)
            except Exception as e:
                self.handle_error("Error", "Error executing query", str(e))
                return
        else:
            rows = filtered_rows

        # پاک کردن داده‌ها از هرگونه "دابل کوتیشن"
        cleaned_rows = []
        for row in rows:
            cleaned_row = []
            for cell in row:
                # اگر داده عددی است، تبدیل به عدد صحیح یا اعشاری
                if isinstance(cell, (int, float)):
                    cleaned_row.append(cell)
                elif isinstance(cell, str):
                    cleaned_row.append(cell.replace('"', ''))  # حذف دابل کوتیشن‌ها از رشته‌ها
                else:
                    cleaned_row.append(str(cell))  # تبدیل داده‌ها به رشته
            cleaned_rows.append(tuple(cleaned_row))

        self.table_frame.update_data(cleaned_rows)
        self.update_page_info()
        self.update_navigation_buttons()


    def apply_filters(self, filter_conditions, filter_values):
        # Dictionary to map Persian column names to actual database column names
        print("filter")
        column_mapping = {
            "کد ملی": "NationalCode",
            "نام": "FirstName       ",
            "نام خانوادگی": "LastName",
            "تاریخ تولد": "BirthDate",
            "جنسیت": "GenderID",
            "تاهل": "MaritalStatusID",
            "موبایل": "Mobile"
        }

        base_query = ''' SELECT NationalCode, FirstName, LastName, BirthDate, GenderID, MaritalStatusID, Mobile FROM [PersonalInfo] WHERE 1=1 '''

        # Apply column name mapping
        mapped_conditions = []
        for condition in filter_conditions:
            column_name, filter_value = condition.split(" LIKE ?")
            if column_name in column_mapping:
                mapped_column = column_mapping[column_name]
                mapped_conditions.append(f"{mapped_column} LIKE ?")

        if mapped_conditions:
            query = base_query + " AND " + " AND ".join(mapped_conditions)
        else:
            query = base_query

        try:
            filtered_rows = self.db_connection.fetch_data(query, tuple(filter_values))
            self.display_data(filtered_rows)
        except Exception as e:
            self.handle_error("Error", "Error applying filters", str(e))

    def previous_page(self):
        if self.current_page.get() > 1:
            self.current_page.set(self.current_page.get() - 1)
            self.display_data()

    def next_page(self):
        if (self.current_page.get() * self.records_per_page.get()) < self.total_records:
            self.current_page.set(self.current_page.get() + 1)
            self.display_data()

    def update_page_info(self):
        total_pages = (self.total_records + self.records_per_page.get() - 1) // self.records_per_page.get()
        self.page_info.config(text=f"صفحه  {self.current_page.get()} از  {total_pages}")

    def update_navigation_buttons(self):
        total_pages = (self.total_records + self.records_per_page.get() - 1) // self.records_per_page.get()
        self.prev_button.config(state="normal" if self.current_page.get() > 1 else "disabled")
        self.next_button.config(state="normal" if self.current_page.get() < total_pages else "disabled")

    def handle_error(self, title, message, detail):
        logging.error(f"{message}: {detail}")
        messagebox.showerror(title, f"{message}\n\n{detail}")

    def on_row_click(self, event):
        try:
            if self.is_form_manager_open:
                return
            selected_item = self.table_frame.tree.focus()
            selected_data = self.table_frame.tree.item(selected_item)['values']
            emp_id = selected_data[0]  # اولین مقدار از لیست انتخاب شده
            if isinstance(emp_id, tuple):
                print("Original emp_id 1 :", emp_id)
                emp_id = emp_id[0]  # استخراج اولین مقدار از تاپل
            # حذف کاراکترهای اضافی و تبدیل به عدد صحیح
            emp_id = int(''.join(filter(str.isdigit, str(emp_id))))
            self.db_manager = DatabaseManager(self.get_connection_string())
            self.form_manager = FormManager(self.root, self.db_manager)
            self.is_form_manager_open = True  # نشان دادن باز بودن فرم
            # اتصال به رویداد بسته شدن فرم
            self.form_manager.set_close_callback(self.on_form_manager_close)
            self.form_manager.on_table_row_click(event, [str(value) if isinstance(value, int) else value for value in selected_data])
            self.form_manager.on_row_select(event, [str(value) if isinstance(value, int) else value for value in  selected_data])
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a valid row.")
        except ValueError as ve:
            messagebox.showerror("Conversion Error", f"Failed to convert Employee ID to integer: {ve}")
            print("ValueError:", ve)
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
            print("Unexpected Error:", e)

    def create_new_users(self):
        try:
            if self.is_form_manager_open:
                return
            self.db_manager = DatabaseManager(self.get_connection_string())
            self.form_manager = FormManager(self.root, self.db_manager)
            self.is_form_manager_open = True  # نشان دادن باز بودن فرم
            self.form_manager.set_close_callback(self.on_form_manager_close)
            self.form_manager.create_details_form(" ")
        except Exception as e:
            messagebox.showerror("خطا در باز کردن پنجره جزییات: ", f"خطا در باز کردن پنجره جزییات رخ داد: {e}")
            print("Unexpected Error:", e)

    def on_form_manager_close(self):
        self.is_form_manager_open = False

    def change_language(self, language):
        messagebox.showinfo("Language", f"Language changed to {language}")

class EmployeeTable(tk.Frame):
    def __init__(self, parent, columns, on_row_click):

        super().__init__(parent)
        # ایجاد اسکرول‌بار عمودی
        self.scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        # تنظیم جدول
        self.tree = ttk.Treeview(self, columns=columns, show="headings", yscrollcommand=self.scrollbar.set)
        self.tree.pack(fill="both", expand=True)
        # اتصال اسکرول‌بار به جدول
        self.scrollbar.config(command=self.tree.yview)



        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.bind("<Double-1>", on_row_click)

    def update_data(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

class FilterForm(tk.Frame):
    def __init__(self, parent, column_names, apply_filter_callback):
        super().__init__(parent)
        self.column_names = column_names
        self.apply_filter_callback = apply_filter_callback
        self.filter_conditions = []
        self.filter_values = []

        self.filters = []

        # تنظیم سبک‌های ویجت‌ها با رنگ قرمز
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), padding=10, background='#9b9184',
                        foreground='#ffffff')  # رنگ قرمز برای دکمه‌ها
        style.configure('TLabel', font=('Helvetica', 12), background='#9b9184', foreground='#1b1a17',
                        padding=10)  # رنگ قرمز برای برچسب‌ها
        style.configure('TEntry', font=('Helvetica', 12), background='#9b9184', foreground='#1b1a17', padding=10)
        style.configure('TCombobox', font=('Helvetica', 12))
        style.configure('TLabelframe', font=('Helvetica', 12))

        for i, column in enumerate(column_names):
            tk.Label(self, text=column, bg="#c2b9ad", fg="#1b1a17").grid(row=0, column=i, padx=5,
                                                                         pady=5)  # رنگ قرمز برای برچسب‌ها
            entry = ttk.Entry(self)
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.filters.append(entry)

        style = ttk.Style()
        style.configure('Custom.TButton', font=('Helvetica', 12), padding=10, bg='red', background='#c2b9ad',
                        foreground='#1b1a17')

        ttk.Button(self, text="اعمال فیلتر", command=self.apply_filters, width=10, style='Custom.TButton').grid(row=2,
                                                                                                                column=0,
                                                                                                                columnspan=len(
                                                                                                                    column_names),
                                                                                                                pady=10)

    def apply_filters(self):
        self.filter_conditions.clear()
        self.filter_values.clear()

        for i, entry in enumerate(self.filters):
            if entry.get():
                self.filter_conditions.append(f"{self.column_names[i]} LIKE ?")
                self.filter_values.append(f"%{entry.get()}%")

        self.apply_filter_callback(self.filter_conditions, self.filter_values)
