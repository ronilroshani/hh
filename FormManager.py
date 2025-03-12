from PIL import Image, ImageTk
import os
from tkinter import filedialog
from tkinter import filedialog  # اینجا filedialog وارد می‌شود
from tkinter import ttk, messagebox
import re  # برای اعتبارسنجی داده‌ها
import logging
from PyQt5 import QtCore, QtWidgets
import tkinter as tk
import jdatetime
from ShamsiCalendarApp import ShamsiCalendarApp
from tkinter import filedialog  # اضافه کردن این ماژول برای باز کردن دیالوگ انتخاب فایل
from PIL import Image, ImageTk  # اطمینان حاصل کنید که این کتابخانه را برای تغییر سایز و پردازش عکس‌ها نصب کرده‌اید.
from tkinter import PhotoImage
from tkinter import Toplevel, Label
from MissionFile import MissionForm
from RewardDisciplinaryFile import RewardDisciplinary
from tkinter import Button, Label, Entry, Tk
from SeniorityFile import SeniorityForm
from AccidentFile import AccidentFile
from LanguageFile import LanguageFile
from MillitaryFile import MillitaryFile
from ClassicFile import ClassicFile
from PromotionFile import PromotionFile
from JobFiles import JobFile
from EmployeeEvaluationFile import EmployeeEvaluationFile
from FamilyFile import FamilyFile
class FormManager:
    def __init__(self, root, db_manager):
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), padding=10, background='#f9f3eb', foreground='red')
        style.configure('TLabel', font=('Helvetica', 12), background='#c2b9ad', foreground='red', padding=10)
        style.configure('TEntry', font=('Helvetica', 12), background='#c2b9ad', foreground='red', padding=10)
        style.configure('TCombobox', font=('Helvetica', 12))
        style.configure('TLabelframe', font=('Helvetica', 12))
        self.root = root  # فرض بگیریم root پنجره اصلی Tkinter شماست
        self.details_window = None
        self.firstName = 'NOEE'
        self.lastName = 'NONE'
        self.info_frame = None  # تعریف info_frame
        self.notebook = None
        self.current_id = None
        self.national_code = None
        self.is_shamsi = True  # به‌صورت پیش‌فرض شمسی است
        self.db_manager = db_manager
        # بارگذاری مقادیر از پایگاه داده
        self.load_data()
        # دیکشنری برای نگه‌داری ورودی‌های هر فیلد
        self.promotions_fields = {}
        self.tabs_dict = {}
        self.education_fields = {}
        self.personal_fields = {
            'NationalCode': tk.Entry(),
            'FirstName': tk.Entry(),
            'LastName': tk.Entry(),
            'FatherName': tk.Entry(),
            'NickName': tk.Entry(),
            'BirthDate': tk.Entry(),
            'BirthPlaceID': ttk.Combobox(root, values=[]),
            'IssuePlaceID': ttk.Combobox(root, values=[]),
            'IssueDate': tk.Entry(),
            'GenderID': ttk.Combobox(root, values=[]),
            'MaritalStatusID': ttk.Combobox(root, values=[]),
            'ReligionID': ttk.Combobox(root, values=[]),
            'BloodGroupID': ttk.Combobox(root, values=[]),
            'Height': tk.Entry(),
            'Weight': tk.Entry(),
            'EyeColorID': ttk.Combobox(root, values=[]),
            'SkinColorID': ttk.Combobox(root, values=[]),
            'SpecialFeatures': tk.Text(),
            'Address': tk.Text(),
            'PostalCode': tk.Entry(),
            'PhoneNumber': tk.Entry(),
            'Mobile': tk.Entry(),
            'Email': tk.Entry(),
            'PersonalID': tk.Entry()
        }
        self.field_names_promotion = {
            "NationalCode": tk.Entry(),
            "CurrentRank": ttk.Combobox(root, values=[]),
            "PromotionDate": tk.Entry(),
            "NextRank": ttk.Combobox(root, values=[]),
            "NextPromotionDate": tk.Entry(),
            "SeniorityDays": tk.Entry(),
            "DeductionDays": tk.Entry(),
            "RankType": ttk.Combobox(root, values=[]),
            "TemporaryRankCount": tk.Entry(),
            "PromotionDescription": tk.Entry(),
            "Inquiries": tk.Entry(),
            "AdjustmentRankID": ttk.Combobox(root, values=[]),
            "AdjustmentSeniorityDays": tk.Entry(),
            "PromotionStages": tk.Entry(),
            "FirstSalaryIncrease": tk.Entry(),
            "FirstSalaryIncreaseDate": tk.Entry(),
            "SecondSalaryIncrease": tk.Entry(),
            "SecondSalaryIncreaseDate": tk.Entry(),
            "ThirdSalaryIncrease": tk.Entry(),
            "ThirdSalaryIncreaseDate": tk.Entry(),
            "FourthSalaryIncrease": tk.Entry(),
            "FourthSalaryIncreaseDate": tk.Entry()
        }
        self.employee_fields = {
            'NationalCode': tk.Entry(),  # کد ملی
            'BaseCode': ttk.Combobox(root, values=[]),  # کد پایگاهی
            'EmploymentStatusID': ttk.Combobox(root, values=[]),  # شناسه وضعیت استخدامی
            'LawBasedEmploymentID': ttk.Combobox(root, values=[]),  # شناسه قانون استخدامی
            'ExpertiseID': ttk.Combobox(root, values=[]),  # شناسه تخصص یا رسته
            'ServiceLocationID': ttk.Combobox(root, values=[]),  # شناسه محل خدمت
            'OperationalSupportRole': tk.Entry(),  # نقش صف یا ستاد
            'InitialMembershipTypeID': ttk.Combobox(root, values=[]),  # نوع عضویت اولیه
            'HiringUnitID': ttk.Combobox(root, values=[]),  # واحد استخدام کننده
            'CurrentMembershipTypeID': ttk.Combobox(root, values=[]),  # نوع عضویت فعلی
            'LatestServiceStatusID': ttk.Combobox(root, values=[]),  # آخرین وضعیت خدمتی
            'EntryTransferDate': tk.Entry(),  # تاریخ ورود یا انتقال
            'StateID': ttk.Combobox(root, values=[]),  # شناسه استان
            'CountyID': ttk.Combobox(root, values=[]),  # شناسه شهرستان
            'OrganizationID': ttk.Combobox(root, values=[]),  # شناسه سازمان
            'DeputyCenterID': ttk.Combobox(root, values=[]),  # شناسه معاونت یا گروه/مرکز
            'SubdivisionManagementID': ttk.Combobox(root, values=[]),  # مدیریت زیرمجموعه
            'SectionDepartmentID': ttk.Combobox(root, values=[]),  # دایره یا قسمت
            'MissionLocationID': ttk.Combobox(root, values=[]),  # محل ماموریت
            'LastStatusID': ttk.Combobox(root, values=[]),  # وضعیت فعلی
        }
        self.fields = {}  #  self.fields یک دیکشنری است
        self.family_fields= {
            "NationalCode": tk.Entry(),  # کد ملی
            "MarriageDate": tk.IntVar(),  # تاریخ ازدواج
            "TotalDependents": tk.IntVar(),  # تعداد کل عائله
            "TotalChildren": tk.IntVar(),  # تعداد کل فرزندان
            "TotalDaughters": tk.IntVar(),  # تعداد فرزند دختر
            "TotalSons": tk.IntVar() # تعداد فرزند پسر
        }
        self.employment_fields = {
            'NationalCode': tk.Entry(),  # کد ملی
            'BaseCode': ttk.Combobox(root, values=[]),  # کد پایگاهی
            'EmploymentStatusID': ttk.Combobox(root, values=[]),  # شناسه وضعیت استخدامی
            'LawBasedEmploymentID': ttk.Combobox(root, values=[]),  # شناسه قانون استخدامی
            'ExpertiseID': ttk.Combobox(root, values=[]),  # شناسه تخصص یا رسته
            'ServiceLocationID':ttk.Combobox(root, values=[]),  # شناسه محل خدمت
            'OperationalSupportRole': tk.Entry(),  # نقش صف یا ستاد
            'InitialMembershipTypeID': ttk.Combobox(root, values=[]),  # نوع عضویت اولیه
            'HiringUnitID': ttk.Combobox(root, values=[]),  # واحد استخدام کننده
            'CurrentMembershipTypeID': ttk.Combobox(root, values=[]),  # نوع عضویت فعلی
            'LatestServiceStatusID': ttk.Combobox(root, values=[]),  # آخرین وضعیت خدمتی
            'EntryTransferDate': tk.Entry(),  # تاریخ ورود یا انتقال
            'StateID': ttk.Combobox(root, values=[]),  # شناسه استان
            'CountyID': ttk.Combobox(root, values=[]),  # شناسه شهرستان
            'OrganizationID': ttk.Combobox(root, values=[]),  # شناسه سازمان
            'DeputyCenterID': ttk.Combobox(root, values=[]),  # شناسه معاونت یا گروه/مرکز
            'SubdivisionManagementID': ttk.Combobox(root, values=[]),  # مدیریت زیرمجموعه
            'SectionDepartmentID': ttk.Combobox(root, values=[]),  # دایره یا قسمت
            'MissionLocationID': ttk.Combobox(root, values=[]),  # محل ماموریت
            'LastStatusID': ttk.Combobox(root, values=[]),  # وضعیت فعلی
        }
        self.mission_fields = {
            'NationalCode': tk.Entry(),  # کد ملی
            'BaseCode': tk.Entry(),  # کد پایگاهی
            'EmploymentStatusID': tk.Entry(),  # شناسه وضعیت استخدامی
            'LawBasedEmploymentID': tk.Entry(),  # شناسه قانون استخدامی
            'ExpertiseID': tk.Entry(),  # شناسه تخصص یا رسته
            'ServiceLocationID': tk.Entry(),  # شناسه محل خدمت
            'OperationalSupportRole': tk.Entry(),  # نقش صف یا ستاد
            'InitialMembershipTypeID': tk.Entry(),  # نوع عضویت اولیه
            'HiringUnitID': tk.Entry(),  # واحد استخدام کننده
            'CurrentMembershipTypeID': tk.Entry(),  # نوع عضویت فعلی
            'LatestServiceStatusID': tk.Entry(),  # آخرین وضعیت خدمتی
            'EntryTransferDate': tk.Entry(),  # تاریخ ورود یا انتقال
            'StateID': tk.Entry(),  # شناسه استان
            'CountyID': tk.Entry(),  # شناسه شهرستان
            'OrganizationID': tk.Entry(),  # شناسه سازمان
            'DeputyCenterID': tk.Entry(),  # شناسه معاونت یا گروه/مرکز
            'SubdivisionManagementID': tk.Entry(),  # مدیریت زیرمجموعه
            'SectionDepartmentID': tk.Entry(),  # دایره یا قسمت
            'MissionLocationID': tk.Entry(),  # محل ماموریت
            'CurrentStatusID': tk.Entry(),  # وضعیت فعلی
        }
        self.field_names_personal = [
            "NationalCode", "FirstName", "LastName", "FatherName", "NickName", "BirthDate",
            "BirthPlaceID", "IssuePlaceID", "IssueDate", "GenderID", "MaritalStatusID", "ReligionID",
            "BloodGroupID", "Height", "Weight", "EyeColorID", "SkinColorID", "SpecialFeatures",
            "Address", "PostalCode", "PhoneNumber", "Mobile", "Email", "PersonalID"
        ]

        field_names = [
            "NationalCode", "EducationLevelID", "Major", "DegreeLevelID",
            "City", "UniversityID", "GraduationDate", "DegreeTypeID",
            "IserID", "Gerayesh", "GPA", "EmploymentDegreeLevelID", "MilitaryEducation", "MilitaryEducationLocation"
        ]
        self.field_names_education = [
            "NationalCode", "EducationLevelID", "Major", "DegreeLevelID",
            "City", "UniversityID", "GraduationDate", "DegreeTypeID",
            "IserID", "Gerayesh", "GPA", "EmploymentDegreeLevelID", "MilitaryEducation", "MilitaryEducationLocation"
        ]
        self.field_names_employee = [
            "NationalCode", "BaseCode",  "EmploymentStatusID", "LawBasedEmploymentID", "ExpertiseID",
            "ServiceLocationID","OperationalSupportRole", "InitialMembershipTypeID","HiringUnitID",
            "CurrentMembershipTypeID", "LatestServiceStatusID","EntryTransferDate","StateID", "CountyID",
            "OrganizationID","DeputyCenterID","SubdivisionManagementID", "SectionDepartmentID","MissionLocationID",
            "LastStatusID"
        ]
        self.promotion_fields = [
            "NationalCode", "CurrentRank", "PromotionDate", "NextRank",
            "NextPromotionDate", "SeniorityDays", "DeductionDays", "RankType",
            "TemporaryRankCount", "PromotionDescription", "Inquiries", "AdjustmentRank",
            "AdjustmentSeniorityDays", "PromotionStages", "FirstSalaryIncrease",
            "FirstSalaryIncreaseDate", "SecondSalaryIncrease", "SecondSalaryIncreaseDate",
            "ThirdSalaryIncrease", "ThirdSalaryIncreaseDate", "FourthSalaryIncrease",
            "FourthSalaryIncreaseDate"
        ]
        self.field_names_job = [
            "NationalCode", "JobTitle", "JobID", "PostKey", "JobLevel",
            "JobGroupID", "WorkLocationID", "AppointmentDate", "AppointmentTypeID",
            "DegreeID", "AccessLevelID", "JobTypeID", "DepartmentID", "JobRankID", "SectionID"
        ]
        self.field_names_bank = [
            "NationalCode", "BankIndex", "BankNameID", "BranchName",
            "AccountNumber", "AccountTypeID", "CardNumber", "IBAN"
        ]
        self.field_names_employee = [
            "NationalCode",
            "BaseCode",
            "EmploymentStatusID",
            "LawBasedEmploymentID",
            "ExpertiseID",
            "ServiceLocationID",
            "OperationalSupportRole",
            "InitialMembershipTypeID",
            "HiringUnitID",
            "CurrentMembershipTypeID",
            "LatestServiceStatusID",
            "EntryTransferDate",
            "StateID",
            "CountyID",
            "OrganizationID",
            "DeputyCenterID",
            "SubdivisionManagementID",
            "SectionDepartmentID",
            "MissionLocationID",
            "LastStatusID",
        ]
        self.gender_values = []
        self.skin_color_values = []
        self.religion_values = []
        self.marital_status_values = []
        self.city_value = []
        self.blood_group_value = []
        self.eye_color_value = []
        self.education_level_values = []
        self.field_of_study_values = []
        self.university_values = []
        self.db_manager = db_manager
        self.education_info_tab = []
        self.field_names_education = [
            "NationalCode", "EducationLevelID", "Major", "DegreeLevelID",
            "City", "UniversityID", "GraduationDate", "DegreeTypeID",
            "IserID", "Gerayesh", "GPA", "EmploymentDegreeLevelID", "MilitaryEducation", "MilitaryEducationLocation"
        ]
        self.education_entries = {}


    def create_details_form(self, row_values=None):
        try:
            if not self.details_window or not self.details_window.winfo_exists():
                style = ttk.Style()
                style.configure('TButton', font=('Helvetica', 12), padding=10, background='#f9f3eb', foreground='red')
                style.configure('TLabel', font=('Helvetica', 12), background='#c2b9ad', foreground='red', padding=10)
                style.configure('TEntry', font=('Helvetica', 12), background='#c2b9ad', foreground='red', padding=10)
                style.configure('TCombobox', font=('Helvetica', 12))
                style.configure('TLabelframe', font=('Helvetica', 12))


                self.details_window = tk.Toplevel(self.root)
                # گرفتن مسیر پوشه‌ای که فایل اجرایی در آن قرار دارد
                base_dir = os.path.dirname(os.path.abspath(__file__))
                # مسیر نسبی به فایل عکس
                icon_path = os.path.join(base_dir, "images", "icon.jpg")
                # بارگذاری تصویر
                self.icon_image = PhotoImage(file=icon_path)

                self.details_window.attributes('-topmost', True)  # این پنجره همیشه روی پنجره اصلی قرار می‌گیرد
                window_width = 1050
                window_height = 700
                screen_width = self.details_window.winfo_screenwidth()
                screen_height = self.details_window.winfo_screenheight()
                x = (screen_width // 2) - (window_width // 2)
                y = (screen_height // 2) - (window_height // 2)
                self.details_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
                self.details_window.protocol("WM_DELETE_WINDOW", self.on_close_details_window)

                # ایجاد یک فریم اصلی
                main_frame = tk.Frame(self.details_window, bg='#c2b9ad')
                main_frame.pack(fill=tk.BOTH, expand=True)

                # ایجاد فریم برای اطلاعات (نام، نام خانوادگی و کد ملی)
                self.info_frame = tk.Frame(main_frame, bg='#c2b9ad')
                self.info_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

                # ایجاد فریم برای تب‌ها
                self.notebook = ttk.Notebook(main_frame)
                self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

                # تعریف تب‌های مختلف
                self.tabs_dict = {
                    "مشخصات فردی": tk.Frame(self.notebook, bg='#c2b9ad',width=20),
                    "وضعیت خدمتی": tk.Frame(self.notebook, bg='#c2b9ad',width=20),
                    "تحصیلات": tk.Frame(self.notebook, bg='#c2b9ad',width=20),
                    "ترفیعات": tk.Frame(self.notebook, bg='#c2b9ad',width=20),
                    "سنوات": tk.Frame(self.notebook, bg='#c2b9ad',width=20),
                    "مشاغل": tk.Frame(self.notebook, bg='#c2b9ad',width=20),
                    "ماموریت ها": tk.Frame(self.notebook, bg='#c2b9ad',width=20),
                    "افراد تحت تکفل": tk.Frame(self.notebook, bg='#c2b9ad',width=20),
                    "متفرقه": tk.Frame(self.notebook, bg='#c2b9ad',width=20)
                }

                for tab_name, tab_frame in self.tabs_dict.items():
                    self.notebook.add(tab_frame, text=tab_name)

                if row_values is None or len(row_values) == 0:
                    raise ValueError("مقادیر ردیف خالی یا موجود نیستند.")

                self.national_code = self.validate_national_code(row_values[0])
                self.create_personal_info_tab()
                self.fill_personal_info_tab(self.national_code)
                self.create_employment_info_tab()
                self.fill_employment_info_tab(self.national_code)
                self.create_education_info_tab()
                self.fill_education_info_tab(self.national_code)
                self.create_promotions_info_tab()
                self.fill_promotions_info_tab(self.national_code)
                self.create_sanavat_info_tab()
                self.fill_sanavat_info_tab(self.national_code)
                self.create_job_info_tab()
                self.fill_job_info(self.national_code)
                self.create_missions_info_tab()
                self.fill_missions_info_tab(self.national_code)
                self.create_family_info_tab()
                self.fill_family_info_tab(self.national_code)
                self.create_employee_bank_details_tab()
                self.fill_employee_bank_details_tab(self.national_code)

                # ایجاد فریم برای ذخیره
                self.save_frame = tk.Frame(main_frame, bg='#c2b9ad')
                self.save_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

                # ایجاد دکمه ذخیره
                self.save_button = tk.Button(self.save_frame, text="ذخیره", command=self.save_all_tabs,bg='#9b9184', fg='#1b1a17')
                self.save_button.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)  # فقط یک بار pack

                self.update_info()
                self.details_window.title("مشخصات " + self.firstName + " " + self.lastName)

        except Exception as e:
            logging.error(f"خطا در ایجاد فرم جزئیات: {e}")
            messagebox.showerror("خطا", str(e))

    def on_close_details_window(self):
        """اجرای تابع بازگشتی و بستن پنجره"""
        if self.close_callback:
            self.close_callback()  # فراخوانی تابع در صورت موجود بودن
        self.details_window.destroy()

    def set_close_callback(self, callback):
        """تنظیم تابعی که هنگام بستن پنجره فراخوانی می‌شود"""
        self.close_callback = callback

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # ایجاد یک ورودی تاریخ (شمسی)
        self.date_edit_shamsi = QtWidgets.QDateEdit()
        self.date_edit_shamsi.setCalendarPopup(True)
        self.date_edit_shamsi.setDisplayFormat("yyyy/MM/dd")
        self.date_edit_shamsi.setDate(self.get_current_shamsi_date())

        layout.addWidget(self.date_edit_shamsi)

        # دکمه برای دریافت تاریخ انتخاب شده
        submit_button = QtWidgets.QPushButton("ثبت تاریخ")
        submit_button.clicked.connect(self.submit_date)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        self.show()

    def update_user_info(self):
        self.name_label.config(text=f"نام: {self.user_data['name']}")
        self.surname_label.config(text=f"نام خانوادگی: {self.user_data['surname']}")
        self.national_code_label.config(text=f"کد ملی: {self.user_data['national_code']}")

    def get_current_shamsi_date(self):
        # گرفتن تاریخ جاری به صورت شمسی
        today_shamsi = jdatetime.date.today()
        return QtCore.QDate(today_shamsi.year, today_shamsi.month, today_shamsi.day)

    def submit_date(self):
        # دریافت تاریخ انتخابی و تبدیل آن به تاریخ شمسی
        selected_date = self.date_edit_shamsi.date()
        shamsi_date = jdatetime.date.fromgregorian(
            year=selected_date.year(),
            month=selected_date.month(),
            day=selected_date.day()
        )
        print(f"تاریخ انتخاب شده (شمسی): {shamsi_date}")

    def load_data(self):
        # بارگذاری داده‌ها از پایگاه داده و ذخیره آن‌ها در متغیرها
        self.gender_values = self.db_manager.fetch_gender_values()
        self.skin_color_values = self.db_manager.fetch_skin_color_values()
        self.religion_values = self.db_manager.fetch_religion_values()
        self.marital_status_values = self.db_manager.fetch_marital_status_values()
        self.religion_values = self.db_manager.fetch_religion_values()
        self.eye_color_value = self.db_manager.fetch_eye_color_values()
        self.city_value = self.db_manager.fetch_city_status_values()
        self.blood_group_value = self.db_manager.fetch_blood_group_values()

    def update_table_with_data(self):
        # پاک کردن داده‌های موجود در جدول قبل از افزودن داده‌های جدید
        for item in self.table.get_children():
            self.table.delete(item)

        # بارگذاری داده‌های واقعی از پایگاه داده
        data = self.db_manager.fetch_all("SELECT * FROM PersonalInfo")
        for row in data:
            self.table.insert("", tk.END, values=row)

    def on_table_row_click(self, event, data):
        try:
            #selected_item = self.table.selection()[0]
            #row_values = self.table.item(selected_item, 'values')
            national_code = data[0].strip("('").strip(",")  # حذف '(' و ','

            #national_code = row_values[0]  # فرض می‌کنیم اولین ستون جدول، کد ملی باشد
            #self.get_personal_info_by_national_code(national_code)

        except Exception as e:
            logging.error(f"Error in on_table_row_click: {e}")
            messagebox.showerror("Error", f"Error in on_table_row_click: {e}")

    def validate_national_code(self,row_values):
        """Validate the national code input."""
        # اطمینان از اینکه کد ملی یک رشته است
        if not isinstance(row_values, str):
            national_code = str(row_values)

        # حذف فاصله‌های اضافی
        national_code = row_values.strip()

        # لیست کاراکترهایی که باید حذف شوند
        unwanted_chars = ["'", "(", ")", ","]

        # حذف کاراکترهای ناخواسته و فضای اضافی
        for char in unwanted_chars:
            national_code = national_code.replace(char, "")

        # بررسی طول و صحت کد ملی
        #if len(national_code) != 10 or not national_code.isdigit():
        #    raise ValueError("National code must be exactly 10 digits long and contain only numbers.")

        """Clean the given ID by removing specific unwanted characters."""
        return national_code

    def is_valid_national_code(self, national_code):
        """
        اعتبارسنجی کد ملی ایران
        :param national_code: کد ملی به صورت رشته یا عدد
        :return: True اگر کد ملی معتبر باشد، در غیر این صورت False
        """
        # تبدیل ورودی به رشته و اضافه کردن صفرهای ابتدایی در صورت نیاز
        national_code = str(national_code).zfill(10)

        # بررسی طول کد ملی
        if len(national_code) != 10 or not national_code.isdigit():
            print("طول کد ملی باید ۱۰ رقم باشد و فقط شامل اعداد باشد.")
            return False

        # بررسی یکسان نبودن تمام ارقام (مثل 1111111111)
        if len(set(national_code)) == 1:
            print("کد ملی نمی‌تواند شامل ارقام تکراری (مثل ۱۱۱۱۱۱۱۱۱۱) باشد.")
            return False

        # محاسبه رقم کنترلی
        control_digit = int(national_code[-1])  # آخرین رقم
        checksum = sum(int(national_code[i]) * (10 - i) for i in range(9)) % 11

        # بررسی صحت رقم کنترلی
        if checksum < 2:
            return control_digit == checksum
        else:
            return control_digit == (11 - checksum)

    def get_active_tab(self):
        """بررسی تب فعال و بازگرداندن نام آن."""
        return self.notebook.tab(self.notebook.select(), "text")  # نام تب فعال را برمی‌گرداند

    def update_info(self):
        # ایجاد لیبل‌ها برای نام، نام خانوادگی و کد ملی
        self.name_label = tk.Label(self.info_frame, text=self.firstName,bg='#c2b9ad', fg='#1b1a17')
        self.name_label.pack(side=tk.TOP, padx=5, pady=5)
        self.surname_label = tk.Label(self.info_frame, text=self.lastName,bg='#c2b9ad', fg='#1b1a17')
        self.surname_label.pack(side=tk.TOP, padx=5, pady=5)
        self.national_code_label = tk.Label(self.info_frame, text=self.national_code,bg='#c2b9ad', fg='#1b1a17')
        self.national_code_label.pack(side=tk.TOP, padx=5, pady=5)

        # برچسب نمایش عکس
        self.photo_label = tk.Label(self.info_frame,bg='#c2b9ad', fg='#1b1a17')
        self.photo_label.pack(side=tk.TOP, padx=5, pady=5)

        # بارگذاری عکس بر اساس کد ملی
        self.load_photo(self.national_code)
        # دکمه انتخاب عکس
        self.photo_button = tk.Button(self.info_frame, text="انتخاب عکس", command=self.upload_photo,bg='#9b9184', fg='#1b1a17')
        self.photo_button.pack(side=tk.TOP, padx=5, pady=5)

    def load_photo(self, national_code):
        query = "SELECT PhotoPath FROM PersonalInfo WHERE NationalCode = ?"
        result = self.db_manager.fetch_one(query, (national_code,))

        if result and result[0]:
            self.display_photo(result[0])
        else:
            self.photo_label.config(image='')

    def display_photo(self, file_path):
        img = Image.open(file_path)
        img = img.resize((150, 200), Image.LANCZOS)  # تغییر اندازه با نسبت 3x4
        photo = ImageTk.PhotoImage(img)

        self.photo_label.config(image=photo,bg='#c2b9ad', fg='#1b1a17')
        self.photo_label.image = photo  # برای جلوگیری از پاک شدن عکس در حافظه

    def upload_photo(self):

        national_code = self.national_code

        # استفاده از filedialog.askopenfilename
        file_path = filedialog.askopenfilename(
            title="انتخاب عکس",
            filetypes=[("Image files", "*.jpg;*.png;*.jpeg")]
        )

        if file_path:
            # ذخیره مسیر عکس در پایگاه داده
            query = "UPDATE PersonalInfo SET PhotoPath = ? WHERE NationalCode = ?"
            self.display_photo(file_path)
            self.db_manager.execute_query(query, (file_path, national_code))
            self.db_manager.commit()
            # تغییر سایز و کاهش حجم عکس
            self.resize_and_display_image(file_path)

    def resize_and_display_image(self, file_path):
        # باز کردن عکس با استفاده از PIL
        img = Image.open(file_path)

        # تغییر سایز عکس به 3x4 (300x400 پیکسل)
        img = img.resize((300, 400), Image.LANCZOS)  # تغییر اندازه با نسبت 3x4

        # کاهش حجم عکس (کیفیت 85 درصد)
        compressed_image_path = os.path.join(os.path.dirname(file_path), "compressed_image.jpg")
        img.save(compressed_image_path, quality=85)

        # تبدیل عکس به فرمت قابل استفاده در tkinter
        photo = ImageTk.PhotoImage(img)

        # نمایش عکس در جای قبلی
        self.photo_label.config(image=photo)
        self.photo_label.image = photo  # برای جلوگیری از پاک شدن عکس در حافظه

    def delete_photo(self, national_code):
        # پیدا کردن مسیر عکس از دیتابیس
        query = "SELECT PhotoPath FROM PersonalInfo WHERE NationalCode = ?"
        result = self.db_manager.fetch_one(query, (national_code,))

        if result and result[0] and os.path.exists(result[0]):
            os.remove(result[0])  # حذف فایل عکس از سیستم

        # پاک کردن مسیر عکس از دیتابیس
        query = "UPDATE PersonalInfo SET PhotoPath = NULL WHERE NationalCode = ?"
        self.db_manager.execute(query, (national_code,))
        self.db_manager.commit()

        self.photo_label.config(image='')  # حذف عکس از فرم

    def set_gender_combobox_value(self, gender_id):
        """مقدار ComboBox جنسیت را با توجه به GenderID تنظیم می‌کند."""
        try:
            # تبدیل GenderID به نام جنسیت
            gender_name = self.gender_mapping.get(gender_id, "Unknown")
            print(f"Fetched Gender Name: {gender_name}")  # برای دیباگ

            # تنظیم مقدار در ComboBox
            if hasattr(self, 'gender_combobox'):
                if gender_name in self.gender_combobox['values']:
                    self.gender_combobox.set(gender_name)
                else:
                    print(f"Gender '{gender_name}' not in ComboBox values.")
            else:
                print("gender_combobox not defined.")
        except Exception as e:
            print(f"Error setting gender in ComboBox: {e}")
            messagebox.showerror("Error", f"Error setting gender in ComboBox: {e}")

    def on_row_select(self, event,data):
        try:
            self.create_details_form(data)

        except ValueError as e:
            logging.error(f"Error converting ID to integer: {e}")
            messagebox.showerror("Error", "Invalid ID format selected.")

    def validate_form(self):
        """اعتبارسنجی فیلدهای فرم و بازگشت لیست خطاها."""
        errors = []

        for field, var in self.fields.items():
            valid = True
            entry = self.get_entry_widget_by_field_name(field)

            # بررسی نام و نام خانوادگی که نباید خالی باشند
            if field in ["FirstName", "LastName"] and not var.get():
                errors.append(f"{field} is required.")
                valid = False

            # بررسی فرمت تاریخ تولد
            if field == "BirthDate" and not re.match(r'\d{4}-\d{2}-\d{2}', var.get()):
                errors.append("Birth Date must be in YYYY-MM-DD format.")
                valid = False

            # تنظیم رنگ فیلد بر اساس اعتبارسنجی
            self.set_field_color(entry, valid)

        return errors

    def get_field_index(self, field_name):
        """دریافت ایندکس فیلد با توجه به نام آن."""
        return list(self.fields.keys()).index(field_name)

    def get_entry_widget_by_field_name(self, field_name):
        # تابع برای گرفتن ویجت ورودی مرتبط با هر فیلد
        for widget in self.personal_info_tab.winfo_children():
            if isinstance(widget, tk.Entry) and widget.cget("textvariable") == str(self.fields[field_name]):
                return widget
        return None

    def update_record(self):
        if not self.current_id:
            messagebox.showerror("Error", "No record selected")
            return

        errors = self.validate_form()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        data = {
            "FirstName": self.fields["FirstName"].get(),
            "LastName": self.fields["LastName"].get(),
            "FatherName": self.fields["FatherName"].get(),
            "NickName": self.fields["NickName"].get(),
            "BirthDate": self.fields["BirthDate"].get(),
            "BirthPlace": self.fields["BirthPlace"].get(),
            "IssuePlace": self.fields["IssuePlace"].get(),
            "IssueDate": self.fields["IssueDate"].get(),
            "Gender": self.fields["Gender"].get(),
            "MaritalStatus": self.fields["MaritalStatus"].get(),
            "Height": self.fields["Height"].get(),
            "Weight": self.fields["Weight"].get(),
            "SkinColor": self.fields["SkinColor"].get(),
            "SpecialFeatures": self.fields["SpecialFeatures"].get(),
            "Address": self.fields["Address"].get(),
            "PostalCode": self.fields["PostalCode"].get(),
            "PhoneNumber": self.fields["PhoneNumber"].get(),
            "Mobile": self.fields["Mobile"].get(),
            "Email": self.fields["Email"].get(),
        }

        query = """UPDATE PersonalInfo 
                   SET FirstName = ?, LastName = ?, FatherName = ?, NickName = ?, 
                       BirthDate = ?, BirthPlace = ?, IssuePlace = ?, IssueDate = ?, 
                       Gender = ?, MaritalStatus = ?, Height = ?, Weight = ?, 
                       SkinColor = ?, SpecialFeatures = ?, Address = ?, PostalCode = ?, 
                       PhoneNumber = ?, Mobile = ?, Email = ? 
                   WHERE ID = ?"""
        try:
            self.db_manager.execute_query(query, (*data.values(), self.current_id))
            messagebox.showinfo("Success", "Record updated successfully")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    def clear_tabs(self):
        for tab in self.tabs_dict.values():
            for widget in tab.winfo_children():
                widget.destroy()

    def validate_email(self, entry):
        # الگوی regex برای اعتبارسنجی ایمیل
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if re.match(email_pattern, entry.get()):
            entry.config(bg='white')  # اگر ایمیل معتبر بود
        else:
            entry.config(bg='red')  # اگر ایمیل نامعتبر بود



    def validate_persian_text(self, entry):
        # تنها حروف فارسی
        if re.match(r'^[\u0600-\u06FF\s]*$', entry.get()):
            entry.config(bg='white')  # اگر درست بود رنگ سفید
        else:
            entry.config(bg='red')  # اگر اشتباه بود رنگ قرمز

    def validate_Weight(self, entry):
        weight = entry.get()
        if self.is_valid_Weight(weight):
            entry.config(bg='white')  # اگر مقدار معتبر بود
        else:
            entry.config(bg='red')  # اگر مقدار نامعتبر بود

    def is_valid_Weight(self, weight):
        # بررسی اینکه ورودی فقط عدد باشد و قد در محدوده منطقی باشد (مثلاً بین 50 و 250 سانتی‌متر)
        if weight.isdigit() and 50 <= int(weight) <= 150 and(weight.isdigit() or weight == ""):
            return True
        return False

    def validate_height(self, entry):

        height = entry.get()
        if self.is_valid_height(height):
            entry.config(bg='white')  # اگر مقدار معتبر بود
        else:
            entry.config(bg='red')  # اگر مقدار نامعتبر بود

    def is_valid_phone(self, Phone):
        # بررسی اینکه ورودی فقط شامل ارقام باشد و حداکثر 11 کاراکتر باشد
        if Phone.isdigit() and len(Phone) <= 11:
            return True
        elif Phone == "":  # اجازه به فیلد خالی
            return True
        return False

    def check_phone_number(self, entry):
        phone_number = entry.get()  # دریافت مقدار وارد شده در فیلد Entry

        # بررسی اینکه شماره تلفن معتبر باشد (دارای 11 رقم)
        if len(phone_number) == 11 and phone_number.isdigit():
            entry.config(bg="white")  # بازگرداندن رنگ پس‌زمینه به حالت عادی
        else:
            entry.config(bg="red")  # تغییر رنگ پس‌زمینه به قرمز در صورت نامعتبر بودن

    def is_valid_height(self, height):
        # بررسی اینکه ورودی فقط عدد باشد و قد در محدوده منطقی باشد (مثلاً بین 50 و 250 سانتی‌متر)
        if height.isdigit() and 50 <= int(height) <= 250  and (height.isdigit() or height == ""):
            return True
        return False


    def set_combobox_default_value(self, combo, display_value):
        """
        تابع برای تنظیم مقدار پیش‌فرض در کمبوباکس
        :param combo: کمبوباکس Tkinter
        :param display_value: مقدار نمایشی (Display Value) برای نمایش به کاربر
        """
        try:
            # ابتدا بررسی می‌کنیم که آیا مقدار نمایش (Display Value) در مقادیر کمبوباکس موجود است
            if display_value in combo['values']:
                combo.set(display_value)
            else:
                # اگر Display Value در مقادیر نبود، کمبوباکس را به مقدار پیش‌فرض "نامشخص" تنظیم می‌کنیم
                print(f"Error: {display_value} is not a valid option for Combobox.")
                combo.set("نامشخص")
        except Exception as e:
            print(f"Error setting default value in Combobox: {e}")

    def create_employment_info_tab(self):
        # ایجاد تب "وضعیت خدمتی"
        self.employee_info_tab = self.tabs_dict["وضعیت خدمتی"]
        self.employee_fields = {}

        # برچسب‌ها و نام فیلدها
        labels = [
            "کد ملی:", "کد پایگاهی:", "وضعیت استخدامی:", "برابر قانون استخدامی:",
            "رسته یا تخصص:", "محل خدمت:", "نقش صف یا ستاد:", "نوع عضویت اولیه:",
            "واحد استخدام کننده:", "نوع عضویت فعلی:", "آخرین وضعیت خدمتی:",
            "تاریخ ورود یا انتقال:", "استان:", "شهرستان:", "سازمان:",
            "معاونت یا گروه/مرکز:", "مدیریت زیر مجموعه:", "دایره یا قسمت:",
            "محل ماموریت:", "وضعیت فعلی:"
        ]

        # ایجاد ویجت‌ها
        for i, (label_text, field_name) in enumerate(zip(labels, self.field_names_employee)):
            label = tk.Label(self.employee_info_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17')
            label.grid(row=i, column=0, sticky=tk.W)

            if field_name == "NationalCode":
                # کد ملی فقط خواندنی
                entry = tk.Entry(self.employee_info_tab, width=24)
                entry.insert(0, self.national_code)
                entry.config(state=tk.DISABLED)
                self.employee_fields[field_name] = entry

            elif field_name == "EntryTransferDate":
                # فیلد تاریخ ورود یا انتقال با دکمه انتخاب تاریخ
                entry = tk.Entry(self.employee_info_tab, width=24)
                self.employee_fields[field_name] = entry
                # دکمه انتخاب تاریخ
                calendar_button = tk.Button(
                    self.employee_info_tab,
                    text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                    command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2)
                )
                calendar_button.grid(row=i, column=2)
            elif "ID" in field_name or "BaseCode":
                # فیلدهایی با شناسه (ID) دارای کومبوباکس
                entry = ttk.Combobox(self.employee_info_tab, width=20)
                entry.grid(row=i, column=1)
                self.load_combobox_data_employment(entry, field_name)
                self.employee_fields[field_name] = entry
            else:
                # سایر فیلدها با ورودی عمومی
                entry = tk.Entry(self.employee_info_tab, width=24)
                self.employee_fields[field_name] = entry
            entry.grid(row=i, column=1)

    def fill_employment_info_tab(self, national_code):
        try:
            query = "SELECT * FROM EmploymentInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            if not result:
                logging.warning(f"No results found for NationalCode: {national_code}")
                return

            for field_name, widget in self.employee_fields.items():
                field_index = self.field_names_employee.index(field_name)
                data_dict = getattr(self, f"{field_name}_data_dict", {})

                # بررسی و تنظیم مقدار db_value
                try:
                    db_value = result[field_index+1] if len(result) > field_index+1 else None
                except IndexError:
                    db_value = None

                # if field_name == "NationalCode":
                #     if db_value is None:
                #         db_value = ""  # مقدار پیش‌فرض اگر db_value تهی است
                #     elif isinstance(db_value, str) and db_value.isdigit():
                #         db_value = int(db_value)  # تبدیل به عدد در صورتی که از نوع رشته و قابل تبدیل باشد
                #     widget.delete(0, tk.END)
                #     widget.insert(0, db_value)

                if isinstance(widget, ttk.Combobox):
                    widget['values'] = list(data_dict.values())
                    display_value = data_dict.get(db_value, "نامشخص")
                    if display_value in widget['values']:
                        widget.set(display_value)
                    else:
                        widget.set("نامشخص")
                    logging.info(
                        f"{field_name} - db_value: {db_value}, data_dict: {data_dict}, display_value: {display_value}")

                elif isinstance(widget, tk.Entry):
                    if field_name in "NationalCode":
                        continue
                    widget.delete(0, tk.END)
                    widget.insert(0, db_value if db_value is not None else "")


        except Exception as e:
            logging.error(f"Error in fill_employment_info_tab: {e}")
            messagebox.showerror("خطا", "خطایی در بارگذاری اطلاعات رخ داد.")

    def load_combobox_data_employment(self, combobox, field_name):
        # دیکشنری برای نگهداری IDها و مقادیر
        data_dict = {}

        # نقشه‌گذاری کوئری‌ها برای فیلدهای Employee
        queries = {
            "EmploymentStatusID": "SELECT * FROM EmploymentStatus ",
            "LawBasedEmploymentID": "SELECT * FROM LawBasedEmployment WHERE LawBasedEmploymentID IS NOT NULL AND LawBasedEmploymentID <> ''",
            "ExpertiseID": "SELECT * FROM Expertise WHERE ExpertiseID IS NOT NULL AND ExpertiseName <> ''",
            "ServiceLocationID": "SELECT ServiceLocationID, ServiceLocationName FROM ServiceLocation WHERE ServiceLocationName IS NOT NULL AND ServiceLocationName <> ''",
            "InitialMembershipTypeID": "SELECT InitialMembershipTypeID, MembershipTypeName FROM InitialMembershipType WHERE MembershipTypeName IS NOT NULL AND MembershipTypeName <> ''",
            "HiringUnitID": "SELECT * FROM HiringUnit WHERE HiringUnitName IS NOT NULL AND HiringUnitName <> ''",
            "CurrentMembershipTypeID": "SELECT *  FROM CurrentMembershipType WHERE CurrentMembershipTypeName IS NOT NULL AND CurrentMembershipTypeName <> ''",
            "LatestServiceStatusID": "SELECT * FROM LatestServiceStatus WHERE LatestServiceStatusID IS NOT NULL AND LatestServiceStatusID <> ''",
            "StateID": "SELECT *  FROM State WHERE StateName IS NOT NULL AND StateName <> ''",
            "CountyID": "SELECT *  FROM County WHERE CountyID IS NOT NULL AND CountyID <> ''",
            "OrganizationID": "SELECT *  FROM Organization WHERE OrganizationName IS NOT NULL AND OrganizationName <> ''",
            "DeputyCenterID": "SELECT * FROM DeputyCenter WHERE DeputyCenterName IS NOT NULL AND DeputyCenterName <> ''",
            "SubdivisionManagementID": "SELECT * FROM SubdivisionManagement WHERE ManagementName IS NOT NULL AND ManagementName <> ''",
            "SectionDepartmentID": "SELECT * FROM SectionDepartment WHERE DepartmentName IS NOT NULL AND DepartmentName <> ''",
            "MissionLocationID": "SELECT CityID, CityName FROM City WHERE CityName IS NOT NULL AND CityName <> ''",
            "OperationalSupportRoleID": "SELECT * FROM OperationalSupportRole",
            "BaseCode": "SELECT * FROM BaseCode WHERE BaseCode IS NOT NULL AND BaseCode <> ''",
            "LastStatusID": "SELECT * FROM LastStatus WHERE LastStatusID <> ''",
        }

        # بارگذاری داده‌ها بر اساس فیلد
        query = queries.get(field_name)
        if not query:
            return  # اگر کوئری موجود نباشد، نیازی به بارگذاری نیست

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

    def set_combobox_default_valfue(combo, values, display_values, default_display_value):
        """
        تابع برای تنظیم مقدار پیش‌فرض در کمبوباکس
        :param combo: کمبوباکس Tkinter
        :param values: لیست مقادیر واقعی (Value) برای ذخیره‌سازی در پایگاه داده
        :param display_values: لیست مقادیر نمایشی (Display Value) برای نمایش به کاربر
        :param default_display_value: مقدار پیش‌فرض برای نمایش به کاربر
        """
        # پیدا کردن ایندکس مقدار پیش‌فرض در لیست مقادیر نمایشی
        if default_display_value in display_values:
            default_index = display_values.index(default_display_value)
            # تنظیم مقدار پیش‌فرض بر اساس مقدار نمایشی
            combo.set(display_values[default_index])
            # تنظیم مقدار واقعی در صورت نیاز (برای ذخیره‌سازی)
            selected_value = values[default_index]
            print(f"Selected Display Value: {display_values[default_index]}")
            print(f"Selected Actual Value (for DB): {selected_value}")
        else:
            print("Default display value not found in display values.")

    def load_combobox_data_personal(self, combobox, field_name):
        try:
            # برای هر شناسه، کوئری مناسب را اجرا کنید
            if field_name == "GenderID":
                query = "SELECT GenderID, Gender FROM Gender"
            elif field_name == "MaritalStatusID":
                query = "SELECT MaritalStatusID, MaritalStatus FROM MaritalStatus"
            elif field_name == "ReligionID":
                query = "SELECT ReligionID, Religion FROM Religion"
            elif field_name == "BloodGroupID":
                query = "SELECT BloodGroupID, BloodGroup FROM BloodGroup"
            elif field_name == "EyeColorID":
                query = "SELECT EyeColorID, EyeColor FROM EyeColor"
            elif field_name == "SkinColorID":
                query = "SELECT SkinColourID, SkinColour FROM SkinColour"
            elif field_name == "BirthPlaceID":
                query = "SELECT CityID, CityName FROM City"
            elif field_name == "IssuePlaceID":
                query = "SELECT CityID, CityName FROM City"
            else:
                return  # اگر شناسه ناشناخته بود، تابع را ترک کنید
            data_dict = {}
            try:
                results = self.db_manager.fetch_all(query)  # فرض بر این است که متدی برای دریافت تمام داده‌ها دارید
                values = [row[1] for row in results]  # نام و ID را به صورت ترکیبی نمایش دهید
                for row in results:
                    data_dict[row[0]] = row[1]  # ذخیره ID و نام در دیکشنری
                combobox['values'] = values
                combobox['state'] = 'readonly'  # تنظیم combobox به حالت readonly
                if values:
                    combobox.current(0)  # انتخاب اولین مقدار به عنوان مقدار پیش‌فرض

                # ذخیره دیکشنری به عنوان یک ویژگی کلاس
                setattr(self, f"{field_name}_data_dict", data_dict)

            except Exception as e:
                logging.error(f"Error loading {field_name} data: {e}")

        except Exception as e:
            logging.error(f"Error loading combobox data for {field_name}: {e}")
            print(f"Error loading combobox data for {field_name}: {e}")

    def validate_numeric_input(self, new_value):
        # فقط اعداد پذیرفته شود و همچنین امکان خالی بودن فیلد وجود داشته باشد
        if new_value.isdigit() or new_value == "":
            return True
        return False

    def save_selected_value(self, combobox, field_name):
        # گرفتن مقدار انتخاب شده از کومبو باکس
        selected_name = combobox.get()

        # تبدیل نام انتخاب شده به ID مربوطه
        selected_id = self.combobox_data[field_name].get(selected_name)

        return selected_id  # بازگرداندن شناسه مربوطه

    def show_mission_form(self):
        # باز کردن فرم ماموریت با ایجاد یک پنجره جدید
        mission_window = tk.Toplevel(self.root)
        MissionForm(mission_window, self.db_manager, national_code=self.missions_fields["NationalCode"].get())

    def create_personal_info_tab(self):
        # ساخت تب جدید برای نمایش اطلاعات شخصی
        self.personal_info_tab = self.tabs_dict["مشخصات فردی"]
        # دیکشنری برای نگه‌داری ورودی‌های هر فیلد
        self.personal_fields = {}
        # برچسب‌ها و ورودی‌های فیلدهای اطلاعات شخصی
        labels = [
            "کد ملی:", "نام:", "نام خانوادگی:", "نام پدر:", "نام مستعار:", "تاریخ تولد:",
            "محل تولد:", "محل صدور:", "تاریخ صدور:", "جنسیت:", "وضعیت تاهل:", "مذهب:",
            "گروه خونی:", "قد:", "وزن:", "رنگ چشم:", "رنگ پوست:", "ویژگی‌های خاص:",
            "آدرس:", "کد پستی:", "شماره تلفن:", "شماره موبایل:", "ایمیل:", "شماره شناسایی:"
        ]

        # ایجاد برچسب‌ها و ورودی‌ها در تب
        for i, (label_text, field_name) in enumerate(zip(labels, self.field_names_personal)):
            label = tk.Label(self.personal_info_tab, text=label_text,bg='#c2b9ad', fg='#1b1a17')
            label.grid(row=i, column=0, sticky=tk.W)
            if field_name in ["GenderID", "MaritalStatusID", "ReligionID", "BloodGroupID", "EyeColorID",
                                "SkinColorID", "BirthPlaceID", "IssuePlaceID"]:
                entry = ttk.Combobox(self.personal_info_tab)
                self.load_combobox_data_personal(entry, field_name)
                self.personal_fields[field_name] = entry  # ذخیره Combobox به جای Entry
            elif field_name in ["Height"]:
                entry = tk.Entry(self.personal_info_tab,width=24)
                entry.bind('<KeyRelease>', lambda event, ent=entry: self.validate_height(ent))
                self.personal_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
            elif field_name in ["Weight"]:
                entry = tk.Entry(self.personal_info_tab, width=24)
                entry.bind('<KeyRelease>', lambda event, ent=entry: self.validate_Weight(ent))
                self.personal_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
            # برای فیلد تاریخ تولد و تاریخ صدور
            elif field_name in ["IssueDate","BirthDate"]:
                entry = tk.Entry(self.personal_info_tab,width=24)
                self.personal_fields[field_name] = entry
                calendar_button = tk.Button(
                    self.personal_info_tab,
                    text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                    command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2)
                )
                calendar_button.grid(row=i, column=2)
            # استفاده از Combobox برای فیلدهای مشخص
            elif field_name in ["FirstName", "LastName", "FatherName", "NickName"]:
                entry = tk.Entry(self.personal_info_tab,width=24)
                entry.bind('<KeyRelease>', lambda event, ent=entry: self.validate_persian_text(ent))
                self.personal_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
            elif field_name in ["Address", "SpecialFeatures"]:
                # فریم برای مدیریت چیدمان (با grid)
                entry = tk.Frame(self.personal_info_tab)
                entry.grid(row=i, column=1, sticky="w")

                # ساخت ویجت Text
                text_widget = tk.Text(entry, wrap="none", height=3, width=16)
                text_widget.grid(row=0, column=0, sticky="w")

                # اضافه کردن اسکرول‌بار عمودی
                scroll_y = tk.Scrollbar(entry, orient="vertical", command=text_widget.yview)
                scroll_y.grid(row=0, column=1, sticky="ns")

                # اتصال اسکرول‌بار عمودی به ویجت Text
                text_widget.config(yscrollcommand=scroll_y.set)

                # ذخیره ویجت Text
                self.personal_fields[field_name] = text_widget
            elif field_name in ["NationalCode"]:
                entry = tk.Entry(self.personal_info_tab,width=24)
                self.personal_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
                entry.bind('<KeyRelease>', lambda event, ent=entry: self.check_national_code(ent))
                entry.insert(0, self.national_code)
            elif field_name in ["Email"]:
                entry = tk.Entry(self.personal_info_tab,width=24)
                self.personal_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
                entry.bind('<KeyRelease>', lambda event, ent=entry: self.validate_email(ent))
            elif field_name in ["PhoneNumber","Mobile"]:
                entry = tk.Entry(self.personal_info_tab,width=24)
                self.personal_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
                entry.bind('<KeyRelease>', lambda event, ent=entry: self.check_phone_number(ent))
            else:
                entry = tk.Entry(self.personal_info_tab,width=24)
                self.personal_fields[field_name] = entry  # ذخیره Entry در فیلدهای دیگر
            entry.grid(row=i, column=1)

    def fill_personal_info_tab(self, national_code):
        if not hasattr(self, 'personal_fields'):
            print("Error: personal_fields is not defined.")
            return

        try:
            # اجرای کوئری برای دریافت اطلاعات شخصی
            query = "SELECT * FROM PersonalInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            if not result:
                print(f"Fill Error: No personal info found for the given National Code: {national_code}.")
                return

            for field_name in list(self.personal_fields.keys()):
                widget = self.personal_fields[field_name]
                field_index = self.field_names_personal.index(field_name)
                entry_value = result[field_index + 1] if result[field_index + 1] is not None else ""
                if field_name in ["FirstName"]:
                  self.firstName = entry_value
                if field_name in ["LastName"]:
                  self.lastName = entry_value
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
            logging.error(f"Fill Error: Error fetching personal info: {e}")
            print(f"Fill Error: Database Error: {e}")

    def create_missions_info_tab(self):
        # ساخت تب جدید برای نمایش اطلاعات خدمت نظامی
        self.military_service_info_tab = self.tabs_dict["ماموریت ها"]
        # دیکشنری برای نگه‌داری ورودی‌های هر فیلد
        self.missions_fields = {}
        # فیلدهای اطلاعات خدمت نظامی
        labels = [
            "کد ملی:",  # National Code
            "مدت خدمت رسمی:",  # Official Service Duration
            "مدت حضور از جبهه:",  # Front Line Duration
            "مدت خدمت بسیجی:"  # Basij Service Duration
        ]
        field_names = [
            "NationalCode",  # کد ملی
            "OfficialServiceDuration",  # مدت خدمت رسمی
            "FrontLineDuration",  # مدت حضور از جبهه
            "BasijServiceDuration"  # مدت خدمت بسیجی
        ]

        # ایجاد ردیف‌های داده
        for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
            # ایجاد برچسب برای هر فیلد
            label = tk.Label(self.military_service_info_tab, text=label_text,bg='#c2b9ad', fg='#1b1a17')
            label.grid(row=i + 1, column=0, sticky=tk.W)

            # ایجاد ورودی برای هر فیلد
            if field_name == "NationalCode":
                entry = tk.Entry(self.military_service_info_tab,width=24)
                entry.insert(0, self.national_code)
                entry.config(state="disabled")

            else:
                entry = tk.Entry(self.military_service_info_tab, validate="key",width=24)
                entry['validatecommand'] = (self.root.register(self.validate_numeric_input), '%P')
            entry.grid(row=i + 1, column=1)
            # اضافه کردن ورودی‌ها به دیکشنری
            self.missions_fields[field_name] = entry
        mission_button = tk.Button(self.military_service_info_tab, text="نمایش ماموریت", command=self.show_mission_form)
        mission_button.grid(row=7, column=0)  # استفاده از grid در فریم تب ماموریت‌ها

    def fill_missions_info_tab(self, national_code):
        try:
            # اجرای کوئری با پارامتر کد ملی
            query = "SELECT * FROM Missions WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if not result:
                print(f"No missions info found for the given National Code: {national_code}.")
                return

            # پر کردن فیلدها با داده‌های دریافتی از پایگاه داده
            field_names = [
                "NationalCode",  # کد ملی
                "OfficialServiceDuration",  # مدت خدمت رسمی
                "FrontLineDuration",  # مدت حضور از جبهه
                "BasijServiceDuration"  # مدت خدمت بسیجی
            ]

            # پر کردن ورودی‌های هر فیلد با داده‌های مربوطه
            for i, field_name in enumerate(field_names):
                entry = self.missions_fields.get(field_name)
                if entry:
                    entry_value = result[i+1] if result[i+1] is not None else ""  # i+1 چون اولین مقدار ID است
                    entry.delete(0, tk.END)  # پاک کردن ورودی قبلی
                    entry.insert(0, entry_value)  # قرار دادن مقدار جدید
                    if field_name == "NationalCode":
                        entry.config(state='disabled')  # غیرفعال کردن فیلد کد ملی

        except Exception as e:
            logging.error(f"Error fetching Military Service info: {e}")
            print(f"Database Error: {e}")

    def create_sanavat_info_tabd(self):
        self.sanavat_info_tab = self.tabs_dict["سنوات"]
        self.sanavat_fields = {}

        labels = [
            "کد ملی:",  # NationalCode
            "تاریخ استخدام اولیه:",  # HireDateFirst
            "تاریخ استخدام رسمی:",  # HireDateOfficial
            "تاریخ استخدام خرید خدمت:",  # HireDatePurchaseService
            "تاریخ بازنشستگی:",  # TerminationDate
            # سایر فیلدها...
        ]

        self.field_names_sanavat = [
            "NationalCode",
            "HireDateFirst",
            "HireDateOfficial",
            "HireDatePurchaseService",
            "TerminationDate",
            # سایر فیلدها...
        ]

        for i, (label_text, field_name) in enumerate(zip(labels, self.field_names_sanavat)):
            label = tk.Label(self.sanavat_info_tab, text=label_text,bg='#c2b9ad', fg='#1b1a17')
            label.grid(row=i, column=0, sticky=tk.W)

            if field_name == "NationalCode":
                entry = tk.Entry(self.sanavat_info_tab,width=24)  # غیرفعال کردن فیلد کد ملی
            else:
                entry = tk.Entry(self.sanavat_info_tab,width=24)

                if field_name in ["TerminationDate"]:
                    entry = tk.Entry(self.sanavat_info_tab, width=24)
                    entry.grid(row=i, column=1)

                    self.sanavat_fields[field_name] = entry
                    calendar_button = tk.Button(self.sanavat_info_tab, text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                                                command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2))
                    calendar_button.grid(row=i, column=2)

                if field_name in ["HireDateFirst"]:
                    entry = tk.Entry(self.sanavat_info_tab, width=24)
                    entry.grid(row=i, column=1)

                    self.sanavat_fields[field_name] = entry
                    calendar_button = tk.Button(self.sanavat_info_tab, text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                                                command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2))
                    calendar_button.grid(row=i, column=2)

                if field_name in ["HireDateOfficial"]:
                    entry = tk.Entry(self.sanavat_info_tab, width=24)
                    entry.grid(row=i, column=1)

                    self.sanavat_fields[field_name] = entry
                    calendar_button = tk.Button(self.sanavat_info_tab, text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                                                command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2))
                    calendar_button.grid(row=i, column=2)

                if field_name in ["HireDatePurchaseService"]:
                    entry = tk.Entry(self.sanavat_info_tab, width=24)
                    entry.grid(row=i, column=1)

                    self.sanavat_fields[field_name] = entry
                    calendar_button = tk.Button(self.sanavat_info_tab, text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                                                command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2))
                    calendar_button.grid(row=i, column=2)


            entry.grid(row=i, column=1)
            self.sanavat_fields[field_name] = entry  # ذخیره ورودی‌ها

        file_button = tk.Button(self.sanavat_info_tab, text="پرونده", command=self.open_SeniorityForm)
        file_button.grid(row=len(labels), column=1, pady=10)  # موقعیت قرارگیری دکمه را مطابق نیاز خود تنظیم کنید

    def create_sanavat_info_tab(self):
        self.sanavat_info_tab = self.tabs_dict["سنوات"]
        self.sanavat_fields = {}

        # لیبل‌ها و نام فیلدها
        labels = [
            "کد ملی:",  # NationalCode
            "تاریخ استخدام اولیه:",  # HireDateFirst
            "تاریخ استخدام رسمی:",  # HireDateOfficial
            "تاریخ استخدام خرید خدمت:",  # HireDatePurchaseService
            "تاریخ بازنشستگی:",  # TerminationDate
        ]

        self.field_names_sanavat = [
            "NationalCode",
            "HireDateFirst",
            "HireDateOfficial",
            "HireDatePurchaseService",
            "TerminationDate",
        ]

        # ایجاد لیبل‌ها، ورودی‌ها و دکمه‌ها
        for i, (label_text, field_name) in enumerate(zip(labels, self.field_names_sanavat)):
            # افزودن لیبل
            label = tk.Label(self.sanavat_info_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17')
            label.grid(row=i, column=0, sticky=tk.W)

            # افزودن ورودی
            entry = tk.Entry(self.sanavat_info_tab, width=24)
            entry.grid(row=i, column=1)
            self.sanavat_fields[field_name] = entry
            if field_name in "NationalCode":
                entry.insert(0, self.national_code)
                entry.config(state='disabled')

            # افزودن دکمه انتخاب تاریخ برای فیلدهای تاریخ
            if field_name in ["HireDateFirst", "HireDateOfficial", "HireDatePurchaseService", "TerminationDate"]:
                calendar_button = tk.Button(
                    self.sanavat_info_tab, text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                    #command=lambda ent=entry: self.open_calendar(ent)  # ارسال ورودی به تابع
                    command = lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2)

                )
                if field_name in ["HireDateFirst", "HireDateOfficial", "HireDatePurchaseService", "TerminationDate"]:
                    self.tarikh_estekhdam =entry
                calendar_button.grid(row=i, column=2)
            elif field_name in "NationalCode":
                entry.insert(0, self.national_code)
                entry.config(state='disabled')
        # افزودن دکمه پرونده
        file_button = tk.Button(self.sanavat_info_tab, text="پرونده", command=self.open_SeniorityForm)
        file_button.grid(row=len(labels), column=1, pady=10)  # موقعیت دکمه را تنظیم کنید

    def open_SeniorityForm(self):
        try:
            # دریافت کد ملی از فیلد مربوطه
            national_code = self.field_names_promotion["NationalCode"].get()
            # بررسی اینکه کد ملی وارد شده باشد
            if not national_code:
                messagebox.showerror("خطا", "لطفاً کد ملی را وارد کنید.")
                return

            # ایجاد پنجره جدید
            SeniorityForm(self.root, self.db_manager,self.national_code)  # ارسال کد ملی به کلاس RewardDisciplinary

            # تنظیمات پنجره جدید

        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")

    def fill_sanavat_info_tab(self, national_code):
        try:
            # اجرای کوئری با پارامتر کد ملی برای دریافت اطلاعات سنوات
            query = "SELECT * FROM SanavatInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if not result:
                print(f"No Sanavat info found for the given National Code: {national_code}.")
                return

            # تنظیم مقادیر فیلدهای سنوات با استفاده از نتیجه کوئری
            for field_name, entry in self.sanavat_fields.items():
                # استفاده از ایندکس صحیح برای هر فیلد
                field_index = self.field_names_sanavat.index(field_name)
                entry_value = result[field_index + 1] if result[field_index + 1] is not None else ""
                entry.delete(0, tk.END)  # پاک کردن مقدار قبلی
                entry.insert(0, entry_value)  # قرار دادن مقدار جدید
                if field_name in "NationalCode":
                    entry.config(state='normal')
        except Exception as e:
            logging.error(f"Error fetching Sanavat info: {e}")
            print(f"Database Error: {e}")


    def create_education_info_tab(self):
        # ایجاد تب "تحصیلات"
        self.education_info_tab = self.tabs_dict["تحصیلات"]
        self.education_fields = {}

        # برچسب‌ها و نام فیلدها
        labels = [
            "کد ملی:", "سطح تحصیلات:", "رشته:", "مقطع تحصیلی:", "شهر:",
            "دانشگاه:", "تاریخ فارغ‌التحصیلی:", "نوع مدرک:", "کد کاربری:",
            "گرایش:", "معدل:", "سطح مدرک شغلی:", "تحصیلات نظامی:", "محل تحصیلات نظامی:"
        ]

        # ایجاد ویجت‌ها
        for i, (label_text, field_name) in enumerate(zip(labels, self.field_names_education)):
            label = tk.Label(self.education_info_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17')
            label.grid(row=i, column=0, sticky=tk.W)

            if field_name == "NationalCode":
                # کد ملی فقط خواندنی
                entry = tk.Entry(self.education_info_tab, width=24)
                entry.insert(0, self.national_code)
                entry.config(state=tk.DISABLED)
                self.education_fields[field_name] = entry

            elif field_name == "GraduationDate":
                # فیلد تاریخ با دکمه انتخاب تاریخ
                entry = tk.Entry(self.education_info_tab, width=24)
                self.education_fields[field_name] = entry
                calendar_button = tk.Button(
                    self.education_info_tab,
                    text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                    command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2)
                )
                calendar_button.grid(row=i, column=2)
            elif "ID" in field_name:
                # فیلدهایی با شناسه (ID) دارای کومبوباکس
                entry = ttk.Combobox(self.education_info_tab, width=20)
                entry.grid(row=i, column=1)
                self.load_combobox_data_education(entry, field_name)
                self.education_fields[field_name] = entry
            else:
                # سایر فیلدها با ورودی عمومی
                entry = tk.Entry(self.education_info_tab, width=24)
                self.education_fields[field_name] = entry
            entry.grid(row=i, column=1)
            # افزودن دکمه "پرونده"
            file_button_military = tk.Button(
                self.education_info_tab, text="پرونده تحصیلات نظامی",
                command=self.Militaryfile, bg='#9b9184', fg='#1b1a17'
            )
            file_button_military.grid(row=len(labels), column=1, pady=10)

            file_button_classic = tk.Button(
                self.education_info_tab, text="پرونده تحصیلات  غیر نظامی",
                command=self.ClassicFile, bg='#9b9184', fg='#1b1a17'
            )
            file_button_classic.grid(row=len(labels), column=2, pady=10)

            file_button_languages = tk.Button(
                self.education_info_tab, text="زبان های خارجی",
                command=self.Languagefile, bg='#9b9184', fg='#1b1a17'
            )
            file_button_languages.grid(row=len(labels), column=4, pady=10)

    def fill_education_info_tab(self, national_code):
        try:
            query = "SELECT * FROM EducationInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            if not result:
                logging.warning(f"No results found for NationalCode: {national_code}")
                return

            for field_name, widget in self.education_fields.items():
                field_index = self.field_names_education.index(field_name)
                data_dict = getattr(self, f"{field_name}_data_dict", {})

                try:
                    db_value = result[field_index + 1] if len(result) > field_index + 1 else None
                except IndexError:
                    db_value = None

                if isinstance(widget, ttk.Combobox):
                    widget['values'] = list(data_dict.values())
                    display_value = data_dict.get(db_value, "نامشخص")
                    if display_value in widget['values']:
                        widget.set(display_value)
                    else:
                        widget.set("نامشخص")

                elif isinstance(widget, tk.Entry):
                    if field_name == "NationalCode":
                        continue
                    widget.delete(0, tk.END)
                    widget.insert(0, db_value if db_value is not None else "")

        except Exception as e:
            logging.error(f"Error in fill_education_info_tab: {e}")
            messagebox.showerror("خطا", "خطایی در بارگذاری اطلاعات رخ داد.")

    def load_combobox_data_education(self, combobox, field_name):
        data_dict = {}

        # نقشه‌گذاری کوئری‌ها برای فیلدهای Education
        queries = {
            "EducationLevelID": "SELECT * FROM EducationLevel WHERE EducationLevel IS NOT NULL",
            "DegreeLevelID": "SELECT * FROM DegreeLevel WHERE DegreeLevel IS NOT NULL",
            "UniversityID": "SELECT * FROM University WHERE UniversityName IS NOT NULL",
            "DegreeTypeID": "SELECT * FROM DegreeType WHERE DegreeTypeName IS NOT NULL",
            "EmploymentDegreeLevelID": "SELECT * FROM EmploymentDegreeLevel WHERE EmploymentDegreeLevelName IS NOT NULL",
        }

        query = queries.get(field_name)
        if not query:
            return

        try:
            results = self.db_manager.fetch_all(query)
            values = [row[1] for row in results if row[1]]
            for row in results:
                if row[1]:
                    data_dict[row[0]] = row[1]

            combobox['values'] = values
            combobox['state'] = 'readonly'
            if values:
                combobox.current(0)
            setattr(self, f"{field_name}_data_dict", data_dict)

        except Exception as e:
            logging.error(f"Error loading {field_name} data: {e}")
            messagebox.showerror("Error", f"Failed to load {field_name} data. Please try again.")

    def check_grade(self, grade):
        try:
            # تبدیل مقدار به عدد اعشاری
            grade_value = float(grade)

            # بررسی اینکه عدد بین 0 و 20 باشد
            if 0 <= grade_value <= 20:
                # اگر رشته نمره شامل اعشار است
                if '.' in grade:
                    decimal_part = grade.split('.')[1]
                    # بررسی اینکه تعداد ارقام بعد از اعشار بیشتر از دو نباشد
                    if len(decimal_part) > 2:
                        return False
                return True  # نمره معتبر است
            else:
                return False
        except (ValueError, IndexError):
            # اگر نتوانست مقدار را به عدد تبدیل کند یا فرمت نادرست بود
            return False

    def validate_grade(self, entry):
        grade_value = entry.get()  # دریافت مقدار از Entry
        if self.check_grade(grade_value):
            entry.config(bg='white')  # اگر نمره معتبر بود، رنگ سفید شود
        else:
            entry.config(bg='red')  # اگر نمره نامعتبر بود، رنگ قرمز شود

    def check_national_code(self, entry):
        national_code = entry.get()
        if self.is_valid_national_code(national_code):
            entry.config(bg='white')  # اگر مقدار معتبر بود
        else:
            entry.config(bg='red')  # اگر مقدار نامعتبر بود

    def validate_numeric_input(self, new_value):
        # فقط اعداد پذیرفته شود و همچنین امکان خالی بودن فیلد وجود داشته باشد
        if new_value.isdigit() or new_value == "":
            return True
        return False

    def create_family_info_tab(self):
        try:
            self.family_info_tab = self.tabs_dict["افراد تحت تکفل"]
            self.family_fields = {}

            labels = [
                "کد ملی سرپرست:",  # National Code
                "تاریخ ازدواج:",  # Marriage Date
                "تعداد کل عائله:",  # Total Dependents
                "تعداد کل فرزندان:",  # Total Children
                "تعداد فرزند دختر:",  # Total Daughters
                "تعداد فرزند پسر:"  # Total Sons
            ]

            field_names = [
                "NationalCode",  # کد ملی
                "LatestMarriageDate",  # تاریخ ازدواج
                "TotalDependents",  # تعداد کل عائله
                "TotalChildren",  # تعداد کل فرزندان
                "TotalDaughters",  # تعداد فرزند دختر
                "TotalSons"  # تعداد فرزند پسر
            ]

            for i, (label_text, field_name) in enumerate(zip(labels, field_names)):
                label = tk.Label(self.family_info_tab, text=label_text,bg='#c2b9ad', fg='#1b1a17')
                label.grid(row=i, column=0, sticky=tk.W)

                if field_name == "NationalCode":
                    entry = tk.Entry(self.family_info_tab,width=24)  # غیرقابل ویرایش
                    entry.insert(0, self.national_code)
                    entry.config(state='disabled')

                else:
                    entry = tk.Entry(self.family_info_tab,width=24)

                    # اضافه کردن دکمه تقویم برای انتخاب تاریخ ازدواج
                    if field_name == "LatestMarriageDate":
                        calendar_button = tk.Button(self.family_info_tab, text="انتخاب تاریخ",bg='#9b9184', fg='#1b1a17',
                                                    command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2))
                        calendar_button.grid(row=i, column=2)

                    if field_name in ["TotalDependents", "TotalChildren", "TotalDaughters", "TotalSons"]:
                        entry = tk.Entry(self.family_info_tab, validate="key",width=24)
                        entry['validatecommand'] = (self.root.register(self.validate_numeric_input), '%P')

                entry.grid(row=i, column=1)
                self.family_fields[field_name] = entry  # ذخیره ورودی در دیکشنری

            # دکمه برای باز کردن فرم عائله
            file_button = tk.Button(self.family_info_tab, text="پرونده", command=self.Family_File)
            file_button.grid(row=len(labels), column=1, pady=10)
        except Exception as e:
            logging.error(f"خطا در ایجاد تب عائله: {e}")
            print(f"خطا در ایجاد تب عائله: {e}")
    def Family_File(self):
       try:
            FamilyFile(self.root,self.db_manager,self.national_code)
       except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")

    def fill_family_info_tab(self, national_code):
        try:
            # اجرای کوئری با پارامتر کد ملی برای دریافت اطلاعات خانوادگی
            query = """SELECT 
                            ?,  -- NationalCode
                            (SELECT TOP 1 MarriageDate 
                             FROM Dependents 
                             WHERE FamilyNationalCode = ? AND MarriageDate IS NOT NULL 
                             ORDER BY MarriageDate DESC) AS LatestMarriageDate,
                            (SELECT COUNT(*) FROM Dependents WHERE FamilyNationalCode = ?) AS TotalDependents,
                            (SELECT COUNT(*) FROM Children WHERE ParentNationalCode = ? AND GenderID = 2) AS TotalDaughters,
                            (SELECT COUNT(*) FROM Children WHERE ParentNationalCode = ? AND GenderID = 1) AS TotalSons,
                            (SELECT COUNT(*) FROM Children WHERE ParentNationalCode = ?) AS TotalChildren"""

            result = self.db_manager.fetch_one(query, (
                national_code, national_code, national_code, national_code, national_code, national_code))

            # بررسی نتیجه کوئری
            if not result:
                print(f"No family info found for the given National Code: {national_code}.")
                return

            # تنظیم مقادیر فیلدهای خانوادگی با استفاده از نتیجه کوئری
            for i, (field_name, entry) in enumerate(self.family_fields.items()):
                # مقداردهی ورودی‌ها با نتیجه کوئری
                entry_value = result[i] if result[i] is not None else ""
                entry.delete(0, tk.END)  # پاک کردن ورودی قبلی
                entry.insert(0, entry_value)  # مقدار جدید را وارد کنید
                if field_name == "NationalCode":
                    entry.config(state='disabled')  # غیرفعال کردن فیلد کد ملی

        except Exception as e:
            logging.error(f"Error fetching Family info: {e}")
            print(f"Database Error: {e}")

    def load_combobox_data(self, field_name):
        """ بارگذاری داده‌ها برای کامبو باکس مشخص شده """

    def create_promotions_info_tab(self):
        # ساخت تب جدید برای نمایش اطلاعات ارتقاء
        self.promotions_info_tab = self.tabs_dict["ترفیعات"]
        self.promotion_dic = {}

        # برچسب‌ها و نام فیلدهای اطلاعات ارتقاء
        labels = [
            "کد ملی:", "درجه یا رتبه فعلی:", "تاریخ ترفیع فعلی:", "درجه یا رتبه بعدی:",
            "تاریخ ترفیع بعدی:", "تعداد روز ارشدیت:", "تعداد روز کسر از ترفیع:", "نوع درجه:",
            "تعداد درجه موقت:", "توضیحات ترفیع:", "استعلامات:", "درجه در مرحله تطبیق:",
            "قدمت در مرحله تطبیق:", "مراحل ترفیعات:", "ارتقاء حقوقی اول:", "تاریخ ارتقاء حقوقی اول:",
            "ارتقاء حقوقی دوم:", "تاریخ ارتقاء حقوقی دوم:", "ارتقاء حقوقی سوم:",
            "تاریخ ارتقاء حقوقی سوم:", "ارتقاء حقوقی چهارم:", "تاریخ ارتقاء حقوقی چهارم:"
        ]

        # نام فیلدها (لیست جدید)

        # ایجاد برچسب‌ها و ورودی‌ها در تب
        for i, (label_text, field_name) in enumerate(zip(labels, self.promotion_fields)):
            try:
                # ایجاد برچسب
                label = tk.Label(self.promotions_info_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17')
                label.grid(row=i, column=0, sticky=tk.W)

                if field_name == "NationalCode":
                    # ایجاد ورودی فقط خواندنی برای کد ملی
                    entry = tk.Entry(self.promotions_info_tab, width=24)
                    entry.insert(0,self.national_code)
                    entry.config(state='disabled')
                elif field_name in ["PromotionDate", "NextPromotionDate",
                                    "FirstSalaryIncreaseDate", "SecondSalaryIncreaseDate",
                                    "ThirdSalaryIncreaseDate", "FourthSalaryIncreaseDate"]:
                    # فیلدهای تاریخی با دکمه انتخاب تاریخ
                    entry = tk.Entry(self.promotions_info_tab, width=24)
                    calendar_button = tk.Button(
                        self.promotions_info_tab, text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                        command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2))
                    calendar_button.grid(row=i, column=2)
                elif field_name in ["CurrentRank", "AdjustmentRank", "NextRank","RankType"]:
                    # ایجاد کومبو باکس
                    entry = ttk.Combobox(self.promotions_info_tab)
                    self.load_combobox_data_promotions(entry, field_name)
                elif field_name in ["DeductionDays", "TemporaryRankCount", "SeniorityDays"]:
                    # فیلدهای عددی
                    entry = tk.Entry(self.promotions_info_tab, validate="key", width=24)
                    entry['validatecommand'] = (self.root.register(self.validate_numeric_input), '%P')
                elif field_name == "Inquiries":
                    # ایجاد چک‌باکس
                    self.inquiries_var = tk.IntVar()
                    entry = tk.Checkbutton(self.promotions_info_tab, variable=self.inquiries_var)
                else:
                    # فیلدهای متنی پیش‌فرض
                    entry = tk.Entry(self.promotions_info_tab, width=24)

                # قرار دادن ویجت در گرید
                entry.grid(row=i, column=1)
                # ذخیره ویجت در دیکشنری
                self.field_names_promotion[field_name] = entry

            except Exception as e:
                logging.error(f"Error creating field Promotions  '{field_name}': {e}")
                print(f"خطایی رخ داد در فیلد '{field_name}': {e}")

        # دکمه برای باز کردن فرم پاداش‌ها و تنبیهات
        file_button = tk.Button(self.promotions_info_tab, text="پرونده", command=self.open_promotions_form)
        file_button.grid(row=len(labels), column=1, pady=10)



    def open_promotions_form(self):
        try:
            # دریافت کد ملی از فیلد مربوطه
            national_code = self.field_names_promotion["NationalCode"].get()

            # بررسی اینکه کد ملی وارد شده باشد
            if not national_code:
                messagebox.showerror("خطا", "لطفاً کد ملی را وارد کنید.")
                return

            # ایجاد پنجره جدید
            PromotionFile(self.root,self.db_manager,national_code)  # ارسال کد ملی به کلاس RewardDisciplinary

            # تنظیمات پنجره جدید

        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")
    def open_reward_disciplinary_form(self):
        try:
            # دریافت کد ملی از فیلد مربوطه
            national_code = self.field_names_promotion["NationalCode"].get()

            # بررسی اینکه کد ملی وارد شده باشد
            if not national_code:
                messagebox.showerror("خطا", "لطفاً کد ملی را وارد کنید.")
                return

            # ایجاد پنجره جدید
            RewardDisciplinary(self.root,self.db_manager,national_code)  # ارسال کد ملی به کلاس RewardDisciplinary

            # تنظیمات پنجره جدید
        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")

    def open__form(self):
        try:
            # دریافت کد ملی از فیلد مربوطه
            national_code = self.field_names_promotion["NationalCode"].get()

            # بررسی اینکه کد ملی وارد شده باشد
            if not national_code:
                messagebox.showerror("خطا", "لطفاً کد ملی را وارد کنید.")
                return

            # ایجاد پنجره جدید
            RewardDisciplinary(self.root,self.db_manager,national_code)  # ارسال کد ملی به کلاس RewardDisciplinary

            # تنظیمات پنجره جدید

        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")

    def fill_promotions_info_tab(self, national_code):
        try:
            # اجرای کوئری برای دریافت اطلاعات ترفیعات از جدول Promotions
            query = "SELECT * FROM Promotions WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            if not result:
                logging.warning(f"No promotions info found for National Code: {national_code}")
                print(f"اطلاعاتی برای کد ملی '{national_code}' یافت نشد.")
                return

            # پر کردن مقادیر در فیلدهای فرم
            for field_name in self.promotion_fields:
                widget = self.field_names_promotion.get(field_name)
                if not widget:
                    logging.warning(f"No widget found for field '{field_name}' in promotions tab.")
                    continue

                # مقدار متناظر با فیلد را از نتیجه پیدا کنید
                field_index = self.promotion_fields.index(field_name)
                entry_value = result[field_index+1] if result[field_index+1] is not None else ""
                # مدیریت انواع مختلف ویجت‌ها
                if isinstance(widget, ttk.Combobox):
                    # بررسی اینکه مقدار entry_value یک عدد معتبر است
                    try:
                        index = int(entry_value) - 1  # تبدیل مقدار به عدد و تنظیم ایندکس
                        if 0 <= index < len(widget['values']):
                            widget.current(index)  # تنظیم مقدار مشخص‌شده
                        else:
                            widget.current(len(widget['values']) - 1)  # تنظیم مقدار آخر در صورت نامعتبر بودن ایندکس
                    except ValueError:
                        widget.current(len(widget['values']) - 1)  # مقدار آخر در صورت نامعتبر بودن entry_value
                elif isinstance(widget, tk.Entry):
                    # اگر ویجت Entry است
                    widget.delete(0, tk.END)
                    widget.insert(0, entry_value)
                elif isinstance(widget, tk.Checkbutton):
                    # اگر ویجت Checkbutton است
                    if isinstance(entry_value, int):
                        widget_variable = widget.cget("variable")
                        self.root.setvar(widget_variable, entry_value)
            print("اطلاعات با موفقیت بارگذاری شد.")

        except Exception as e:
            logging.error(f"Error fetching promotions info: {e}")
            print(f"خطا در پر کردن اطلاعات ترفیعات: {e}")


    def load_combobox_data_promotions(self, combobox, field_name):
        # دیکشنری برای نگهداری IDها و مقادیر
        data_dict = {}
        # بارگذاری داده‌ها بر اساس فیلد
        if field_name == "CurrentRank":
            query = "SELECT RankID, RankDescription FROM Ranks"
        elif field_name == "AdjustmentRank":
            query = "SELECT RankID, RankDescription FROM Ranks"
        elif field_name == "NextRank":
            query = "SELECT RankID, RankDescription FROM Ranks"
        elif field_name == "RankType":
            query = "SELECT * FROM RankType"

        else:
            return  # برای دیگر فیلدها نیازی به بارگذاری نیست

        try:
            results = self.db_manager.fetch_all(query)  # فرض بر این است که متدی برای دریافت تمام داده‌ها دارید
            values = [row[1] for row in results]  # نام و ID را به صورت ترکیبی نمایش دهید

            for row in results:
                data_dict[row[0]] = row[1]  # ذخیره ID و نام در دیکشنری

            combobox['values'] = values
            # تنظیم combobox به حالت readonly
            combobox['state'] = 'readonly'

            if values:
                combobox.current(0)  # انتخاب اولین مقدار به عنوان مقدار پیش‌فرض


            # ذخیره دیکشنری به عنوان یک ویژگی کلاس
            setattr(self, f"{field_name}_data_dict", data_dict)

        except Exception as e:
            logging.error(f"Error loading {field_name} data: {e}")
            print(f"Error loading {field_name} data: {e}")


    def open_calendar(self, entry, row, column, pady):
        # باز کردن تقویم و دریافت تاریخ شمسی
        def on_date_select(selected_date):
            """کال‌بک برای انتخاب تاریخ."""
            # پاک کردن مقدار قبلی و درج مقدار جدید در فیلد
            entry.delete(0, tk.END)
            entry.insert(0, selected_date)  #

        calendar_app = ShamsiCalendarApp(
            root=self.root,
            entry=entry,
            on_date_select_callback=on_date_select

        )

    def open_cddalenddar(self, entry, row, column, pady):
        def on_date_select(selected_date):
            """کال‌بک برای انتخاب تاریخ."""
            # پاک کردن مقدار قبلی و درج مقدار جدید در فیلد
            entry.delete(0, tk.END)
            entry.insert(0, selected_date)  # مقدار تاریخ انتخاب‌شده

        # ایجاد اپلیکیشن تقویم و ارسال کال‌بک برای مدیریت تاریخ انتخابی
        calendar_app = ShamsiCalendarApp(
            root=self.root,
            entry=entry,
            row=row,
            column=column,
            pady=pady,
            on_date_select_callback=on_date_select
        )

    def create_calendar_callback(self, entry, row, column, pady=2):
        # بازگشت تابعی که هنگام کلیک روی دکمه تقویم اجرا می‌شود
        return lambda: self.open_calendar(entry, row, column, pady)


    def get_combobox_id(self, field_name, display_value):
        # دریافت ID معادل برای مقدار نمایشی
        data_dict = getattr(self, f"{field_name}_data_dict", {})
        for id_value, name in data_dict.items():
            if name == display_value:
                return id_value
        return None  # اگر مقداری پیدا نشد، None برگردانید

    def Accidentsfile(self):
        try:
            AccidentFile(self.root, self.db_manager,self.national_code)  # ارسال کد ملی به کلاس RewardDisciplinary
        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")

    def Militaryfile(self):
        try:
            MillitaryFile(self.root, self.db_manager,self.national_code)  # ارسال کد ملی به کلاس RewardDisciplinary
        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")
    def ClassicFile(self):
        try:
            ClassicFile(self.root, self.db_manager,self.national_code)  # ارسال کد ملی به کلاس RewardDisciplinary
        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")

    def Languagefile(self):
        try:
            LanguageFile(self.root, self.db_manager,self.national_code)  # ارسال کد ملی به کلاس lanaguage file
        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")

    def create_employee_bank_details_tab(self):
        # ایجاد تب اطلاعات بانکی
        self.employee_bank_details_tab = self.tabs_dict["متفرقه"]

        # دیکشنری برای ذخیره ویجت‌های فیلدها
        self.bank_fields = {}

        # تعریف برچسب‌ها و نام فیلدها
        labels = [
            "کد ملی:", "شاخص بانک:", "نام بانک:", "نام شعبه:",
            "شماره حساب حقوقی:", "نوع حساب:", "شماره کارت:", "شماره شبا:"
        ]

        # ایجاد ویجت‌ها در تب
        for i, (label_text, field_name) in enumerate(zip(labels, self.field_names_bank)):
            label = tk.Label(
                self.employee_bank_details_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17'
            )
            label.grid(row=i, column=0, sticky=tk.W)
            if field_name in ["NationalCode"]:
                entry = tk.Entry(self.employee_bank_details_tab, width=24)
                entry.insert(0, self.national_code)
                entry.config(state=tk.DISABLED)
            elif field_name in ["AccountTypeID", "BankNameID"]:
                # ایجاد Combobox برای فیلدهای انتخابی
                entry = ttk.Combobox(self.employee_bank_details_tab, width=20, state="readonly")
                self.load_employee_bank_details_tab(entry, field_name)  # بارگذاری داده‌ها
            else:
                # ایجاد Entry برای فیلدهای متنی
                entry = tk.Entry(self.employee_bank_details_tab, width=24)

            entry.grid(row=i, column=1)
            self.bank_fields[field_name] = entry

        # افزودن دکمه "پرونده"
        file_button_accident = tk.Button(
            self.employee_bank_details_tab, text="پرونده حوادث",
            command=self.Accidentsfile, bg='#9b9184', fg='#1b1a17'
        )
        file_button_value = tk.Button(
            self.employee_bank_details_tab, text="پرونده ارزشیابی",
            command=self.EmployeeEvaluationForm, bg='#9b9184', fg='#1b1a17'
        )
        file_button_punishment = tk.Button(
            self.employee_bank_details_tab, text="پرونده تشویقات ح محکومیت ها",
            command=self.open_reward_disciplinary_form, bg='#9b9184', fg='#1b1a17'
        )
        file_button_negative = tk.Button(
            self.employee_bank_details_tab, text="پرونده امتیازات و تشویقات",
            command=self.open_reward_disciplinary_form, bg='#9b9184', fg='#1b1a17'
        )
        file_button_negative.grid(row=len(labels), column=1, pady=10)
        file_button_punishment.grid(row=len(labels), column=2, pady=10)
        file_button_value.grid(row=len(labels), column=3, pady=10)
        file_button_accident.grid(row=len(labels), column=4, pady=10)
    def EmployeeEvaluationForm(self):
        try:
            # بررسی اینکه کد ملی وارد شده باشد
            if not self.national_code:
                messagebox.showerror("خطا", "لطفاً کد ملی را وارد کنید.")
                return

            # ایجاد پنجره جدید
            EmployeeEvaluationFile(self.root,self.national_code,self.db_manager,self.tarikh_estekhdam)
            #def __init__(self, national_code, db_manager, start_year=None):

        # تنظیمات پنجره جدید
        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")


    def fill_employee_bank_details_tab(self, national_code):
        try:
            # اجرای کوئری با پارامتر کد ملی برای دریافت اطلاعات بانکی
            query = "SELECT * FROM EmployeeBankDetails WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if not result:
                print(f"No bank details found for the given National Code: {national_code}.")
                return

            for field_name in self.field_names_bank:
                    widget = self.bank_fields.get(field_name)
                    if not widget:
                        logging.warning(f"No widget found for field '{field_name}' in promotions tab.")
                        continue

                    # مقدار متناظر با فیلد را از نتیجه پیدا کنید
                    field_index = self.field_names_bank.index(field_name)
                    entry_value = result[field_index] if result[field_index] is not None else ""
                    # مدیریت انواع مختلف ویجت‌ها
                    if isinstance(widget, ttk.Combobox):
                        # بررسی اینکه مقدار entry_value یک عدد معتبر است
                        try:
                            index = int(entry_value) - 1  # تبدیل مقدار به عدد و تنظیم ایندکس
                            if 0 <= index < len(widget['values']):
                                widget.current(index)  # تنظیم مقدار مشخص‌شده
                            else:
                                widget.current(len(widget['values']) - 1)  # تنظیم مقدار آخر در صورت نامعتبر بودن ایندکس
                        except ValueError:
                            widget.current(len(widget['values']) - 1)  # مقدار آخر در صورت نامعتبر بودن entry_value
                    elif field_name == "NationalCode":
                        widget.config(state="disabled")
                    elif isinstance(widget, tk.Entry):
                        # اگر ویجت Entry است
                        widget.delete(0, tk.END)
                        widget.insert(0, entry_value)
                    elif isinstance(widget, tk.Checkbutton):
                        # اگر ویجت Checkbutton است
                        if isinstance(entry_value, int):
                            widget_variable = widget.cget("variable")
                            self.root.setvar(widget_variable, entry_value)
        except Exception as e:
            logging.error(f"Error fetching bank details: {e}")
            print(f"Database Error: {e}")

    def load_employee_bank_details_tab(self, combobox, field_name):
        try:
            # برای هر شناسه، کوئری مناسب را اجرا کنید
            if field_name == "AccountTypeID":
                query = "SELECT AccountTypeID, AccountTypeName  FROM AccountType"
            elif field_name == "BankNameID":
                query = "SELECT BankNameID, BankName  FROM BankName"
            else:
                return  # اگر شناسه ناشناخته بود، تابع را ترک کنید
            data_dict = {}
            try:
                results = self.db_manager.fetch_all(query)  # فرض بر این است که متدی برای دریافت تمام داده‌ها دارید
                values = [row[1] for row in results]  # نام و ID را به صورت ترکیبی نمایش دهید
                for row in results:
                    data_dict[row[0]] = row[1]  # ذخیره ID و نام در دیکشنری
                combobox['values'] = values
                combobox['state'] = 'readonly'  # تنظیم combobox به حالت readonly
                if values:
                    combobox.current(0)  # انتخاب اولین مقدار به عنوان مقدار پیش‌فرض

                # ذخیره دیکشنری به عنوان یک ویژگی کلاس
                setattr(self, f"{field_name}_data_dict", data_dict)

            except Exception as e:
                logging.error(f"load_employee_bank_details_tab Error loading {field_name} data: {e}")

        except Exception as e:
            logging.error(f"Error loading combobox data for {field_name}: {e}")
            print(f"Error loading combobox data for {field_name}: {e}")

    def create_job_info_tab(self):
        # ایجاد تب "مشاغل"
        self.job_info_tab = self.tabs_dict["مشاغل"]
        self.job_fields = {}

        # برچسب‌ها و نام فیلدها
        labels = [
            "کد ملی:", "عنوان شغلی:", "کد شغل:", "کلید پست:",
            "سطح شغلی:", "گروه شغلی:", "محل کار:", "تاریخ انتصاب:",
            "نوع انتصاب:", "مدرک:", "سطح دسترسی:", "نوع شغل:",
            "بخش:", "رتبه شغلی:", "واحد:"
        ]
        # ایجاد برچسب‌ها و ویجت‌های ورودی
        for i, (label_text, field_name) in enumerate(zip(labels, self.field_names_job)):
            label = tk.Label(self.job_info_tab, text=label_text, bg='#c2b9ad', fg='#1b1a17')
            label.grid(row=i, column=0, sticky=tk.W)

            if field_name in [
                "WorkLocationID", "JobGroupID", "JobRankID", "SectionID",
                "DepartmentID", "JobTypeID", "AccessLevelID", "DegreeID", "AppointmentTypeID"
            ]:
                # ایجاد کومبوباکس برای فیلدهای دارای لیست
                entry = ttk.Combobox(self.job_info_tab, width=20)
                self.load_combobox_data_job(entry, field_name)  # بارگذاری داده‌ها در کومبوباکس
            elif field_name == "AppointmentDate":
                # ایجاد ورودی برای تاریخ به همراه دکمه انتخاب تاریخ
                entry = tk.Entry(self.job_info_tab, width=24)
                calendar_button = tk.Button(
                    self.job_info_tab, text="انتخاب تاریخ", bg='#9b9184', fg='#1b1a17',
                    command=lambda ent=entry: self.open_calendar(ent, row=i, column=1, pady=2))
                calendar_button.grid(row=i, column=2)
            elif field_name == "NationalCode":
                # ایجاد ورودی فقط خواندنی برای کد ملی
                entry = tk.Entry(self.job_info_tab, width=24)
                entry.insert(0, self.national_code)
                entry.config(state="disabled")
            else:
                # ایجاد ورودی عمومی
                entry = tk.Entry(self.job_info_tab, width=24)
                entry.grid(row=i, column=1)
            self.job_fields[field_name] = entry
            entry.grid(row=i, column=1)
        file_button = tk.Button(self.job_info_tab, text="پرونده", command=self.open_JobForm)
        file_button.grid(row=len(labels), column=3, pady=10)  # موقعیت قرارگیری دکمه را مطابق نیاز خود تنظیم کنید

    def open_JobForm(self):
        try:
            # دریافت کد ملی از فیلد مربوطه
            national_code = self.field_names_promotion["NationalCode"].get()
            # بررسی اینکه کد ملی وارد شده باشد
            if not national_code:
                messagebox.showerror("خطا", "لطفاً کد ملی را وارد کنید.")
                return

            # ایجاد پنجره جدید
            JobFile(self.root, self.db_manager,self.national_code)  # ارسال کد ملی به کلاس RewardDisciplinary

            # تنظیمات پنجره جدید

        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {e}")

    def fill_job_info(self, national_code):
        try:
            query = "SELECT * FROM JobInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            if not result:
                print(f"No job info found for the given National Code: {national_code}.")
                return
            for field_name in self.field_names_job:
                widget = self.job_fields.get(field_name)
                if not widget:
                    logging.warning(f"No widget found for field '{field_name}' in promotions tab.")
                    continue

                # مقدار متناظر با فیلد را از نتیجه پیدا کنید
                field_index = self.field_names_job.index(field_name)
                entry_value = result[field_index] if result[field_index] is not None else ""
                # مدیریت انواع مختلف ویجت‌ها
                if isinstance(widget, ttk.Combobox):
                    # بررسی اینکه مقدار entry_value یک عدد معتبر است
                    try:
                        index = int(entry_value) - 1  # تبدیل مقدار به عدد و تنظیم ایندکس
                        if 0 <= index < len(widget['values']):
                            widget.current(index)  # تنظیم مقدار مشخص‌شده
                        else:
                            widget.current(len(widget['values']) - 1)  # تنظیم مقدار آخر در صورت نامعتبر بودن ایندکس
                    except ValueError:
                        widget.current(len(widget['values']) - 1)  # مقدار آخر در صورت نامعتبر بودن entry_value
                elif field_name == "NationalCode":
                    widget.delete(0, tk.END)
                    widget.insert(0, entry_value)
                    widget.config(state="disabled")
                elif isinstance(widget, tk.Entry):
                    # اگر ویجت Entry است
                    widget.delete(0, tk.END)
                    widget.insert(0, entry_value)
                elif isinstance(widget, tk.Checkbutton):
                    # اگر ویجت Checkbutton است
                    if isinstance(entry_value, int):
                        widget_variable = widget.cget("variable")
                        self.root.setvar(widget_variable, entry_value)

        except Exception as e:
            logging.error(f"Error fetching job info: {e}")
            print(f"Database Error: {e}")

    def load_combobox_data_job(self, combobox, field_name):
        data_dict = {}

        if field_name == "JobGroupID":
            query = "SELECT JobGroupID, JobGroupName FROM JobGroup"
        elif field_name == "WorkLocationID":
            query = "SELECT WorkLocationID, WorkLocationName FROM WorkLocation"
        elif field_name == "AppointmentTypeID":
            query = "SELECT AppointmentTypeID, AppointmentTypeName FROM AppointmentType"
        elif field_name == "DegreeID":
            query = "SELECT DegreeID, DegreeName FROM Degree"
        elif field_name == "AccessLevelID":
            query = "SELECT AccessLevelID, AccessLevelName FROM AccessLevel"
        elif field_name == "JobTypeID":
            query = "SELECT JobTypeID, JobTypeName FROM JobType"
        elif field_name == "DepartmentID":
            query = "SELECT DepartmentID, DepartmentName FROM Department"
        elif field_name == "JobRankID":
            query = "SELECT JobRankID, JobRankName FROM JobRank"
        elif field_name == "SectionID":
            query = "SELECT SectionID, SectionName FROM Section"
        else:
            return

        try:
            results = self.db_manager.fetch_all(query)
            values = [row[1] for row in results]
            for row in results:
                data_dict[row[0]] = row[1]  # ذخیره ID و نام در دیکشنری
            combobox['values'] = values
            combobox['state'] = 'readonly'

            if values:
                combobox.current(0)  # انتخاب اولین مقدار پیش‌فرض

            setattr(self, f"{field_name}_data_dict", data_dict)  # ذخیره دیکشنری

        except Exception as e:
            logging.error(f"Error loading {field_name} data: {e}")

    def safe_int(self, value):
        if value.strip() == '':  # اگر خالی بود
            return 0  # مقدار پیش‌فرض
        try:
            return int(value)
        except ValueError:
            logging.error(f"Invalid integer value: {value}")
            return 0  # مقدار پیش‌فرض

    def save_all_tabs(self):
        try:
            #self.save_personal_info()
            #self.save_missions_info()
            self.save_education_info()
            #self.save_promotions_info()
            #self.save_sanavat_info()
            #self.save_employment_info()
            #self.save_employee_bank_details()
            #self.save_job_info()
            #self.save_family_info()
        except Exception as e:
            logging.error(f"Error saving data: {e}")
            messagebox.showerror("Error", str(e))

    def show_error_message(self, message):
        # ساخت پنجره خطا
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_window.geometry("300x150")
        error_window.transient(self.root)  # متمرکز کردن پنجره خطا روی پنجره اصلی
        error_window.grab_set()  # جلوگیری از تعامل کاربر با سایر بخش‌ها تا بسته شدن پنجره خطا
        error_window.attributes("-topmost", True)  # نمایش پنجره خطا در بالای همه پنجره‌ها

        # افزودن متن پیام خطا
        label = tk.Label(error_window, text=message, font=("Helvetica", 12), fg="red")
        label.pack(pady=20)

        # دکمه بستن پنجره خطا
        button = tk.Button(error_window, text="باشه", command=error_window.destroy)
        button.pack(pady=10)

        # موقعیت دادن به پنجره خطا در وسط صفحه
        error_window.update_idletasks()
        x = (error_window.winfo_screenwidth() - 300) // 2
        y = (error_window.winfo_screenheight() - 150) // 2
        error_window.geometry(f"+{x}+{y}")

    def save_personal_info(self):
        try:
            # جمع‌آوری اطلاعات از فیلدها
            national_code = self.personal_fields['NationalCode'].get()
            if len(national_code) != 10:
                logging.error("Error saving personal info: کد ملی باید ده رقم بوده و تکراری نباشد.")
                self.show_error_message("کد ملی باید ده رقم بوده و تکراری نباشد.")  # نمایش پیام خطا به صورت مرکزی
                return
            # جمع‌آوری اطلاعات از فیلدها
            national_code = self.personal_fields['NationalCode'].get().strip()
            first_name = self.personal_fields['FirstName'].get().strip()
            last_name = self.personal_fields['LastName'].get().strip()
            father_name = self.personal_fields['FatherName'].get().strip()
            nick_name = self.personal_fields['NickName'].get().strip()
            birth_date = self.personal_fields['BirthDate'].get().strip()
            birth_place_id = self.BirthPlaceID_data_dict.get(self.personal_fields['BirthPlaceID'].get(), None)
            issue_place_id = self.IssuePlaceID_data_dict.get(self.personal_fields['IssuePlaceID'].get(), None)
            issue_date = self.personal_fields['IssueDate'].get().strip()
            gender_id = self.GenderID_data_dict.get(self.personal_fields['GenderID'].get(), None)
            marital_status_id = self.MaritalStatusID_data_dict.get(self.personal_fields['MaritalStatusID'].get(), None)
            religion_id = self.ReligionID_data_dict.get(self.personal_fields['ReligionID'].get(), None)
            blood_group_id = self.BloodGroupID_data_dict.get(self.personal_fields['BloodGroupID'].get(), None)
            height = self.personal_fields['Height'].get().strip()
            weight = self.personal_fields['Weight'].get().strip()
            eye_color_id = self.EyeColorID_data_dict.get(self.personal_fields['EyeColorID'].get(), None)
            skin_color_id = self.SkinColorID_data_dict.get(self.personal_fields['SkinColorID'].get(), None)
            special_features = self.personal_fields['SpecialFeatures'].get("1.0", "end-1c").strip()
            address = self.personal_fields['Address'].get("1.0", "end-1c").strip()
            postal_code = self.personal_fields['PostalCode'].get().strip()
            phone_number = self.personal_fields['PhoneNumber'].get().strip()
            mobile = self.personal_fields['Mobile'].get().strip()
            email = self.personal_fields['Email'].get().strip()
            personal_id = self.personal_fields['PersonalID'].get().strip()

            # کوئری برای به‌روزرسانی
            update_query = """
                UPDATE PersonalInfo SET 
                    FirstName = ?, LastName = ?, FatherName = ?, NickName = ?, BirthDate = ?, 
                    BirthPlaceID = ?, IssuePlaceID = ?, IssueDate = ?, GenderID = ?, 
                    MaritalStatusID = ?, ReligionID = ?, BloodGroupID = ?, Height = ?, 
                    Weight = ?, EyeColorID = ?, SkinColorID = ?, SpecialFeatures = ?, 
                    Address = ?, PostalCode = ?, PhoneNumber = ?, Mobile = ?, Email = ?, 
                    PersonalID = ?
                WHERE NationalCode = ?
            """

            # پارامترها برای UPDATE
            params_update = (
                first_name, last_name, father_name, nick_name, birth_date,
                birth_place_id, issue_place_id, issue_date, gender_id, marital_status_id,
                religion_id, blood_group_id, height, weight, eye_color_id, skin_color_id,
                special_features, address, postal_code, phone_number, mobile, email, personal_id,
                national_code  # پارامتر اضافی برای WHERE
            )

            # کوئری برای درج
            insert_query = """
                INSERT INTO PersonalInfo (NationalCode, FirstName, LastName, FatherName, NickName, BirthDate, 
                    BirthPlaceID, IssuePlaceID, IssueDate, GenderID, MaritalStatusID, ReligionID, 
                    BloodGroupID, Height, Weight, EyeColorID, SkinColorID, SpecialFeatures, Address, 
                    PostalCode, PhoneNumber, Mobile, Email, PersonalID) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # لیست پارامترها برای INSERT
            params_insert = (
                national_code, first_name, last_name, father_name, nick_name, birth_date,
                birth_place_id, issue_place_id, issue_date, gender_id, marital_status_id,
                religion_id, blood_group_id, height, weight, eye_color_id, skin_color_id,
                special_features, address, postal_code, phone_number, mobile, email, personal_id
            )

            # بررسی وجود رکورد
            query = "SELECT * FROM PersonalInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if result is None:  # اگر رکورد وجود ندارد، درج کن
                self.db_manager.execute_query(insert_query, params_insert)
                self.show_success_notification("اطلاعات با موفقیت ذخیره شد.")


            else:  # اگر رکورد وجود دارد، به‌روزرسانی کن
                self.db_manager.execute_query(update_query, params_update)
                self.show_success_notification("اطلاعات با موفقیت بروزرسانی شد.")

        except Exception as e:
            logging.error(f"Save Error: Error saving personal info: {e}")
            messagebox.showerror("Personal Save Error", str(e))

    def show_success_notification(self, message):
        # ایجاد پنجره کوچک برای نمایش پیغام موفقیت بدون نوار عنوان
        notification = Toplevel(self.root)
        notification.title("پیغام")
        notification.geometry("200x100")
        notification.attributes('-topmost', True)
        notification.overrideredirect(1)  # حذف نوار عنوان

        # محاسبه موقعیت وسط صفحه
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (200 // 2)  # 200 عرض پنجره است
        y = (screen_height // 2) - (100 // 2)  # 100 ارتفاع پنجره است

        # تنظیم موقعیت پنجره در وسط صفحه
        notification.geometry(f"200x100+{x}+{y}")

        # نمایش پیام در پنجره
        label = Label(notification, text=message, font=("Helvetica", 12))
        label.pack(expand=True, padx=10, pady=10)

        # بستن پنجره بعد از ۵ ثانیه
        notification.after(5000, notification.destroy)

    def show_success_notifications(self, message):
        # ایجاد پنجره کوچک برای نمایش پیغام موفقیت
        notification = Toplevel(self.root)
        notification.title("پیغام")
        notification.geometry("200x100")
        notification.attributes('-topmost', True)

        # نمایش پیام در پنجره
        label = Label(notification, text=message, font=("Helvetica", 12))
        label.pack(expand=True, padx=10, pady=10)

        # بستن پنجره بعد از ۵ ثانیه
        notification.after(5000, notification.destroy)

    def save_missions_infod(self):
        try:
            # جمع‌آوری اطلاعات از فیلدها
            national_code = self.national_code
            official_service_duration = self.missions_fields['OfficialServiceDuration'].get()
            front_line_duration = self.missions_fields['FrontLineDuration'].get()
            basij_service_duration = self.missions_fields['BasijServiceDuration'].get()

            # تبدیل مدت‌ها به int اگر ممکن باشد
            official_service_duration = int(official_service_duration) if official_service_duration.isdigit() else None
            front_line_duration = int(front_line_duration) if front_line_duration.isdigit() else None
            basij_service_duration = int(basij_service_duration) if basij_service_duration.isdigit() else None

            # کوئری برای ذخیره اطلاعات خدمت نظامی
            insert_query = """
                INSERT INTO MissionInfo (PersonalNationalCode, MissionTypeID, StartDate, EndDate, MissionDurationInMonths, CountryID, MissionOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            # در اینجا می‌توانید مقادیر MissionTypeID و CountryID را تعیین کنید یا از فیلدهای ورودی دیگر بگیرید
            mission_type_id = None  # مقدار MissionTypeID باید مشخص شود
            country_id = None  # مقدار CountryID باید مشخص شود
            start_date = None  # تاریخ شروع باید مشخص شود
            end_date = None  # تاریخ پایان باید مشخص شود

            # پارامترها برای INSERT
            params_insert = (
                national_code, mission_type_id, start_date, end_date,
                official_service_duration, country_id, front_line_duration  # پارامتر مناسب اضافه شد
            )

            # بررسی وجود رکورد
            query = "SELECT * FROM MissionInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if result is None:  # اگر رکورد وجود ندارد، درج کن
                self.db_manager.execute_query(insert_query, params_insert)

            else:  # اگر رکورد وجود دارد، به‌روزرسانی کن
                self.db_manager.execute_query(update_query, params_update)

            # چاپ تعداد پارامترها برای بررسی
            print(f"Number of parameters for insert: {len(params_insert)}")  # باید برابر با 7 باشد
            # اجرای کوئری برای ذخیره اطلاعات

            self.db_manager.execute_query(insert_query, params_insert)
            messagebox.showinfo("Success", "اطلاعات خدمت نظامی با موفقیت ذخیره شد.")

        except Exception as e:
            logging.error(f"Mission Error saving military service info: {e}")
            messagebox.showerror("Error", str(e))

    def save_missions_info(self):
        try:
            # جمع‌آوری اطلاعات از فیلدها
            national_code = self.national_code
            official_service_duration = self.missions_fields['OfficialServiceDuration'].get()
            front_line_duration = self.missions_fields['FrontLineDuration'].get()
            basij_service_duration = self.missions_fields['BasijServiceDuration'].get()

            # تبدیل مدت‌ها به int اگر ممکن باشد
            official_service_duration = int(official_service_duration) if official_service_duration.isdigit() else None
            front_line_duration = int(front_line_duration) if front_line_duration.isdigit() else None
            basij_service_duration = int(basij_service_duration) if basij_service_duration.isdigit() else None

            # کوئری برای درج اطلاعات خدمت نظامی
            insert_query = """
                INSERT INTO MissionInfo (PersonalNationalCode, MissionTypeID, StartDate, EndDate, MissionDurationInMonths, CountryID, MissionOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            # کوئری برای به‌روزرسانی اطلاعات خدمت نظامی
            update_query = """
                UPDATE MissionInfo
                SET MissionTypeID = ?, StartDate = ?, EndDate = ?, MissionDurationInMonths = ?, CountryID = ?, MissionOrder = ?
                WHERE PersonalNationalCode = ?
            """

            # مقادیر اولیه
            mission_type_id = None  # مقدار MissionTypeID باید مشخص شود
            country_id = None  # مقدار CountryID باید مشخص شود
            start_date = None  # تاریخ شروع باید مشخص شود
            end_date = None  # تاریخ پایان باید مشخص شود

            # پارامترها برای INSERT
            params_insert = (
                national_code, mission_type_id, start_date, end_date,
                official_service_duration, country_id, front_line_duration
            )

            # پارامترها برای UPDATE
            params_update = (
                mission_type_id, start_date, end_date, official_service_duration,
                country_id, front_line_duration, national_code
            )

            # بررسی وجود رکورد
            query = "SELECT * FROM MissionInfo WHERE PersonalNationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if result is None:  # اگر رکورد وجود ندارد، درج کن
                self.db_manager.execute_query(insert_query, params_insert)
                self.show_success_notification("اطلاعات با موفقیت ذخیره شد.")

            else:  # اگر رکورد وجود دارد، به‌روزرسانی کن
                self.db_manager.execute_query(update_query, params_update)
                self.show_success_notification("اطلاعات با موفقیت بروزرسانی شد.")


            # پیام موفقیت
            #messagebox.showinfo("Success", "اطلاعات خدمت نظامی با موفقیت ذخیره شد.")

        except Exception as e:
            logging.error(f"Mission Error saving military service info: {e}")
            #messagebox.showerror("Error", str(e))

    def save_education_info(self):
        try:
            # جمع‌آوری اطلاعات از فیلدها
            national_code = self.national_code
            self.education_fields = [
                "NationalCode", "EducationLevelID", "Major", "DegreeLevelID",
                "City", "UniversityID", "GraduationDate", "DegreeTypeID",
                "IserID", "Gerayesh", "GPA", "EmploymentDegreeLevelID", "MilitaryEducation", "MilitaryEducationLocation"
            ]

            # تبدیل مقادیر ComboBox به ID
            education_level_id = self.get_combobox_id("EducationLevelID",
                                                      self.education_entries["EducationLevelID"].get())
            start_date = self.education_entries["Major"].get()

            field_of_study_id = self.get_combobox_id("DegreeLevelID", self.education_entries["DegreeLevelID"].get())
            educational_institution_id = self.get_combobox_id("UniversityID",
                                                              self.education_entries["UniversityID"].get())
            start_date = self.education_entries["City"].get()
            end_date = self.education_entries["GraduationDate"].get()
            failure_months = self.education_entries["Gerayesh"].get()
            certificate_id = self.get_combobox_id["CertificateID"].get()
            grade = self.education_entries["GPA"].get()
            MilitaryEducation = self.education_entries["MilitaryEducation"].get()
            MilitaryEducationLocation = self.education_entries["MilitaryEducationLocation"].get()


            # کوئری برای به‌روزرسانی
            update_query = """
                UPDATE EducationInfo SET 
                    EducationLevelID = ?, FieldOfStudyID = ?, EducationalInstitutionID = ?, 
                    StartDate = ?, EndDate = ?, FailureMonths = ?, 
                    CertificateID = ?, Grade = ?, CityID = ?, 
                    UniversityID = ?, IserID = ?
                WHERE NationalCode = ?
            """

            # پارامترها برای UPDATE
            params_update = (
                education_level_id, field_of_study_id, educational_institution_id,
                start_date, end_date, failure_months, certificate_id,
                grade, city_id, university_id, iser_id, national_code
            )

            # کوئری برای درج
            insert_query = """
                INSERT INTO EducationInfo (NationalCode, EducationLevelID, FieldOfStudyID, 
                    EducationalInstitutionID, StartDate, EndDate, FailureMonths, 
                    CertificateID, Grade, CityID, UniversityID, IserID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # پارامترها برای INSERT
            params_insert = (
                national_code, education_level_id, field_of_study_id,
                educational_institution_id, start_date, end_date,
                failure_months, certificate_id, grade,
                city_id, university_id, iser_id
            )

            # بررسی وجود رکورد
            query = "SELECT * FROM EducationInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if not result:
                print(f"No education info found for the given National Code: {national_code}. Inserting new record.")
                # اگر رکورد وجود ندارد، درج کن
                self.db_manager.execute_query(insert_query, params_insert)
            else:
                print(f"Education info found for the given National Code: {national_code}. Updating record.")
                # اگر رکورد وجود دارد، به‌روزرسانی کن
                self.db_manager.execute_query(update_query, params_update)

            messagebox.showinfo("Success", "اطلاعات تحصیلی با موفقیت ذخیره شد.")

        except Exception as e:
            logging.error(f"Error saving education info: {e}")
            messagebox.showerror("Error", str(e))

    def save_promotions_info(self):
        try:
            # جمع‌آوری اطلاعات از فیلدها
            national_code = self.field_names_promotion["NationalCode"].get()

            # تبدیل مقادیر ComboBox به ID
            current_rank_id = self.get_combobox_id("CurrentRank", self.field_names_promotion["CurrentRank"].get())
            next_rank_id = self.get_combobox_id("NextRank", self.field_names_promotion["NextRank"].get())
            adjustment_rank_id = self.get_combobox_id("AdjustmentRank",
                                                      self.field_names_promotion["AdjustmentRank"].get())
            promotion_date = self.field_names_promotion["PromotionDate"].get()
            next_promotion_date = self.field_names_promotion["NextPromotionDate"].get()
            seniority_days = self.field_names_promotion["SeniorityDays"].get()
            deduction_days = self.field_names_promotion["DeductionDays"].get()
            # rank_type = self.field_names_promotion["RankType"].get()
            rank_type = self.get_combobox_id("RankType", self.field_names_promotion["RankType"].get())

            temporary_rank_count = self.field_names_promotion["TemporaryRankCount"].get()
            promotion_description = self.field_names_promotion["PromotionDescription"].get()
            inquiries = self.field_names_promotion["Inquiries"].get() == "True"  # تبدیل به boolean
            adjustment_seniority_days = self.field_names_promotion["AdjustmentSeniorityDays"].get()
            promotion_stages = self.field_names_promotion["PromotionStages"].get()
            first_salary_increase = self.field_names_promotion["FirstSalaryIncrease"].get()
            first_salary_increase_date = self.field_names_promotion["FirstSalaryIncreaseDate"].get()
            second_salary_increase = self.field_names_promotion["SecondSalaryIncrease"].get()
            second_salary_increase_date = self.field_names_promotion["SecondSalaryIncreaseDate"].get()
            third_salary_increase = self.field_names_promotion["ThirdSalaryIncrease"].get()
            third_salary_increase_date = self.field_names_promotion["ThirdSalaryIncreaseDate"].get()
            fourth_salary_increase = self.field_names_promotion["FourthSalaryIncrease"].get()
            fourth_salary_increase_date = self.field_names_promotion["FourthSalaryIncreaseDate"].get()

            # کوئری برای به‌روزرسانی
            update_query = """
                UPDATE Promotions SET 
                    CurrentRank = ?, PromotionDate = ?, NextRank = ?, 
                    NextPromotionDate = ?, SeniorityDays = ?, DeductionDays = ?, 
                    RankType = ?, TemporaryRankCount = ?, PromotionDescription = ?, 
                    Inquiries = ?, AdjustmentRankID = ?, AdjustmentSeniorityDays = ?, 
                    PromotionStages = ?, FirstSalaryIncrease = ?, FirstSalaryIncreaseDate = ?, 
                    SecondSalaryIncrease = ?, SecondSalaryIncreaseDate = ?, 
                    ThirdSalaryIncrease = ?, ThirdSalaryIncreaseDate = ?, 
                    FourthSalaryIncrease = ?, FourthSalaryIncreaseDate = ?
                WHERE NationalCode = ?
            """

            # پارامترها برای UPDATE
            params_update = (
                current_rank_id, promotion_date, next_rank_id,
                next_promotion_date, seniority_days, deduction_days,
                rank_type, temporary_rank_count, promotion_description,
                inquiries, adjustment_rank_id, adjustment_seniority_days,
                promotion_stages, first_salary_increase, first_salary_increase_date,
                second_salary_increase, second_salary_increase_date,
                third_salary_increase, third_salary_increase_date,
                fourth_salary_increase, fourth_salary_increase_date,
                national_code
            )

            # کوئری برای درج
            insert_query = """
                INSERT INTO Promotions (NationalCode, CurrentRank, PromotionDate, 
                    NextRank, NextPromotionDate, SeniorityDays, DeductionDays, 
                    RankType, TemporaryRankCount, PromotionDescription, 
                    Inquiries, AdjustmentRankID, AdjustmentSeniorityDays, 
                    PromotionStages, FirstSalaryIncrease, FirstSalaryIncreaseDate, 
                    SecondSalaryIncrease, SecondSalaryIncreaseDate, 
                    ThirdSalaryIncrease, ThirdSalaryIncreaseDate, 
                    FourthSalaryIncrease, FourthSalaryIncreaseDate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # پارامترها برای INSERT
            params_insert = (
                national_code, current_rank_id, promotion_date,
                next_rank_id, next_promotion_date, seniority_days,
                deduction_days, rank_type, temporary_rank_count,
                promotion_description, inquiries, adjustment_rank_id,
                adjustment_seniority_days, promotion_stages,
                first_salary_increase, first_salary_increase_date,
                second_salary_increase, second_salary_increase_date,
                third_salary_increase, third_salary_increase_date,
                fourth_salary_increase, fourth_salary_increase_date
            )

            # بررسی وجود رکورد
            query = "SELECT * FROM Promotions WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if not result:
                print(f"No promotions info found for the National Code: {national_code}. Inserting new record.")
                # اگر رکورد وجود ندارد، درج کن
                self.db_manager.execute_query(insert_query, params_insert)
            else:
                print(f"Promotions info found for the given National Code: {national_code}. Updating record.")
                # اگر رکورد وجود دارد، به‌روزرسانی کن
                self.db_manager.execute_query(update_query, params_update)

            messagebox.showinfo("Success", "اطلاعات ارتقاء با موفقیت ذخیره شد.")

        except Exception as e:
            logging.error(f"Error saving promotions info: {e}")
            messagebox.showerror("Error", str(e))

    def save_family_info(self):
        try:
            # جمع‌آوری اطلاعات از فیلدها
            national_code = self.family_fields["NationalCode"].get()
            latest_marriage_date = self.family_fields["LatestMarriageDate"].get()
            total_dependents = self.family_fields["TotalDependents"].get()
            total_children = self.family_fields["TotalChildren"].get()
            total_daughters = self.family_fields["TotalDaughters"].get()
            total_sons = self.family_fields["TotalSons"].get()

            # تبدیل مقادیر به نوع مناسب
            total_dependents = int(total_dependents) if total_dependents.isdigit() else None
            total_children = int(total_children) if total_children.isdigit() else None
            total_daughters = int(total_daughters) if total_daughters.isdigit() else None
            total_sons = int(total_sons) if total_sons.isdigit() else None

            # کوئری برای به‌روزرسانی
            update_query = """
                UPDATE Dependents
                SET MarriageDate = ?, -- تاریخ ازدواج
                    -- تعداد اعضای خانوار در جدول Dependents ذخیره نمی‌شود، به همین دلیل این بخش را حذف می‌کنیم
                WHERE FamilyNationalCode = ?
            """

            # پارامترها برای UPDATE
            params_update = (
                latest_marriage_date, national_code
            )

            # کوئری برای درج
            insert_query = """
                INSERT INTO Dependents (FamilyNationalCode, MarriageDate)
                VALUES (?, ?)
            """

            # پارامترها برای INSERT
            params_insert = (
                national_code, latest_marriage_date
            )

            # بررسی وجود رکورد
            query = "SELECT * FROM Dependents WHERE FamilyNationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if not result:
                print(f"No family info found for the given National Code: {national_code}. Inserting new record.")
                # اگر رکورد وجود ندارد، درج کن
                self.db_manager.execute_query(insert_query, params_insert)
            else:
                print(f"Family info found for the given National Code: {national_code}. Updating record.")
                # اگر رکورد وجود دارد، به‌روزرسانی کن
                self.db_manager.execute_query(update_query, params_update)

            messagebox.showinfo("Success", "اطلاعات خانوادگی با موفقیت ذخیره شد.")

        except Exception as e:
            logging.error(f"Error saving family info: {e}")
            messagebox.showerror("Error", str(e))

    def save_sanavat_info(self):
        try:
            # جمع‌آوری اطلاعات از فیلدها
            national_code = self.sanavat_fields["NationalCode"].get()
            hire_date_first = self.sanavat_fields["HireDateFirst"].get()
            hire_date_official = self.sanavat_fields["HireDateOfficial"].get()
            hire_date_purchase_service = self.sanavat_fields["HireDatePurchaseService"].get()
            termination_date = self.sanavat_fields["TerminationDate"].get()

            # تبدیل مقادیر به نوع مناسب
            # بررسی فیلدهای تاریخ، در صورت خالی بودن مقدار None تنظیم می‌شود
            hire_date_first = hire_date_first if hire_date_first else None
            hire_date_official = hire_date_official if hire_date_official else None
            hire_date_purchase_service = hire_date_purchase_service if hire_date_purchase_service else None
            termination_date = termination_date if termination_date else None

            # کوئری برای به‌روزرسانی اطلاعات
            update_query = """
                UPDATE SanavatInfo
                SET HireDateFirst = ?, 
                    HireDateOfficial = ?, 
                    HireDatePurchaseService = ?, 
                    TerminationDate = ?
                WHERE NationalCode = ?
            """

            # پارامترهای کوئری برای UPDATE
            params_update = (
                hire_date_first, hire_date_official, hire_date_purchase_service, termination_date, national_code
            )

            # کوئری برای درج اطلاعات
            insert_query = """
                INSERT INTO SanavatInfo (NationalCode, HireDateFirst, HireDateOfficial, HireDatePurchaseService, TerminationDate)
                VALUES (?, ?, ?, ?, ?)
            """

            # پارامترهای کوئری برای INSERT
            params_insert = (
                national_code, hire_date_first, hire_date_official, hire_date_purchase_service, termination_date
            )

            # بررسی وجود رکورد
            query = "SELECT * FROM SanavatInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            # بررسی نتیجه کوئری
            if not result:
                print(f"No Sanavat info found for the given National Code: {national_code}. Inserting new record.")
                # اگر رکوردی وجود ندارد، درج رکورد جدید
                self.db_manager.execute_query(insert_query, params_insert)
            else:
                print(f"Sanavat info found for the given National Code: {national_code}. Updating record.")
                # اگر رکوردی وجود دارد، به‌روزرسانی اطلاعات
                self.db_manager.execute_query(update_query, params_update)

            messagebox.showinfo("Success", "اطلاعات سنوات با موفقیت ذخیره شد.")

        except Exception as e:
            logging.error(f"Error saving Sanavat info: {e}")
            messagebox.showerror("Error", str(e))

    def save_employment_infow(self):
        try:
            # جمع‌آوری اطلاعات از فیلدها
            national_code = self.national_code
            base_code = self.employment_fields["BaseCode"].get()
            employment_status = self.employment_fields["EmploymentStatusID"].get()
            law_based_employment = self.employment_fields["LawBasedEmploymentID"].get()
            expertise = self.employment_fields["ExpertiseID"].get()
            service_location = self.employment_fields["ServiceLocationID"].get()
            current_membership_type = self.employment_fields["CurrentMembershipTypeID"].get()
            entry_transfer_date = self.employment_fields["EntryTransferDate"].get()

            gender_id = self.GenderID_data_dict.get(self.personal_fields['GenderID'].get(), None)
            marital_status_id = self.MaritalStatusID_data_dict.get(self.personal_fields['MaritalStatusID'].get(), None)
            religion_id = self.ReligionID_data_dict.get(self.personal_fields['ReligionID'].get(), None)
            blood_group_id = self.BloodGroupID_data_dict.get(self.personal_fields['BloodGroupID'].get(), None)


            # چاپ مقادیر ورودی برای دیباگینگ

            # تبدیل مقادیر به نوع مناسب
            base_code_id = self.BaseCode_data_dict.get(self.employment_fields['BaseCode'].get(), None)
            employment_status_id = self.EmploymentStatusID_data_dict.get(self.employment_fields['EmploymentStatusID'].get(), None)
            law_based_employment_id = self.LawBasedEmploymentID_data_dict.get(self.employment_fields['LawBasedEmploymentID'].get(), None)
            expertise_id = self.ExpertiseID_data_dict.get(expertise)
            service_location_id = self.ServiceLocationID_data_dict.get(service_location)
            current_membership_type_id = self.CurrentMembershipTypeID_data_dict.get(current_membership_type)

            if employment_status_id is None:
                raise ValueError("Invalid value provided for EmploymentStatukhniohonoisID")
            if law_based_employment_id is None:
                raise ValueError("Invalid value provided for LawBasedEmploymentID")
            if expertise_id is None:
                raise ValueError("Invalid value provided for ExpertiseID")
            if base_code_id is None:
                raise ValueError("Invalid value provided for BaseCode")
            # چاپ مقادیر ID برای دیباگینگ
            # بررسی معتبر بودن شناسه‌ها
            if (employment_status_id is None or law_based_employment_id is None or
                    expertise_id is None or base_code_id is None):
                raise ValueError(
                    "Invalid values provided for EmploymentStatusID, LawBasedEmploymentID, ExpertiseID, or BaseCode")

            # ادامه کد برای به‌روزرسانی یا درج رکورد
            ...

        except Exception as e:
            logging.error(f"Error saving employment info: {e}")
            messagebox.showerror("Error", str(e))

    def save_employment_info(self):
        try:
            # دریافت و اعتبارسنجی اطلاعات از فیلSدهای ورودی
            national_code = self.employment_fields['NationalCode'].get()
            base_code = self.employment_fields['BaseCode'].get()
            employment_status_id = self.EmploymentStatusID_data_dict.get(
                self.employment_fields['EmploymentStatusID'].get())
            law_based_employment_id = self.LawBasedEmploymentID_data_dict.get(
                self.employment_fields['LawBasedEmploymentID'].get())
            expertise_id = self.ExpertiseID_data_dict.get(self.employment_fields['ExpertiseID'].get())
            service_location_id = self.ServiceLocationID_data_dict.get(
                self.employment_fields['ServiceLocationID'].get())
            operational_support_role = self.employment_fields['OperationalSupportRole'].get()
            initial_membership_type_id = self.InitialMembershipTypeID_data_dict.get(
                self.employment_fields['InitialMembershipTypeID'].get())
            hiring_unit_id = self.HiringUnitID_data_dict.get(self.employment_fields['HiringUnitID'].get())
            current_membership_type_id = self.CurrentMembershipTypeID_data_dict.get(
                self.employment_fields['CurrentMembershipTypeID'].get())
            latest_service_status_id = self.LatestServiceStatusID_data_dict.get(
                self.employment_fields['LatestServiceStatusID'].get())
            entry_transfer_date = self.employment_fields['EntryTransferDate'].get()
            state_id = self.StateID_data_dict.get(self.employment_fields['StateID'].get())
            county_id = self.CountyID_data_dict.get(self.employment_fields['CountyID'].get())
            organization_id = self.OrganizationID_data_dict.get(self.employment_fields['OrganizationID'].get())
            deputy_center_id = self.DeputyCenterID_data_dict.get(self.employment_fields['DeputyCenterID'].get())
            subdivision_management_id = self.SubdivisionManagementID_data_dict.get(
                self.employment_fields['SubdivisionManagementID'].get())
            section_department_id = self.SectionDepartmentID_data_dict.get(
                self.employment_fields['SectionDepartmentID'].get())
            mission_location_id = self.MissionLocationID_data_dict.get(
                self.employment_fields['MissionLocationID'].get())
            last_status_id = self.LastStatusID_data_dict.get(self.employment_fields['LastStatusID'].get())
            # بررسی وجود رکورد بر اساس کد ملی
            check_query = "SELECT * FROM EmploymentInfo WHERE NationalCode = ?"
            print(check_query)
            if service_location_id is None:
                city_id = 1
            state_id =1
            county_id=1
            result = self.db_manager.fetch_one(check_query, (national_code,))

            # پارامترهای مشترک برای درج یا به‌روزرسانی
            params = (
                national_code, base_code, employment_status_id, law_based_employment_id, expertise_id,
                service_location_id, operational_support_role, initial_membership_type_id, hiring_unit_id,
                current_membership_type_id, latest_service_status_id, entry_transfer_date, state_id,
                county_id, organization_id, deputy_center_id, subdivision_management_id, section_department_id,
                mission_location_id, last_status_id
            )

            # اگر رکورد وجود ندارد، درج می‌کند؛ در غیر این صورت به‌روزرسانی
            if result is None:
                insert_query = """
                    INSERT INTO EmploymentInfo (NationalCode, BaseCode, EmploymentStatusID, LawBasedEmploymentID, 
                        ExpertiseID, ServiceLocationID, OperationalSupportRole, InitialMembershipTypeID, HiringUnitID, 
                        CurrentMembershipTypeID, LatestServiceStatusID, EntryTransferDate, StateID, CountyID, OrganizationID, 
                        DeputyCenterID, SubdivisionManagementID, SectionDepartmentID, MissionLocationID, LastStatusID) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                self.db_manager.execute_query(insert_query, params)
            else:
                update_query = """
                    UPDATE EmploymentInfo SET 
                        BaseCode = ?, EmploymentStatusID = ?, LawBasedEmploymentID = ?, ExpertiseID = ?, 
                        ServiceLocationID = ?, OperationalSupportRole = ?, InitialMembershipTypeID = ?, 
                        HiringUnitID = ?, CurrentMembershipTypeID = ?, LatestServiceStatusID = ?, 
                        EntryTransferDate = ?, StateID = ?, CountyID = ?, OrganizationID = ?, 
                        DeputyCenterID = ?, SubdivisionManagementID = ?, SectionDepartmentID = ?, 
                        MissionLocationID = ?, LastStatusID = ?
                    WHERE NationalCode = ?
                """
                # افزودن کد ملی به انتهای پارامترها برای WHERE
                update_params = params[1:] + (national_code,)
                self.db_manager.execute_query(update_query, update_params)

            # نمایش پیام موفقیت
            self.show_success_notification("اطلاعات شغلی با موفقیت ذخیره شد.")

        except Exception as e:
            # ثبت خطا و نمایش پیام خطا
            logging.error(f"Save Error: Error saving employment info: {e}")
            self.show_error_message("خطا در ذخیره اطلاعات شغلی: " + str(e))

    def save_employee_bank_details(self):
        try:
            national_code = self.sanavat_fields["NationalCode"].get()
            # گرفتن مقادیر از فیلدها
            bank_name = self.bank_fields["BankNameID"].get()
            branch_name = self.bank_fields["BranchName"].get()
            account_number = self.bank_fields["AccountNumber"].get()
            account_type = self.bank_fields["AccountTypeID"].get()
            card_number = self.bank_fields["CardNumber"].get()
            iban = self.bank_fields["IBAN"].get()

            # ساخت کوئری برای ذخیره‌سازی
            query = """
                INSERT INTO EmployeeBankDetails (NationalCode, BankNameID, BranchName, AccountNumber, AccountTypeID, CardNumber, IBAN)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.db_manager.execute_query(query,  (national_code, bank_type, bank_name, branch_name, account_number, account_type, card_number, iban))
            #self.db_manager.execute(query, (national_code, bank_type, bank_name, branch_name, account_number, account_type, card_number, iban))
            print("Bank details saved successfully.")

        except Exception as e:
            logging.error(f"Error saving bank details: {e}")
            print(f"save_employee_bank_details  Error: {e}")

    def save_job_info(self):
        try:
            # گرفتن مقادیر از فیلدها
            national_code = self.national_code
            job_title = self.job_fields["JobTitle"].get()

            # بررسی و تبدیل مقادیر به int با مدیریت خطا
            job_id = self.safe_int(self.job_fields["JobID"].get())
            post_key = self.safe_int(self.job_fields["PostKey"].get())
            job_level = self.safe_int(self.job_fields["JobLevel"].get())
            job_group_id = self.safe_int(self.job_fields["JobGroupID"].get())
            work_location_id = self.safe_int(self.job_fields["WorkLocationID"].get())
            appointment_date = self.job_fields["AppointmentDate"].get()
            appointment_type_id = self.safe_int(self.job_fields["AppointmentTypeID"].get())
            degree_id = self.safe_int(self.job_fields["DegreeID"].get())
            access_level_id = self.safe_int(self.job_fields["AccessLevelID"].get())
            job_type_id = self.safe_int(self.job_fields["JobTypeID"].get())
            department_id = self.safe_int(self.job_fields["DepartmentID"].get())
            job_rank_id = self.safe_int(self.job_fields["JobRankID"].get())
            section_id = self.safe_int(self.job_fields["SectionID"].get())

            # بررسی مقداردهی فیلدهای اجباری
            if job_id is None or national_code == "":
                print("Job ID یا National Code خالی است. لطفاً تمام فیلدهای ضروری را پر کنید.")
                return

            # ساخت کوئری برای ذخیره‌سازی
            query = """
                INSERT INTO JobInfo (NationalCode, JobTitle, JobID, PostKey, JobLevel, JobGroupID, WorkLocationID, AppointmentDate, AppointmentTypeID, DegreeID, AccessLevelID, JobTypeID, DepartmentID, JobRankID, SectionID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.db_manager.execute_query(query, (
                national_code, job_title, job_id, post_key, job_level, job_group_id, work_location_id,
                appointment_date, appointment_type_id, degree_id, access_level_id, job_type_id, department_id,
                job_rank_id, section_id
            ))

            print("Job details saved successfully.")

        except Exception as e:
            logging.error(f"Error saving job details: {e}")
            print(f"Database Error: {e}")
            messagebox.showerror("Error", f"Error in save_job_info: {e}")



    # def create_educationinfos_tab(self):
    #     # ساخت فرم اطلاعات تحصیلی
    #
    #     self.education_tab = self.tabs_dict["تحصیلات"]
    #     self.education_tab.grid(row=0, column=0, sticky='nsew')
    #
    #     # فیلدهای جدول و برچسب‌ها
    #     labels = [
    #         "کد ملی", "مدرک تحصیلی", "رشته", "مقطع تحصیلی",
    #         "شهر", "دانشگاه محل تحصیل", "تاریخ اخذ مدرک", "نوع مدرک تحصیلی",
    #         "مقطع ایثارگری", "معدل", "مدرک تحصیلی بدو استخدام", "تحصیلات نظامی", "محل تحصیل نظامی"
    #     ]
    #
    #
    #
    #     # ایجاد ردیف‌های داده
    #     for i, (label_text, field_name) in enumerate(zip(labels, self.field_names)):
    #         label = tk.Label(self.education_tab, text=label_text)
    #         label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
    #
    #         entry = tk.Entry(self.education_tab, width=30)
    #         entry.grid(row=i, column=1, padx=5, pady=5)
    #         self.education_fields[field_name] = entry
    #
    #     # دکمه‌های عملیات
    #     load_button = tk.Button(self.education_tab, text="بارگذاری اطلاعات", command=self.load_education_info)
    #     load_button.grid(row=len(labels), column=0, padx=5, pady=5)
    #
    #     save_button = tk.Button(self.education_tab, text="ذخیره اطلاعات", command=self.save_education_info)
    #     save_button.grid(row=len(labels), column=1, padx=5, pady=5)

    def fill_education_info(self, data):
        # پر کردن فیلدها با داده‌های دریافتی
        for i, field_name in enumerate(self.education_fields):
            entry = self.education_fields[field_name]
            entry_value = data[i + 1] if data[i + 1] is not None else ""  # i+1 چون اولین مقدار ID است
            entry.delete(0, tk.END)
            entry.insert(0, entry_value)
            if field_name == "NationalCode":
                entry.config(state='disabled')  # غیرفعال کردن فیلد کد ملی

    def load_education_info(self):
        # بارگذاری اطلاعات تحصیلی از پایگاه داده
        national_code = self.education_fields["NationalCode"].get()

        try:
            query = "SELECT * FROM EducationInfo WHERE NationalCode = ?"
            result = self.db_manager.fetch_one(query, (national_code,))

            if not result:
                messagebox.showinfo("اطلاعات", f"اطلاعاتی برای کد ملی {national_code} یافت نشد.")
                return

            self.fill_education_info(result)

        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بارگذاری اطلاعات تحصیلی: {e}")

    def save_education_info(self):
        # ذخیره اطلاعات تحصیلی به پایگاه داده
        data = [self.education_fields[field_name].get() for field_name in self.education_fields]

        # بررسی خالی نبودن کد ملی
        if not data[0]:
            messagebox.showerror("خطا", "کد ملی نمی‌تواند خالی باشد.")
            return

        # ساخت کوئری ذخیره‌سازی یا به‌روزرسانی
        query = """
            MERGE INTO EducationInfos AS target
            USING (SELECT ? AS NationalCode) AS source
            ON target.NationalCode = source.NationalCode
            WHEN MATCHED THEN
                UPDATE SET
                    EducationLevelID = ?, Major = ?, DegreeLevelID = ?, City = ?, UniversityID = ?,
                    GraduationDate = ?, DegreeTypeID = ?, IserID = ?,Gerayesh=?, GPA = ?, EmploymentDegreeLevelID = ?,
                    MilitaryEducation = ?, MilitaryEducationLocation = ?
            WHEN NOT MATCHED THEN
                INSERT (NationalCode, EducationLevelID, Major, DegreeLevelID, City, UniversityID,
                        GraduationDate, DegreeTypeID, IserID,Gerayesh, GPA, EmploymentDegreeLevelID,
                        MilitaryEducation, MilitaryEducationLocation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        params = data[1:] + data  # پارامترها دوبار استفاده می‌شوند برای INSERT و UPDATE

        try:
            self.db_manager.execute_query(query, params)
            messagebox.showinfo("موفقیت", "اطلاعات با موفقیت ذخیره شد.")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ذخیره اطلاعات تحصیلی: {e}")
