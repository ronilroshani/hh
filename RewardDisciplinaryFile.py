import tkinter as tk
from tkinter import ttk, messagebox

class RewardDisciplinary:
    def __init__(self, master, db_manager, national_code=None):
        try:
            self.db_manager = db_manager
            self.national_code = national_code

            # ایجاد پنجره جدید به جای استفاده از پنجره اصلی
            self.master = tk.Toplevel(master)  # پنجره جدید
            self.master.title("ارزشیابی کارمند")
            self.master.config(bg='#c2b9ad')
            self.master.attributes("-topmost", True)

            # تنظیم سایز پنجره و موقعیت آن در وسط
            self.center_window()

            # قاب اصلی در پنجره جدید
            self.main_frame = tk.Frame(self.master, bg='#c2b9ad')
            self.main_frame.pack(fill="both", expand=True)

            # تنظیمات پویا برای گرید اصلی
            self.master.grid_rowconfigure(0, weight=1)
            self.master.grid_columnconfigure(0, weight=1)

            # نوت‌بوک برای تب‌ها
            self.notebook = ttk.Notebook(self.main_frame)
            self.notebook.pack(fill="both", expand=True)

            # تب تشویقات
            self.reward_tab = tk.Frame(self.notebook, bg='#c2b9ad')
            self.notebook.add(self.reward_tab, text="\u062A\u0634\u0648\u06CC\u0642\u0627\u062A")

            # تب تنبیهات
            self.disciplinary_tab = tk.Frame(self.notebook, bg='#c2b9ad')
            self.notebook.add(self.disciplinary_tab, text="\u062A\u0646\u0628\u06CC\u0647\u0627\u062A")

            # ایجاد فرم‌ها برای هر تب
            self.create_reward_form()
            self.create_disciplinary_form()

            # بازیابی داده‌ها از پایگاه داده
            self.master.lift()
            self.master.grab_set()
            self.create_buttons()

            self.load()
        except Exception as e:
            messagebox.showerror("\u062E\u0637\u0627",
                                 f"\u062E\u0637\u0627 \u062F\u0631 \u0627\u06CC\u062C\u0627\u062F \u0641\u0631\u0645 \u062A\u0634\u0648\u06CC\u0642\u0627\u062A \u0648 \u062A\u0646\u0628\u06CC\u0647\u0627\u062A: {e}")
            print(e)

    # ایجاد دکمه‌
    def create_buttons(self):
        self.save_button = tk.Button(self.main_frame, text="\u0630\u062E\u064A\u0631\u0647", command=self.save_promotion)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.cancel_button = tk.Button(self.main_frame, text="\u06A9\u0646\u0633\u0644", command=self.master.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

    def center_window(self):
        window_width, window_height = 1050, 800
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.master.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.master.attributes('-topmost', True)

    def load(self):
        try:
            reward_data = self.db_manager.get_reward_by_national_code(self.national_code)
            disciplinary_data = self.db_manager.get_disciplinary_by_national_code(self.national_code)
            self.fill(reward_data=reward_data, disciplinary_data=disciplinary_data)
        except Exception as e:
            print(f"\u062E\u0637\u0627: {e}")

    def fill(self, reward_data=None, disciplinary_data=None):
        # پر کردن فرم تشویقات
        if reward_data:
            for field, value in reward_data.items():
                if field in self.reward_entries:
                    self.reward_entries[field].delete("1.0", "end")
                    self.reward_entries[field].insert("1.0", value)

        # پر کردن فرم تنبیهات
        if disciplinary_data:
            for field, value in disciplinary_data.items():
                if field in self.disciplinary_entries:
                    self.disciplinary_entries[field].delete("1.0", "end")
                    self.disciplinary_entries[field].insert("1.0", value)

    def create_disciplinary_form(self):
        labels = ["\u0646\u0648\u0639 \u062A\u0646\u0628\u06CC\u0647:",
                  "\u0645\u062F\u062A \u0632\u0645\u06270640\u0646 \u062A\u0646\u0628\u06CC\u0647:",
                  "\u062A\u0627\u0631\u06CC\u062E \u0634\u0631\u0648\u0639:",
                  "\u0645\u062F\u0631\u06A9 \u062A\u0646\u0628\u06CC\u0647:",
                  "\u0631\u062A\u0628\u0647 \u062F\u0631 \u0632\u0645\u0627\u0646 \u062A\u0646\u0628\u06CC\u0647:",
                  "\u062F\u0644\u0627\u06CC\u0644:"]
        field_names = ["ActionType", "ActionDuration", "StartDate", "Document", "Rank", "Reason"]

        self.disciplinary_entries = {}
        # نمایش لیبل‌ها در سطرهای مختلف
        for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
            # ایجاد لیبل
            label = tk.Label(self.disciplinary_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17', anchor="e",
                             width=20)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="e")

            # ایجاد فریم برای فیلد متنی و اسکرول بار
            frame = tk.Frame(self.disciplinary_tab, bg='#c2b9ad')
            entry = tk.Text(frame, width=5, height=40, wrap='word', bg='#ffffff', fg='#1b1a17')
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=entry.yview)
            entry.config(yscrollcommand=scrollbar.set)

            # اضافه کردن فیلد متنی و اسکرول بار به فریم
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            # ذخیره فیلدها در دیکشنری
            self.disciplinary_entries[field_name] = entry

        # تنظیم کشش یکنواخت برای ستون‌ها و ردیف‌ها
        for col in range(2):  # ستون‌های 0 و 1
            self.disciplinary_tab.grid_columnconfigure(col, weight=1)
        for row in range(len(field_names)):  # برای هر ردیف
            self.disciplinary_tab.grid_rowconfigure(row + 5, weight=1)  # شروع از ردیف 5 برای لیبل‌ها

    def create_reward_form(self):
        labels = ["\u0646\u0648\u0639 \u062A\u0634\u0648\u06CC\u0642:",
                  "\u062A\u0627\u0631\u06CC\u062E \u062A\u0634\u0648\u06CC\u0642:",
                  "\u0627\u0646\u06AF\u06CC\u0632\u0647 \u062A\u0634\u0648\u06CC\u0642:",
                  "\u0631\u062A\u0628\u0647 \u062F\u0631 \u0632\u0645\u0627\u0646 \u062A\u0634\u0648\u06CC\u0642:",
                  "\u0645\u062F\u0631\u06A9 \u062A\u0634\u0648\u06CC\u0642:"]
        field_names = ["RewardType", "RewardDate", "Motivation", "RankAtTime", "Document"]
        self.reward_entries = {}
        # نمایش لیبل‌ها در سطرهای مختلف
        for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
            # ایجاد لیبل
            label = tk.Label(self.reward_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17', anchor="e",
                             width=20)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="e")

            # ایجاد فریم برای فیلد متنی و اسکرول بار
            frame = tk.Frame(self.reward_tab, bg='#c2b9ad')
            entry = tk.Text(frame, width=5, height=40, wrap='word', bg='#ffffff', fg='#1b1a17')
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=entry.yview)
            entry.config(yscrollcommand=scrollbar.set)

            # اضافه کردن فیلد متنی و اسکرول بار به فریم
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            # ذخیره فیلدها در دیکشنری
            self.reward_entries[field_name] = entry

        # تنظیم کشش یکنواخت برای ستون‌ها و ردیف‌ها
        for col in range(2):  # ستون‌های 0 و 1
            self.reward_tab.grid_columnconfigure(col, weight=1)
        for row in range(len(field_names)):  # برای هر ردیف
            self.reward_tab.grid_rowconfigure(row + 5, weight=1)  # شروع از ردیف 5 برای لیبل‌ها

    def save_promotion(self):
        self.save_reward()
        self.save_disciplinary()

    def save_reward(self):
        reward_data = {field: entry.get("1.0", "end-1c") for field, entry in self.reward_entries.items()}
        self.db_manager.save_reward(self.national_code, reward_data)

    def save_disciplinary(self):
        disciplinary_data = {field: entry.get("1.0", "end-1c") for field, entry in self.disciplinary_entries.items()}
        self.db_manager.save_disciplinary(self.national_code, disciplinary_data)
