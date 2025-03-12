import tkinter as tk
from tkinter import ttk


class MillitaryFile:
    def __init__(self, parent, db_manager, national_code):
        self.parent = parent
        self.db_manager = db_manager
        self.national_code = national_code

        self.window = tk.Toplevel(self.parent)
        self.window.title("پرونده نحصیلات نظامی")
        self.window.geometry("900x600")
        self.window.config(bg="#c2b9ad")
        self.window.attributes("-topmost", True)

        # قاب اصلی در پنجره جدید
        self.main_frame = tk.Frame(self.window, bg='#c2b9ad')
        self.main_frame.pack(fill="both", expand=True)

        # ایجاد تب‌ها
        self.tab_control = ttk.Notebook(self.main_frame)
        style = ttk.Style()
        style.configure("TFrame", background="#c2b9ad")
        # تب نحصیلات نظامی
        self.millitary_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.millitary_tab, text="نحصیلات نظامی")

        # نمایش تب‌ها
        self.tab_control.pack(expand=1, fill="both")
        self.center_window()

        # ایجاد فرم برای نحصیلات نظامی
        self.create_millitary_form()

        self.window.lift()
        self.window.grab_set()

        self.load()

    def load(self):
        try:
            millitary_data = self.db_manager.get_millitary_by_national_code(self.national_code)
            self.fill(millitary_data=millitary_data)
        except Exception as e:
            print(f"\u062E\u0637\u0627: {e}")

    def fill(self, millitary_data=None):
        # پر کردن فرم نحصیلات نظامی
        if millitary_data:
            for record in millitary_data:
                for field, value in record.items():
                    if field in self.millitary_entries:
                        self.millitary_entries[field].delete("1.0", "end")
                        self.millitary_entries[field].insert("1.0", value)

    def create_millitary_form(self):
        labels = [
            "عنوان دوره نظامی", "محل دوره", "تاریخ شروع دوره", "تاریخ پایان دوره",
            "مدت دوره", "محدودیت", "مدرک - سند"
        ]
        field_names = [
            "MillitaryTitle", "MillitaryLocation", "MillitaryStartDate", "MillitaryEndDate",
            "MillitaryDuration", "MillitaryMahdoodiyat", "Document"
        ]


        self.millitary_entries = {}
        for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
            # ایجاد لیبل
            label = tk.Label(self.millitary_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17', anchor="e",
                             width=20)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="e")

            # ایجاد فریم برای فیلد متنی و اسکرول بار
            frame = tk.Frame(self.millitary_tab, bg='#c2b9ad')
            entry = tk.Text(frame, width=5, height=40, wrap='word', bg='#ffffff', fg='#1b1a17')
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=entry.yview)
            entry.config(yscrollcommand=scrollbar.set)

            # اضافه کردن فیلد متنی و اسکرول بار به فریم
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            # ذخیره فیلدها در دیکشنری
            self.millitary_entries[field_name] = entry

        # تنظیم کشش یکنواخت برای ستون‌ها و ردیف‌ها
        for col in range(2):  # ستون‌های 0 و 1
            self.millitary_tab.grid_columnconfigure(col, weight=1)
        for row in range(len(field_names)):  # برای هر ردیف
            self.millitary_tab.grid_rowconfigure(row + 5, weight=1)  # شروع از ردیف 5 برای لیبل‌ها

        # دکمه ذخیره
        save_button = tk.Button(self.millitary_tab, text="ذخیره", command=self.save_millitary)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def center_window(self):
        window_width, window_height = 1450, 800
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.window.attributes('-topmost', True)

    def save_millitary(self):
        # گرفتن داده‌ها از فرم نحصیلات نظامی
        millitary_data = {field: entry.get("1.0", "end-1c") for field, entry in self.millitary_entries.items()}
        self.db_manager.save_millitary(self.national_code, millitary_data)
