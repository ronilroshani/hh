import tkinter as tk
from tkinter import ttk


class EmployeeEvaluationFile:
    def __init__(self, parent,  national_code,db_manager,lll):

        self.start_year= 1400
        self.parent = parent
        self.db_manager = db_manager
        self.national_code = national_code

        self.window = tk.Toplevel(self.parent)
        self.window.title("پرونده ارزیابی کارمندان")
        self.window.geometry("900x600")
        self.window.config(bg="#e6e6e6")
        self.window.attributes("-topmost", True)

        # قاب اصلی
        self.main_frame = tk.Frame(self.window, bg='#e6e6e6')
        self.main_frame.pack(fill="both", expand=True)

        # ایجاد تب‌ها
        self.tab_control = ttk.Notebook(self.main_frame)
        style = ttk.Style()
        style.configure("TFrame", background="#e6e6e6")

        # تب ارزیابی
        self.evaluation_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.evaluation_tab, text="ارزیابی کارمند")

        # نمایش تب‌ها
        self.tab_control.pack(expand=1, fill="both")
        self.center_window()

        # ایجاد فرم
        self.create_evaluation_form()

        self.window.lift()
        self.window.grab_set()

        # بارگذاری اطلاعات
        self.load()

    def load(self):
        try:
            evaluation_data = self.db_manager.get_evaluation_by_national_code(self.national_code)
            self.fill(evaluation_data=evaluation_data)

        except Exception as e:
            print(f"خطا در بارگذاری اطلاعات: {e}")

    def generate_evaluation_form(self):
        """تولید فرم برای 30 سال ارزیابی به‌طور دو سطری"""
        self.form_inputs = []  # لیستی برای ذخیره ویجت‌های QLineEdit مربوط به نمرات

        for i in range(0, 30, 2):
            # محاسبه سال‌های جاری
            year_1 = self.start_year + i
            year_2 = self.start_year + i + 1

            # ایجاد لیبل و فیلد ورودی برای سال اول
            year_label_1 = QLabel(f"سال {i + 1} ({year_1}):")
            score_input_1 = QLineEdit()
            score_input_1.setPlaceholderText("نمره ارزیابی")
            self.form_inputs.append(score_input_1)  # ذخیره در لیست

            # ایجاد لیبل و فیلد ورودی برای سال دوم
            year_label_2 = QLabel(f"سال {i + 2} ({year_2}):")
            score_input_2 = QLineEdit()
            score_input_2.setPlaceholderText("نمره ارزیابی")
            self.form_inputs.append(score_input_2)  # ذخیره در لیست

            # ایجاد چیدمان افقی برای دو سال
            row_layout = QHBoxLayout()
            row_layout.addWidget(year_label_1)
            row_layout.addWidget(score_input_1)
            row_layout.addStretch()
            row_layout.addWidget(year_label_2)
            row_layout.addWidget(score_input_2)

            # افزودن چیدمان به فرم اصلی
            self.layout.addLayout(row_layout)
            self.layout.addSpacing(10)  # اضافه کردن فاصله بین ردیف‌ها
    def fill(self, evaluation_data=None):
        # پر کردن فرم ارزیابی
        if evaluation_data:
            for record in evaluation_data:
                for field, value in record.items():
                    if field in self.evaluation_entries:
                        self.evaluation_entries[field].delete(0, "end")
                        self.evaluation_entries[field].insert(0, value)
    def create_evaluation_form(self):
            try:
                """ایجاد فرم ارزیابی برای 30 سال به صورت دو سطری"""
                self.form_inputs = []  # لیست ذخیره فیلدهای QLineEdit

                for i in range(0, 30, 2):
                    # محاسبه سال‌های جاری
                    year_1 = self.start_year + i
                    year_2 = self.start_year + i + 1

                    # ایجاد لیبل و فیلد ورودی برای سال اول
                    year_label_1 = QLabel(f"سال {i + 1} ({year_1}):")
                    score_input_1 = QLineEdit()
                    score_input_1.setPlaceholderText("نمره ارزیابی")
                    self.form_inputs.append(score_input_1)  # ذخیره در لیست

                    # ایجاد لیبل و فیلد ورودی برای سال دوم
                    year_label_2 = QLabel(f"سال {i + 2} ({year_2}):")
                    score_input_2 = QLineEdit()
                    score_input_2.setPlaceholderText("نمره ارزیابی")
                    self.form_inputs.append(score_input_2)  # ذخیره در لیست

                    # ایجاد چیدمان افقی برای یک ردیف
                    row_layout = QHBoxLayout()
                    row_layout.addWidget(year_label_1)
                    row_layout.addWidget(score_input_1)
                    row_layout.addStretch()
                    row_layout.addWidget(year_label_2)
                    row_layout.addWidget(score_input_2)

                    # اضافه کردن چیدمان به لایه اصلی فرم
                    self.layout.addLayout(row_layout)
                    self.layout.addSpacing(10)  # فاصله بین ردیف‌ها
            except Exception as e:
                print(e)
    def center_window(self):
        window_width, window_height = 900, 600
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.window.attributes('-topmost', True)
    def save_evaluation(self):
        try:
            # گرفتن داده‌ها از فرم
            evaluation_data = {field: entry.get() for field, entry in self.evaluation_entries.items()}
            self.db_manager.save_employee_evaluation(self.national_code, evaluation_data)
            print("اطلاعات ارزیابی با موفقیت ذخیره شد.")
        except Exception as e:
            print(f"خطا در ذخیره‌سازی اطلاعات: {e}")

    def create_evaluation_form(self):
        """ایجاد فرم ارزیابی برای 30 سال به صورت دو سطری با Tkinter"""
        self.form_inputs = []  # لیست ذخیره فیلدهای tk.Entry

        # قاب برای محتوای فرم
        form_frame = tk.Frame(self.evaluation_tab, bg="#e6e6e6")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for i in range(0, 30, 2):
            # محاسبه سال‌های جاری
            year_1 = self.start_year + i
            year_2 = self.start_year + i + 1

            # ایجاد لیبل و فیلد ورودی برای سال اول
            year_label_1 = tk.Label(form_frame, text=f"سال {i + 1} ({year_1}):", bg="#e6e6e6", width=15, anchor="w")
            score_input_1 = tk.Entry(form_frame, width=10)
            self.form_inputs.append(score_input_1)

            # ایجاد لیبل و فیلد ورودی برای سال دوم
            year_label_2 = tk.Label(form_frame, text=f"سال {i + 2} ({year_2}):", bg="#e6e6e6", width=15, anchor="w")
            score_input_2 = tk.Entry(form_frame, width=10)
            self.form_inputs.append(score_input_2)

            # چیدمان در دو سطر (ردیف و ستون)
            year_label_1.grid(row=i // 2, column=0, padx=5, pady=5, sticky="w")
            score_input_1.grid(row=i // 2, column=1, padx=5, pady=5)
            year_label_2.grid(row=i // 2, column=2, padx=5, pady=5, sticky="w")
            score_input_2.grid(row=i // 2, column=3, padx=5, pady=5)
