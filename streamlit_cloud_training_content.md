## Cover

**استقرار NACA Airfoil Kit Pro در Streamlit Community Cloud**

راهنمای عملی اتصال GitHub، انتشار و نگه‌داری نسخه وب بدون کارت

## Slide 1

**سریع‌ترین مسیر عمومی، Community Cloud است**

- برای اپلیکیشن‌های Streamlit طراحی شده و استقرار را از GitHub انجام می‌دهد.
- مخزن، شاخه و فایل ورودی را انتخاب می‌کنید؛ سرویس build را مدیریت می‌کند.
- تغییرات جدید روی GitHub، نسخه مستقرشده را به‌روزرسانی می‌کنند.
- برای پروژه فعلی، کارت پرداخت یا Docker لازم نیست.

## Slide 2

**چهار فایل، پیش‌نیاز انتشار هستند**

- مخزن عمومی: `Ali-Marandi/naca-airfoil-kit`
- شاخه انتشار: `main`
- فایل ورودی رابط: `app.py`
- وابستگی‌های Python: `requirements.txt`

یادآوری: حساب GitHub باید روی مخزن مجوز **admin** داشته باشد.

## Slide 3

**ابتدا GitHub را به Cloud متصل کنید**

- در `share.streamlit.io` با GitHub وارد شوید.
- از **Workspaces → Connect GitHub account** استفاده کنید.
- در صفحه OAuth گیت‌هاب، گزینه **Authorize streamlit** را تأیید کنید.
- دسترسی به مخزن‌های عمومی برای این پروژه کافی است؛ دسترسی private فقط در صورت نیاز فعال می‌شود.

## Slide 4

**فرم Create app را دقیق پر کنید**

| فیلد | مقدار |
|---|---|
| Repository | `Ali-Marandi/naca-airfoil-kit` |
| Branch | `main` |
| Main file path | `app.py` |
| Custom subdomain | `naca-airfoil-kit-pro` در صورت آزادبودن |

بعد از انتخاب **Yup, I have an app**، مقادیر را دستی وارد کنید و **Deploy** را بزنید.

## Slide 5

**Build را با پنج آزمون کوتاه تأیید کنید**

- صفحه با عنوان NACA Airfoil Kit Pro باز می‌شود.
- NACA 2412 با 100 نقطه تولید می‌شود.
- Cl، Cd و L/D در پنل شاخص‌ها دیده می‌شوند.
- سه تب Geometry، Pressure Distribution و Flow Field کار می‌کنند.
- اگر build شکست خورد، ابتدا `requirements.txt` و log را بررسی کنید.

## Slide 6

**انتشار GitHub، چرخهٔ به‌روزرسانی شماست**

- هر push به `main` نسخه وب را به‌روز می‌کند.
- تغییر وابستگی‌ها build جدیدی را اجرا می‌کند.
- URL عمومی را با تیم یا کاربران به اشتراک بگذارید.
- کلیدها و تنظیمات حساس آینده را در بخش Secrets نگه دارید، نه در GitHub.

## Slide 7

**از دمو تا محصول، با کنترل‌پذیری پیش بروید**

Community Cloud برای نسخه عمومی، آموزشی و نمایش محصول مناسب است. برای SLA، کاربران هم‌زمان زیاد، دامنه سازمانی یا تحلیل‌های سنگین، مسیر بعدی یک سرویس production یا VPS خواهد بود.

## References

[1]: https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account "Connect your GitHub account — Streamlit"
[2]: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy "Deploy your app — Streamlit"
