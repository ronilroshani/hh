import tkinter as tk
from tkinter import ttk, messagebox

import logging

from ShamsiCalendarApp import ShamsiCalendarApp

class FamilyFile:
    def __init__(self, parent, db_manager, national_code):
        self.field_names_Family = [
            "NationalCode", "FirstName", "LastName",  "BirthDate", "ShomareShenasname",
            "BirthPlaceID", "IssuePlaceID", "IssueDate", "GenderID", "RelationshipID", "FamilyJobID",
            "EducationLevelID", "RelationshipChangeID", "OrderNumber"
        ]

        self.parent = parent
        self.db_manager = db_manager
        self.national_code = national_code

        self.window = tk.Toplevel(self.parent)
        self.window.title("پرونده عائله")
        self.window.geometry("900x600")
        self.window.config(bg="#c2b9ad")
        self.window.attributes("-topmost", True)

        # قاب اصلی در پنجره جدید
        self.main_frame = tk.Frame(self.window, bg='#c2b9ad')
        self.main_frame.pack(fill="both", expand=True)

        # ایجاد تب‌ها
        self.Family_info_tab = ttk.Notebook(self.main_frame)
        style = ttk.Style()
        style.configure("TFrame", background="#c2b9ad")
        # تب مشاغل
        self.Family_tab = ttk.Frame(self.Family_info_tab, style="TFrame")
        self.Family_info_tab.add(self.Family_tab, text="مشاغل")

        # نمایش تب‌ها
        self.Family_info_tab.pack(expand=1, fill="both")
        self.center_window()

        # ایجاد فرم برای مشاغل
        self.create_Family_info_tab()

        self.window.lift()
        self.window.grab_set()
        self.table_frame = FamilyTable(self.window, self.get_column_names(), self.on_row_click)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.display_data()
        #self.load()

    def on_row_click(self, event):
        self.fill_Family_info_tab(self.national_code)

    def get_column_names(self):

        return [
             "کد ملی", "نام", "نام خانوادگی", "تاریخ تولد",
             "جنسیت","تاهل", "موبایل", ""
        ]

    def handle_error(self, title, message, detail):
        logging.error(f"{message}: {detail}")
        messagebox.showerror(title, f"{message}\n\n{detail}")

    def display_data(self, filtered_rows=None):
        query = ('SELECT  COUNT(*) FROM [FamilyFile] ')  # تغییر جهت محاسبه تعداد رکوردها
        try:
            self.total_records = int(self.db_manager.fetch_all(query)[0][0])  # تبدیل به عدد صحیح
        except Exception as e:
            self.handle_error("Error", "Error fetching total record count", str(e))
            return

         # start_index = (self.current_page.get() - 1) * self.records_per_page.get()
        # end_index = start_index + self.records_per_page.get()

        query = f'''
        SELECT *
        FROM [FamilyFile]
        '''

        if filtered_rows is None:
            try:
                rows = self.db_manager.fetch_all(query)
            except Exception as e:
                self.handle_error("Error", "Error executing query", str(e))
                return
        else:
            rows = filtered_rows

        # پاک کردن داده‌ها از هرگونه "دابل کوتیشن"
        cleaned_rows = []
        for row in rows:
            cleaned_row = tuple(str(cell).replace('"', '') if isinstance(cell, str) else cell for cell in row)
            cleaned_rows.append(cleaned_row)


        self.table_frame.update_data(cleaned_rows)
        # self.update_page_info()
        # self.update_navigation_buttons()


    def center_window(self):
        window_width, window_height = 1450, 800
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.window.attributes('-topmost', True)

    def create_Family_info_tab(self):
            # دیکشنری برای نگه‌داری ورودی‌های هر فیلد
            self.Family_fields = {}
            # برچسب‌ها و ورودی‌های فیلدهای اطلاعات شخصی
            labels = [
                "کد ملی:", "نام:", "نام خانوادگی:", "تاریخ تولد:", "شماره شناسنامه:",
                "محل تولد:", "محل صدور:", "تاریخ صدور:", "جنسیت:", "نسبت", "شغل", "تحصیلات", "تغییرات ", "شماره دستور"
            ]

            self.field_names_Family = [
                "NationalCode", "FirstName", "LastName", "BirthDate", "ShomareShenasname",
                "BirthPlaceID", "IssuePlaceID", "IssueDate", "GenderID", "RelationshipID", "FamilyJobID",
                "EducationLevelID", "RelationshipChangeID", "OrderNumber"
            ]

            # ایجاد برچسب‌ها و ورودی‌ها در تب
            for i, (label_text, field_name) in enumerate(zip(labels, self.field_names_Family)):
                label = tk.Label(self.Family_info_tab, text=label_text,bg='#c2b9ad', fg='#1b1a17')
                label.grid(row=i, column=0, sticky=tk.W)
                if field_name in ["GenderID", "","BirthPlaceID", "IssuePlaceID", "RelationshipID",
                                  "FamilyJobID","EducationLevelID", "RelationshipChangeID"]:
                    entry = ttk.Combobox(self.Family_info_tab)
                    self.load_combobox_data_Family(entry, field_name)
                    self.Family_fields[field_name] = entry  # ذخیره Combobox به جای Entry
                elif field_name in ["IssueDate","BirthDate"]:
                    entry = tk.Entry(self.Family_info_tab,width=24)
                    self.Family_fields[field_name] = entry
                    calendar_button = tk.Button(
                        self.Family_info_tab,
                        text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                        command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2)
                    )
                    calendar_button.grid(row=i, column=2)
                # استفاده از Combobox برای فیلدهای مشخص
                elif field_name in ["FirstName", "LastName", "FatherName"]:
                    entry = tk.Entry(self.Family_info_tab,width=24)
                    entry.bind('<KeyRelease>', lambda event, ent=entry: self.validate_persian_text(ent))
                    self.Family_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
                elif field_name in ["NationalCode"]:
                    entry = tk.Entry(self.Family_info_tab,width=24)
                    self.Family_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
                    entry.bind('<KeyRelease>', lambda event, ent=entry: self.check_national_code(ent))
                    entry.insert(0, self.national_code)
                else:
                    entry = tk.Entry(self.Family_info_tab,width=24)
                    self.Family_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
                entry.grid(row=i, column=1)

    def load_combobox_data_Family(self, combobox, field_name):
        data_dict = {}
        if field_name == "GenderID":
            query = "SELECT * FROM Gender"
        elif field_name == "BirthPlaceID":
            query = "SELECT * FROM City"
        elif field_name == "IssuePlaceID":
            query = "SELECT * FROM City"
        elif field_name == "RelationshipID":
            query = "SELECT * FROM Relationship"
        elif field_name == "FamilyJobID":
            query = "SELECT * FROM FamilyJob"
        elif field_name == "EducationLevelID":
            query = "SELECT * FROM EducationLevel"
        elif field_name == "RelationshipChangeID":
            query = "SELECT * FROM RelationshipChange"
        else:
            return

        try:
            # دریافت نتایج از پایگاه داده
            results = self.db_manager.fetch_all(query)
            # اضافه کردن مقدار "انتخاب کنید..." به لیست مقادیر و فیلتر کردن مقادیر خالی
            values = [row[1] for row in results if row[1]]
            for row in results:
                if row[1]:  # فقط مقادیر غیر خالی
                    data_dict[row[0]] = row[1]

            # تنظیم مقادیر برای combobox و قرار دادن اولین مقدار به عنوان پیش‌فرض
            combobox['values'] = values
            combobox['state'] = 'readonly'
            if values:
                combobox.current(0)
            # ذخیره دیکشنری به عنوان یک ویژگی کلاس
            setattr(self, f"{field_name}_data_dict", data_dict)

        except Exception as e:
            logging.error(f"Error loading {field_name} data: {e}")
            messagebox.showerror("Error", f"Failed to load {field_name} data. Please try again.")

    def fill_Family_info_tab(self, national_code):
            if not hasattr(self, 'Family_fields'):
                print("Error: Family_fields is not defined.")
                return

            try:
                # اجرای کوئری برای دریافت اطلاعات شخصی
                query = "SELECT * FROM FamilyFile WHERE NationalCode = ?"
                result = self.db_manager.fetch_one(query, (national_code,))

                if not result:
                    print(f"Fill Error: No Family info found for the given National Code: {national_code}.")
                    return

                for field_name in list(self.Family_fields.keys()):
                    widget = self.Family_fields[field_name]
                    field_index = self.field_names_Family.index(field_name)
                    entry_value = result[field_index + 1] if result[field_index + 1] is not None else ""

                    if isinstance(widget, ttk.Combobox):
                        # اگر ویجت Combobox است
                        data_dict = getattr(self, f"{field_name}_data_dict", {})
                        display_value = data_dict.get(entry_value, None)
                        if display_value:  # اگر مقدار یافت شد
                            widget.set(display_value)
                        else:  # مقدار نامعتبر است
                            widget.set("نامشخص")  # مقدار خالی
                    elif isinstance(widget, tk.Text):
                        # اگر ویجت Text است
                        widget.delete("1.0", tk.END)  # حذف محتوای قبلی
                        # اگر مقدار ورودی خالی است، مقدار پیش‌فرض را بگذارید
                        if entry_value is None or entry_value == "":
                            entry_value = "مقدار خالی"
                        widget.config(wrap=tk.WORD)  # wrap به صورت خودکار به کلمات منتقل می‌شود
                        widget.insert("1.0", entry_value)  # درج مقدار جدید
                    elif field_name in "National_Code":
                        continue
                    else:
                        # اگر ویجت Entry است
                        widget.delete(0, tk.END)
                        widget.insert(0, entry_value)

            except Exception as e:
                logging.error(f"Fill Error: Error fetching Family File: {e}")
                print(f"Fill Error: Database Error: {e}")

    def validate_persian_text(self, entry):
        # تنها حروف فارسی
        if re.match(r'^[\u0600-\u06FF\s]*$', entry.get()):
            entry.config(bg='white')  # اگر درست بود رنگ سفید
        else:
            entry.config(bg='red')  # اگر اشتباه بود رنگ قرمز

    def open_calendar(self, entry, row, column, pady):
        # باز کردن تقویم و دریافت تاریخ شمسی
        def on_date_select(selected_date):
            """کال‌بک برای انتخاب تاریخ."""
            # پاک کردن مقدار قبلی و درج مقدار جدید در فیلد
            entry.delete(0, tk.END)
            entry.insert(0, selected_date)  #

        calendar_app = ShamsiCalendarApp(
            root=self.parent,
            entry=entry,
            on_date_select_callback=on_date_select

        )


class FamilyTable(tk.Frame):
    def __init__(self, parent, columns, on_row_click):
        print("vvvvv")

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
