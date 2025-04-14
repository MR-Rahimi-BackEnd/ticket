#!/bin/bash

# ورودی: host:port
hostport="$1"
shift

# استخراج hostname و port از ورودی
host=$(echo "$hostport" | cut -d: -f1)
port=$(echo "$hostport" | cut -d: -f2)

# منتظر ماندن برای آماده شدن دیتابیس
while ! nc -z "$host" "$port"; do
  echo "Waiting for $host:$port..."
  sleep 1
done

# اجرای دستور بعد از آماده شدن دیتابیس
exec "$@"
