import tkinter as tk
from tkinter import ttk, messagebox


class AccidentsFormold:
    def __init__(self,parent, db_manager, national_code):
        self.parent = parent
        self.db_manager = db_manager  # مدیریت پایگاه داده
        self.national_code = national_code  # کد ملی
        self.window = tk.Toplevel(self.parent)
        self.window.title("مدیریت حوادث")
        self.window.geometry("800x600")
        self.window.configure(bg="#f0f0f0")

        # عنوان
        title_label = tk.Label(self.window, text="مدیریت حوادث", font=("B Nazanin", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # جدول نمایش اطلاعات حوادث
        self.accidents_table = ttk.Treeview(self.window, columns=("ID", "Date", "Type", "Cause", "Document"), show="headings")
        self.accidents_table.heading("ID", text="شناسه")
        self.accidents_table.heading("Date", text="تاریخ حادثه")
        self.accidents_table.heading("Type", text="نوع حادثه")
        self.accidents_table.heading("Cause", text="علت حادثه")
        self.accidents_table.heading("Document", text="مدرک")
        self.accidents_table.column("ID", width=50, anchor="center")
        self.accidents_table.column("Date", width=150, anchor="center")
        self.accidents_table.column("Type", width=150, anchor="center")
        self.accidents_table.column("Cause", width=200, anchor="center")
        self.accidents_table.column("Document", width=200, anchor="center")
        self.accidents_table.pack(fill="both", expand=True, padx=10, pady=10)

        # دکمه‌های عملیات
        buttons_frame = tk.Frame(self.window, bg="#f0f0f0")
        buttons_frame.pack(pady=10)

        add_button = tk.Button(buttons_frame, text="افزودن حادثه", command=self.add_accident, bg="#4CAF50", fg="white")
        add_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(buttons_frame, text="حذف حادثه", command=self.delete_accident, bg="#f44336", fg="white")
        delete_button.grid(row=0, column=1, padx=5)

        refresh_button = tk.Button(buttons_frame, text="بروزرسانی", command=self.refresh_accidents, bg="#2196F3", fg="white")
        refresh_button.grid(row=0, column=2, padx=5)

        # بارگذاری اطلاعات اولیه
        self.refresh_accidents()

    def refresh_accidents(self):
        """بازیابی اطلاعات حوادث از پایگاه داده"""
        for row in self.accidents_table.get_children():
            self.accidents_table.delete(row)

        query = "SELECT * FROM Accidents WHERE NationalCode = ?"
        results = self.db_manager.fetch_all(query, (self.national_code,))
        for accident in results:
            self.accidents_table.insert("", "end", values=accident)

    def add_accident(self):
        """افزودن حادثه جدید"""
        def save_accident():
            accident_date = date_entry.get()
            accident_type = type_entry.get()
            accident_cause = cause_entry.get()
            document = document_entry.get()

            if not accident_date or not accident_type or not accident_cause:
                messagebox.showerror("خطا", "لطفاً تمام مقادیر لازم را وارد کنید.")
                return

            query = """
                INSERT INTO Accidents (NationalCode, AccidentDate, AccidentType, AccidentCause, Document)
                VALUES (?, ?, ?, ?, ?)
            """
            self.db_manager.execute(query, (self.national_code, accident_date, accident_type, accident_cause, document))
            messagebox.showinfo("موفقیت", "حادثه با موفقیت ثبت شد.")
            add_window.destroy()
            self.refresh_accidents()

        # پنجره افزودن حادثه
        add_window = tk.Toplevel(self.window)
        add_window.title("افزودن حادثه")
        add_window.geometry("400x300")
        add_window.configure(bg="#f0f0f0")

        tk.Label(add_window, text="تاریخ حادثه:", bg="#f0f0f0").pack(pady=5)
        date_entry = tk.Entry(add_window, width=30)
        date_entry.pack(pady=5)

        tk.Label(add_window, text="نوع حادثه:", bg="#f0f0f0").pack(pady=5)
        type_entry = tk.Entry(add_window, width=30)
        type_entry.pack(pady=5)

        tk.Label(add_window, text="علت حادثه:", bg="#f0f0f0").pack(pady=5)
        cause_entry = tk.Entry(add_window, width=30)
        cause_entry.pack(pady=5)

        tk.Label(add_window, text="مدرک:", bg="#f0f0f0").pack(pady=5)
        document_entry = tk.Entry(add_window, width=30)
        document_entry.pack(pady=5)

        save_button = tk.Button(add_window, text="ذخیره", command=save_accident, bg="#4CAF50", fg="white")
        save_button.pack(pady=10)

    def delete_accident(self):
        """حذف حادثه انتخاب‌شده"""
        selected_item = self.accidents_table.selection()
        if not selected_item:
            messagebox.showerror("خطا", "لطفاً یک حادثه را انتخاب کنید.")
            return

        accident_id = self.accidents_table.item(selected_item[0], "values")[0]
        query = "DELETE FROM Accidents WHERE AccidentID = ?"
        self.db_manager.execute(query, (accident_id,))
        messagebox.showinfo("موفقیت", "حادثه با موفقیت حذف شد.")
        self.refresh_accidents()
