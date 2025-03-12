import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import jdatetime
import calendar

class ShamsiCalendarApp:
    is_open = False  # متغیر کلاس‌سطحی برای بررسی وضعیت باز بودن پنجره
    def __init__(self, root, entry, row=None, column=None, pady=None, on_date_select_callback=None):
        if ShamsiCalendarApp.is_open:
            return
        ShamsiCalendarApp.is_open = True  # تنظیم وضعیت پنجره به باز
        self.root = root
        self.entry = entry
        self.on_date_select_callback = on_date_select_callback
        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("انتخاب تاریخ شمسی")
        self.calendar_window.attributes("-topmost", True)  # نمایش پنجره خطا در بالای همه پنجره‌ها
        self.days_frame = tk.Frame(self.calendar_window)
        self.days_frame.grid(row=2, column=0, pady=10)
        self.entry.grid(row=row, column=column, pady=pady)
        self.calendar_window.update_idletasks()
        x = (self.calendar_window.winfo_screenwidth() - 300) // 2
        y = (self.calendar_window.winfo_screenheight() - 150) // 2
        self.calendar_window.geometry(f"+{x}+{y}")

        today = jdatetime.datetime.now()
        self.year = today.year
        self.month = today.month
        self.selected_day = today.day
        month_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                       "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

        self.month_dropdown = ttk.Combobox(self.calendar_window, values=month_names, state="readonly")
        self.month_dropdown.current(self.month - 1)
        self.month_dropdown.grid(row=0, column=0, pady=10)

        self.year_entry = tk.Entry(self.calendar_window, width=5)
        self.year_entry.insert(0, str(self.year))
        self.year_entry.grid(row=1, column=0, pady=10)

        self.days_frame = tk.Frame(self.calendar_window)
        self.days_frame.grid(row=2, column=0, pady=10)
        self.calendar_window.protocol("WM_DELETE_WINDOW", self.on_close)
        # confirm_button = tk.Button(self.calendar_window, text="تایید", command=self.confirm_date)
        # confirm_button.grid(row=3, column=0, pady=10)

        self.show_days()

    def on_close(self):
        """وقتی پنجره بسته شد، وضعیت به بسته تغییر می‌کند."""
        ShamsiCalendarApp.is_open = False
        self.calendar_window.destroy()

    def select_date(self, day, month, year):
        print("og1")
        selected_date = f"{year}/{month}/{day}"
        if self.on_date_select_callback:
            self.on_date_select_callback(selected_date)  # ارسال تاریخ به متد کال‌بک
            print(selected_date)
#        self.on_close()

    def on_date_select(self, show_day):
        print("og2")
        selected_date = f"{self.year}/{self.month}/{self.selected_day}"
        if self.on_date_select_callback:
            self.on_date_select_callback(selected_date)  # ارسال تاریخ به متد کال‌بک
            print(selected_date)

        if self.entry is not None:
            self.entry.delete(0, 'end')
            self.entry.insert(0, show_day)
        else:
            print("Entry is None")

    def to_persian_number(self, number):
        persian_digits = "۰۱۲۳۴۵۶۷۸۹"
        return ''.join(persian_digits[int(digit)] for digit in str(number))

    def confirm_date(self):

        print("og3")
        """زمانی که کاربر تاریخ را تأیید کرد."""
        selected_date = f"{self.year}/{self.month}/{self.selected_day}"
        print("selected_date", selected_date)
        if self.on_date_select_callback:
            self.on_date_select_callback(selected_date)  # ارسال تاریخ انتخاب‌شده به تابع فراخوانی‌کننده
        self.on_close()

    def show_days(self):
        month_index = self.month_dropdown.current() + 1
        year_value = self.year_entry.get()
        if not year_value.isdigit() or int(year_value) < 1:
            messagebox.showerror("خطا", "لطفاً یک سال معتبر وارد کنید.")
            return
        year_value = int(year_value)
        days_in_month = calendar.monthrange(year_value, month_index)[1]
        for day in range(1, days_in_month + 1):
            day_button = tk.Button(self.days_frame, text=self.to_persian_number(day),
                                   command=lambda d=day: self.select_date(d, month_index, year_value),
                                   font=("Vazir", 11), bg="#c2b9ad", fg="#1b1a17", width=4)
            day_button.grid(row=(day - 1) // 7, column=(day - 1) % 7, padx=2, pady=2)

        for day in range(1, days_in_month + 1):
            confirm_button = tk.Button(self.days_frame, text=self.to_persian_number(day),
                                   command=lambda d=day: self.select_date(d, month_index, year_value),
                                   font=("Vazir", 11), bg="#c2b9ad", fg="#1b1a17", width=4)
            confirm_button.grid(row=(day - 1) // 7, column=(day - 1) % 7, padx=2, pady=2)


    def validate_persian_date(self, date_str):
        """Validate if the date is in Persian format YYYY/MM/DD"""
        parts = date_str.split("/")
        if len(parts) == 3:
            try:
                year, month, day = map(int, parts)
                # Check if the year, month, and day are valid
                jdatetime.datetime(year, month, day)
                return True
            except ValueError:
                return False
        return False

    def on_submit(self):
        date_value = self.entry.get()
        if not self.validate_persian_date(date_value):
            messagebox.showerror("خطا", "لطفاً تاریخ شمسی معتبر وارد کنید.")
        else:
            print("تاریخ وارد شده معتبر است:", date_value)
            # ادامه عملیات ذخیره یا بروزرسانی اطلاعات
