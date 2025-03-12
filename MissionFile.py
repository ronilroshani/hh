import tkinter as tk
from tkinter import ttk

class MissionForm:
    def __init__(self, parent, db_manager, national_code):
        self.parent = parent
        self.db_manager = db_manager
        self.national_code = national_code

        self.window = tk.Toplevel(self.parent)
        self.window.title("فرم مأموریت")
        self.window.geometry("900x600")
        self.window.config(bg="#c2b9ad")
        self.window.attributes("-topmost", True)

        # قاب اصلی
        self.main_frame = tk.Frame(self.window, bg='#c2b9ad')
        self.main_frame.pack(fill="both", expand=True)

        # ایجاد تب‌ها
        self.tab_control = ttk.Notebook(self.main_frame)
        style = ttk.Style()
        style.configure("TFrame", background="#c2b9ad")

        self.internal_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.internal_tab, text="مأموریت داخلی")

        self.external_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.external_tab, text="مأموریت خارجی")

        self.tab_control.pack(expand=1, fill="both")

        self.create_internal_form()
        self.create_external_form()

        self.center_window()
        self.window.lift()
        self.window.grab_set()

        self.load_data()

    def center_window(self):
        window_width, window_height = 1450, 800
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def create_internal_form(self):
        labels = ["شرح مأموریت:", "تاریخ شروع:", "تاریخ پایان:", "مدت مأموریت (ماه):", "سازمان اعزام‌کننده:",
                  "مدرک مأموریت:", "آیا مأموریت خارجی است:"]
        field_names = ["MissionDescription", "MissionStartDate", "MissionEndDate", "MissionDurationInMonths",
                       "SendingOrganizationID", "MissionDocument", "IsForeignMission"]

        self.internal_entries = {}
        for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
            # ایجاد لیبل
            label = tk.Label(self.internal_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17', anchor="e", width=20)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="e")

            # ایجاد فریم برای فیلد
            frame = tk.Frame(self.internal_tab, bg='#c2b9ad')

            if field_name == "IsForeignMission":
                # ایجاد چک‌باکس برای فیلد "آیا مأموریت خارجی است"
                var = tk.BooleanVar()  # متغیری برای نگهداری وضعیت چک‌باکس
                entry = tk.Checkbutton(frame, text="بله", variable=var, onvalue=True, offvalue=False, bg='#c2b9ad')
                self.internal_entries[field_name] = var  # ذخیره متغیر برای استفاده بعدی
            else:
                # سایر فیلدها
                entry = tk.Text(frame, width=5, height=40, wrap='word', bg='#ffffff', fg='#1b1a17')
                scrollbar = tk.Scrollbar(frame, orient="vertical", command=entry.yview)
                entry.config(yscrollcommand=scrollbar.set)

                # اضافه کردن اسکرول بار به فریم
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                self.internal_entries[field_name] = entry  # ذخیره متغیر برای استفاده بعدی

            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

        # تنظیم کشش یکنواخت برای ستون‌ها و ردیف‌ها
        for col in range(len(field_names)):  # برای هر ستون
            self.internal_tab.grid_columnconfigure(col, weight=1)

        save_button = tk.Button(self.internal_tab, text="ذخیره", command=self.save_internal)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def create_external_form(self):
        labels = ["کشور:", "تاریخ شروع:", "تاریخ پایان:", "سازمان اعزام‌کننده:", "مدرک مأموریت:"]
        field_names = ["CountryID", "ForeignMissionStartDate", "ForeignMissionEndDate", "ForeignSendingOrganizationID",
                       "ForeignMissionDocument"]

        self.external_entries = {}
        for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
            # ایجاد لیبل
            label = tk.Label(self.external_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17', anchor="e", width=20)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="e")

            # ایجاد فریم برای فیلد و اسکرول بار
            frame = tk.Frame(self.external_tab, bg='#c2b9ad')
            entry = tk.Text(frame, width=5, height=40, wrap='word', bg='#ffffff', fg='#1b1a17')
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=entry.yview)
            entry.config(yscrollcommand=scrollbar.set)

            # اضافه کردن اسکرول بار به فریم
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            # ذخیره فیلدها در دیکشنری
            self.external_entries[field_name] = entry

        # تنظیم کشش یکنواخت برای ستون‌ها و ردیف‌ها
        for col in range(len(field_names)):  # برای هر ستون
            self.external_tab.grid_columnconfigure(col, weight=1)

        save_button = tk.Button(self.external_tab, text="ذخیره", command=self.save_external)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def load_data(self):
        try:
            mission_data = self.db_manager.get_mission_by_national_code(self.national_code)
            forigen_mission_data = self.db_manager.get_forigen_mission_by_national_code(self.national_code)
            if mission_data:
                self.fill_data(mission_data,forigen_mission_data)
        except Exception as e:
            print(f"خطا در بارگذاری داده‌ها: {e}")

    def fill_data(self, mission_data,forigen_mission_data):
            try:
                if mission_data:
                    for record in mission_data:
                        for field, value in record.items():
                            if field in self.internal_entries:
                                if field == "IsForeignMission":
                                    print("DDD")  # تنظیم مقدار چک‌باکس به True/False
                                else:
                                    if field in self.internal_entries:
                                        self.internal_entries[field].delete("1.0", "end")
                                        self.internal_entries[field].insert("1.0", value)

                if forigen_mission_data:
                    for record in forigen_mission_data:
                        for field, value in record.items():
                            if field in self.external_entries:
                                if field in self.external_entries:
                                    self.external_entries[field].delete("1.0", "end")
                                    self.external_entries[field].insert("1.0", value)

            except Exception as e:
                print(e)
                exit(None)
    def save_internal(self):
        try:
            data = {field: entry.get() for field, entry in self.internal_entries.items()}
            self.db_manager.save_internal_mission(self.national_code, data)
            print("مأموریت داخلی با موفقیت ذخیره شد.")
        except Exception as e:
            print(f"خطا در ذخیره مأموریت داخلی: {e}")

    def save_external(self):
        try:
            data = {field: entry.get() for field, entry in self.external_entries.items()}
            self.db_manager.save_external_mission(self.national_code, data)
            print("مأموریت خارجی با موفقیت ذخیره شد.")
        except Exception as e:
            print(f"خطا در ذخیره مأموریت خارجی: {e}")
