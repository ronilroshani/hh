from cryptography.fernet import Fernet

# خواندن کلید از فایل
with open(r"F:\app\HumanResource\secret.key", "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# خواندن محتوای فایل پیکربندی
with open(r"F:\app\HumanResource\ConnectionString.ini", "rb") as file:
    file_data = file.read()

# رمزنگاری محتوای فایل
encrypted_data = cipher_suite.encrypt(file_data)

# ذخیره اطلاعات رمزنگاری‌شده
with open("config_encrypted.ini", "wb") as file:
    file.write(encrypted_data)

print("✅ فایل config.ini رمزنگاری شد و در config_encrypted.ini ذخیره شد!")
