# راهنمای استقرار ابری NACA Airfoil Kit Pro – نسخه وب

## وضعیت فعلی

نسخه وب **Streamlit** در محیط اجرایی موقت راه‌اندازی و بررسی شده است. این محیط برای آزمایش و نمایش مناسب است، اما با پایان نشست یا خوابیدن محیط اجرایی دائمی نخواهد بود. برای استقرار پایدار، فایل‌های `Dockerfile`، `docker-compose.yml` و `requirements.txt` به پروژه افزوده شده‌اند.

## پیش‌نیازهای سرور پایدار

سرور Ubuntu 22.04/24.04 یا هر سرویس ابری سازگار با Docker باید این موارد را داشته باشد:

- Docker Engine نسخه 24 یا بالاتر
- Docker Compose Plugin نسخه 2 یا بالاتر
- پورت 8501 باز، یا یک Reverse Proxy با HTTPS در جلو سرویس
- حداقل 1 گیگابایت حافظه RAM برای اجرای پایدار رابط وب و نمودارهای Matplotlib

## استقرار با Docker Compose

```bash
git clone https://github.com/Ali-Marandi/naca-airfoil-kit.git
cd naca-airfoil-kit
docker compose up -d --build
docker compose ps
```

پس از سالم شدن سرویس، رابط وب از نشانی زیر در دسترس است:

```text
http://YOUR_SERVER_IP:8501
```

برای مشاهده وضعیت و گزارش‌ها:

```bash
docker compose logs -f
docker compose ps
curl http://127.0.0.1:8501/_stcore/health
```

برای به‌روزرسانی نسخه:

```bash
git pull
docker compose up -d --build
docker image prune -f
```

## استقرار HTTPS پشت Reverse Proxy

برای محیط عملیاتی، پورت 8501 را مستقیماً در اینترنت قرار ندهید. یک دامنه، گواهی TLS معتبر و reverse proxy مانند Nginx یا Caddy در جلو سرویس قرار دهید. مسیرهای WebSocket باید بدون تغییر به سرویس Streamlit پاس داده شوند.

نمونه پیکربندی ساده Nginx:

```nginx
server {
    listen 80;
    server_name airfoil.example.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

پس از فعال‌سازی HTTPS، دسترسی عمومی باید از این الگو باشد:

```text
https://airfoil.example.com
```

## بررسی سلامت و بازیابی

فایل `docker-compose.yml` شامل `restart: unless-stopped` و health check داخلی است. بنابراین پس از راه‌اندازی مجدد سرور، کانتینر به‌صورت خودکار اجرا خواهد شد. وضعیت سلامت سرویس را با دستور زیر بررسی کنید:

```bash
docker inspect --format='{{.State.Health.Status}}' naca-airfoil-kit-pro
```

## نکات داده و امنیت

- نسخه وب فعلی به فایل `uiuc_database.json` متکی است و هنگام build در image قرار می‌گیرد.
- داده‌های تحلیل در این نسخه در حافظه جلسه کاربر تولید می‌شوند. پیش از فعال‌سازی ذخیره‌سازی ابری واقعی، باید API احراز هویت، پایگاه داده و مدیریت کلیدهای محرمانه اضافه شود.
- کلیدهای API یا توکن‌ها را هرگز داخل Git، فایل `Dockerfile` یا رابط Streamlit قرار ندهید؛ آن‌ها را فقط از طریق secret manager یا متغیرهای محیطی سرور تزریق کنید.

## آزمون محلی

برای اجرای بدون Docker:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

سپس مرورگر را در `http://localhost:8501` باز کنید.
