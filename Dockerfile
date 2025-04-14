# 1. انتخاب تصویر پایه
FROM python:3.11-slim

# 2. نصب ابزارهای کمکی
RUN apt-get update && apt-get install -y netcat-openbsd

# 3. تنظیم دایرکتوری کاری
WORKDIR /app

# 4. کپی کردن فایل‌ها
COPY . .

# 5. نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# 6. پورت پیش‌فرض
EXPOSE 8000

# 7. دستور اجرا
CMD ["sh", "-c", "./wait-for.sh db:5432 -- python manage.py runserver 0.0.0.0:8000"]
