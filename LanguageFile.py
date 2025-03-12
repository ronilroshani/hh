import tkinter as tk
from tkinter import ttk


class LanguageFile:
    def __init__(self, parent, db_manager, national_code):
        self.parent = parent
        self.db_manager = db_manager
        self.national_code = national_code

        self.window = tk.Toplevel(self.parent)
        self.window.title("پرونده زبان های خارجی")
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
        # تب زبان
        self.language_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.language_tab, text="پرونده زبان")

        # نمایش تب‌ها
        self.tab_control.pack(expand=1, fill="both")
        self.center_window()

        # ایجاد فرم برای زبان
        self.create_language_form()

        self.window.lift()
        self.window.grab_set()

        self.load()

    def load(self):
        try:
            language_data = self.db_manager.get_language_by_national_code(self.national_code)
            self.fill(language_data=language_data)
        except Exception as e:
            print(f"\u062E\u0637\u0627: {e}")

    def fill(self, language_data=None):
        # پر کردن فرم زبان
        if language_data:
            for record in language_data:
                for field, value in record.items():
                    if field in self.language_entries:
                        self.language_entries[field].delete("1.0", "end")
                        self.language_entries[field].insert("1.0", value)

    def create_language_form(self):
        labels = [
            "نوع زبان:", "سطح زبان:",  "مدرک:",

        ]
        field_names = [
            "languageType", "LanguageDegree", "LanguageCertificate"
        ]

        self.language_entries = {}
        for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
            # ایجاد لیبل
            label = tk.Label(self.language_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17', anchor="e",
                             width=20)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="e")

            # ایجاد فریم برای فیلد متنی و اسکرول بار
            frame = tk.Frame(self.language_tab, bg='#c2b9ad')
            entry = tk.Text(frame, width=5, height=40, wrap='word', bg='#ffffff', fg='#1b1a17')
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=entry.yview)
            entry.config(yscrollcommand=scrollbar.set)

            # اضافه کردن فیلد متنی و اسکرول بار به فریم
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            # ذخیره فیلدها در دیکشنری
            self.language_entries[field_name] = entry

        # تنظیم کشش یکنواخت برای ستون‌ها و ردیف‌ها
        for col in range(2):  # ستون‌های 0 و 1
            self.language_tab.grid_columnconfigure(col, weight=1)
        for row in range(len(field_names)):  # برای هر ردیف
            self.language_tab.grid_rowconfigure(row + 5, weight=1)  # شروع از ردیف 5 برای لیبل‌ها

        # دکمه ذخیره
        save_button = tk.Button(self.language_tab, text="ذخیره", command=self.save_language)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def center_window(self):
        window_width, window_height = 1450, 800
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.window.attributes('-topmost', True)

    def save_language(self):
        # گرفتن داده‌ها از فرم زبان
        language_data = {field: entry.get("1.0", "end-1c") for field, entry in self.language_entries.items()}
        self.db_manager.save_language(self.national_code, language_data)
