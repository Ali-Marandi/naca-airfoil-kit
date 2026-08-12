# استقرار بدون کارت NACA Airfoil Kit Pro – نسخه وب

## گزینهٔ پیشنهادی: Streamlit Community Cloud

برای نسخه وب موجود، **Streamlit Community Cloud** مناسب‌ترین مسیر بدون کارت است. این سرویس به‌صورت رایگان اپلیکیشن‌های Streamlit را مستقیماً از مخزن GitHub اجرا می‌کند، نگه‌داری کانتینر را انجام می‌دهد و با هر `git push` تغییرات را به‌روزرسانی می‌کند. این روش از همان فایل‌های موجود پروژه یعنی `app.py` و `requirements.txt` استفاده می‌کند و نیازی به Docker، کارت پرداخت یا تغییر معماری ندارد.

### پیش‌نیازهای آماده‌شده در مخزن

| مورد | وضعیت | توضیح |
|---|---|---|
| `app.py` | آماده | نقطهٔ ورود رابط Streamlit |
| `requirements.txt` | آماده | وابستگی‌های Python شامل Streamlit، NumPy و Matplotlib |
| `.streamlit/config.toml` | آماده | تم و تنظیمات عمومی؛ پورت ثابت حذف شده تا با سرویس‌های ابری سازگار باشد |
| مخزن GitHub | عمومی | `Ali-Marandi/naca-airfoil-kit` روی شاخه `main` |

### مراحل استقرار

1. وارد [Streamlit Community Cloud](https://share.streamlit.io/) شوید و با حساب GitHub خود ادامه دهید.
2. گزینه **Create app** را انتخاب کنید.
3. این مقادیر را وارد کنید:

| فیلد | مقدار |
|---|---|
| Repository | `Ali-Marandi/naca-airfoil-kit` |
| Branch | `main` |
| Main file path | `app.py` |
| App URL (پیشنهادی) | `naca-airfoil-kit-pro`، در صورت آزادبودن |

4. روی **Deploy** کلیک کنید. پس از نصب وابستگی‌ها، یک نشانی عمومی از الگوی زیر دریافت می‌کنید:

```text
https://naca-airfoil-kit-pro.streamlit.app
```

### مدیریت پس از استقرار

هر تغییر جدید در شاخه `main` به‌طور خودکار برنامه را به‌روزرسانی می‌کند. گزارش‌های build، گزینه Reboot و تنظیمات مشاهده‌کنندگان از داشبورد Streamlit Community Cloud قابل مدیریت است. برنامه را با داده‌های عمومی نگه دارید و هر کلید API آینده را فقط از بخش **Secrets** همان سرویس وارد کنید، نه در GitHub.

> سرویس رایگان برای دمو، نمونه‌کار و استفاده سبک مناسب است. برای SLA، دامنه سفارشی سازمانی، کاربر هم‌زمان زیاد یا بار محاسباتی دائمی، باید بعداً به یک سرویس تجاری یا VPS ارتقا داد.

## گزینهٔ پشتیبان: Hugging Face Spaces

اگر Streamlit Community Cloud در دسترس نبود، [Hugging Face Spaces](https://huggingface.co/new-space) گزینهٔ جایگزین است. هنگام ساخت Space، SDK را **Streamlit** انتخاب کنید. مستندات رسمی Hugging Face برای Spaces مبتنی بر Streamlit تأکید می‌کند که پورت پیش‌فرض 8501 باید حفظ شود؛ فایل پیکربندی فعلی پروژه به همین دلیل پورت را به‌صورت ثابت تنظیم نمی‌کند.

برای این مسیر، یک Space عمومی جدید بسازید و کد پروژه را در مخزن Space قرار دهید. فایل `requirements.txt` موجود برای نصب وابستگی‌ها استفاده می‌شود. از آنجا که Space و GitHub دو مخزن جدا هستند، هماهنگ‌سازی تغییرات باید با push به هر دو مخزن یا با یک workflow اختصاصی انجام شود.

## مواردی که عمداً استفاده نمی‌شوند

| سرویس | دلیل مناسب نبودن در این مرحله |
|---|---|
| Render | درخواست تأیید کارت برای ساخت سرویس در این حساب |
| GitHub Pages | فقط فایل ایستا را میزبانی می‌کند و نمی‌تواند اپلیکیشن Python/Streamlit را اجرا کند |
| Vercel/Netlify | برای اجرای مستقیم Streamlit/Python به معماری serverless یا بازطراحی بک‌اند نیاز دارد |

## منابع رسمی

1. [Streamlit Community Cloud](https://streamlit.io/cloud)
2. [مستندات Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)
3. [مستندات Hugging Face Streamlit Spaces](https://huggingface.co/docs/hub/en/spaces-sdks-streamlit)
