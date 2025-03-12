import pyodbc
import bcrypt
from getpass import getpass

# تابع برای هش کردن رمز عبور
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# اتصال به دیتابیس
connection_string = "DRIVER={SQL Server};SERVER=YOUR_SERVER;DATABASE=YOUR_DB;UID=YOUR_USER;PWD=YOUR_PASSWORD"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# دریافت نام کاربری و رمز از کاربر
username = input("نام کاربری جدید: ")
password = getpass("رمز عبور: ")  # برای مخفی کردن ورودی رمز عبور

# هش کردن رمز عبور
password_hash = hash_password(password)

# افزودن کاربر به دیتابیس
try:
    cursor.execute("INSERT INTO Users (Username, PasswordHash, Role) VALUES (?, ?, ?)", (username, password_hash, 'admin'))
    conn.commit()
    print("✅ کاربر با موفقیت اضافه شد!")
except Exception as e:
    print(f"❌ خطا در افزودن کاربر: {e}")

conn.close()
