import tkinter as tk
from tkinter import ttk


class SeniorityForm:
    def __init__(self, parent, db_manager, national_code):
        self.parent = parent
        self.db_manager = db_manager
        self.national_code = national_code

        self.window = tk.Toplevel(self.parent)
        self.window.title("سنوات مثبت و منفی")
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
        # تب سنوات مثبت
        self.positive_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.positive_tab, text="سنوات مثبت")

        # تب سنوات منفی
        self.negative_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.negative_tab, text="سنوات منفی")
        # نمایش تب‌ها
        self.tab_control.pack(expand=1, fill="both")
        self.center_window()
        # ایجاد فرم‌ها
        self.create_positive_form()
        self.create_negative_form()
        self.window.lift()
        self.window.grab_set()

        self.load()


    def load(self):
        try:
            positive_seniority_data = self.db_manager.get_positive_seniority_by_national_code(self.national_code)
            negative_seniority_data = self.db_manager.get_negative_seniority_by_national_code(self.national_code)
            self.fill(positive_seniority_data=positive_seniority_data, negative_seniority_data=negative_seniority_data)
        except Exception as e:
            print(f"\u062E\u0637\u0627: {e}")

    def fill(self, positive_seniority_data=None, negative_seniority_data=None):
        # پر کردن فرم سنوات مثبت
        if positive_seniority_data:
            for record in positive_seniority_data:
                for field, value in record.items():
                    if field in self.positive_entries:
                        self.positive_entries[field].delete("1.0", "end")
                        self.positive_entries[field].insert("1.0", value)

        # پر کردن فرم سنوات منفی
        if negative_seniority_data:
            for record in negative_seniority_data:
                for field, value in record.items():
                    if field in self.negative_entries:
                        self.negative_entries[field].delete("1.0", "end")
                        self.negative_entries[field].insert("1.0", value)

    def create_positive_form(self):
        labels = [
            "lm;","محل خدمت:", "تاریخ شروع:", "تاریخ پایان:",
            "جمع مدت خدمت:", "درجه زمان خدمت:", "وضعیت استخدام:",
            "مدت انقطاع از خدمت:", "نوع انفصال:", "مدرک:"
        ]
        field_names = [
            "NationalCode", "ServiceLocation", "StartDate", "EndDate",
            "TotalServiceDuration", "RankAtTimeOfService", "EmploymentStatus",
            "ServiceBreakDuration", "TerminationType", "Document"
        ]

        self.positive_entries = {}
        for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
            # ایجاد لیبل
            label = tk.Label(self.positive_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17', anchor="e",
                             width=20)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="e")

            # ایجاد فریم برای فیلد متنی و اسکرول بار

            frame = tk.Frame(self.positive_tab, bg='#c2b9ad')
            entry = tk.Text(frame, width=5, height=40, wrap='word', bg='#ffffff', fg='#1b1a17')
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=entry.yview)
            entry.config(yscrollcommand=scrollbar.set)

            # اضافه کردن فیلد متنی و اسکرول بار به فریم
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            # ذخیره فیلدها در دیکشنری
            self.positive_entries[field_name] = entry

        # تنظیم کشش یکنواخت برای ستون‌ها و ردیف‌ها
        for col in range(2):  # ستون‌های 0 و 1
            self.positive_tab.grid_columnconfigure(col, weight=1)
        for row in range(len(field_names)):  # برای هر ردیف
            self.positive_tab.grid_rowconfigure(row + 5, weight=1)  # شروع از ردیف 5 برای لیبل‌ها

    def create_negative_form(self):
        labels = [
            "ddd","مدرک:", "ملاحظات:","تاریخ شروع:", "تعداد روز:", "تاریخ خاتمه:",
            "نوع:"
        ]
        field_names = [
            "NationalCode","Notes", "StartDate", "DurationDays", "EndDate",
            "Typese", "Document"
        ]

        self.negative_entries = {}
        for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
            # ایجاد لیبل
            label = tk.Label(self.negative_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17', anchor="e",
                             width=20)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="e")

            # ایجاد فریم برای فیلد متنی و اسکرول بار
            frame = tk.Frame(self.negative_tab, bg='#c2b9ad')
            entry = tk.Text(frame, width=5, height=40, wrap='word', bg='#ffffff', fg='#1b1a17')
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=entry.yview)
            entry.config(yscrollcommand=scrollbar.set)

            # اضافه کردن فیلد متنی و اسکرول بار به فریم
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            # ذخیره فیلدها در دیکشنری
            self.negative_entries[field_name] = entry

        # تنظیم کشش یکنواخت برای ستون‌ها و ردیف‌ها
        for col in range(2):  # ستون‌های 0 و 1
            self.negative_tab.grid_columnconfigure(col, weight=1)
        for row in range(len(field_names)):  # برای هر ردیف
            self.negative_tab.grid_rowconfigure(row + 5, weight=1)  # شروع از ردیف 5 برای لیبل‌ها

        # دکمه ذخیره
        save_button = tk.Button(self.positive_tab, text="ذخیره", command=self.save_positive)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

        save_button = tk.Button(self.negative_tab, text="ذخیره", command=self.save_negative)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def create_buttons(self):
        # دکمه ذخیره
        save_button = tk.Button(self.main_frame, text="ذخیره", command=self.save_positive)
        save_button.grid(row=len("labels"), column=0, columnspan=2, pady=10)

        self.cancel_button = tk.Button(self.main_frame, text="\u06A9\u0646\u0633\u0644", command=self.main_frame.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

    def center_window(self):
        window_width, window_height = 1450, 800
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.window.attributes('-topmost', True)

    def save_positive(self):
        # گرفتن داده‌ها از فرم سنوات مثبت
        positive_data = {field: entry.get() for field, entry in self.positive_entries.items()}
        self.db_manager.save_positive_seniority(self.national_code, positive_data)

    def save_negative(self):
        # گرفتن داده‌ها از فرم سنوات منفی
        negative_data = {field: entry.get() for field, entry in self.negative_entries.items()}
        self.db_manager.save_negative_seniority(self.national_code, negative_data)
