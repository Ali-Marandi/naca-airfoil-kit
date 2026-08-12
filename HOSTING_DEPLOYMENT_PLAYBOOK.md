# راهنمای عملی استقرار نسخه وب NACA Airfoil Kit Pro

**تهیه‌کننده: Manus AI**  
**هدف: اتصال دقیق مخزن GitHub به Streamlit Community Cloud و تشریح مسیر پشتیبان Hugging Face Spaces**

## تصمیم پیشنهادی

برای اجرای بدون کارت، **Streamlit Community Cloud** مسیر پیشنهادی و قابل اتکا برای این پروژه است. Community Cloud مستقیماً با GitHub متصل می‌شود، به شما اجازه می‌دهد مخزن، شاخه و فایل ورودی را انتخاب کنید و پس از هر تغییر در کد، نسخه مستقرشده را به‌روزرسانی می‌کند. [1] [2] در مقابل، مستندات فعلی Hugging Face نشان می‌دهد که SDKهای فعال Space شامل Gradio، Docker و Static هستند و ساخت Spaceهای محاسباتی Gradio یا Docker نیازمند پلن پولی است؛ بنابراین Hugging Face دیگر گزینهٔ **بدون‌کارتِ تأییدشده** برای این اپ Streamlit نیست. [4]

> «Connecting GitHub to your Streamlit Community Cloud account allows you to deploy apps directly from the files you store in your repositories.» — مستندات Streamlit Community Cloud [1]

| مسیر | توصیه | وضعیت کارت | مناسب برای |
|---|---|---|---|
| Streamlit Community Cloud | **مسیر اصلی** | بدون کارت در مسیر رایگان Community Cloud | اپ عمومی Streamlit، استقرار سریع از GitHub |
| Hugging Face Spaces با Docker | مسیر فنی پشتیبان | طبق مستندات فعلی، ساخت Docker Space نیازمند پلن پولی است | زمانی که حساب HF دارای دسترسی محاسباتی باشد |
| Render | متوقف‌شده برای این هدف | حساب فعلی افزودن کارت را درخواست کرد | محیط production آینده |

## بخش اول — استقرار گام‌به‌گام در Streamlit Community Cloud

### 1. آماده‌سازی مخزن GitHub

مخزن `Ali-Marandi/naca-airfoil-kit` از قبل برای استقرار آماده است. پیش از ورود به Community Cloud، مطمئن شوید شاخهٔ `main` شامل `app.py` و `requirements.txt` باشد. Community Cloud برای استقرار از مخزن به مجوز **admin** روی همان مخزن نیاز دارد. اگر مجوز admin ندارید، باید از مالک مخزن درخواست کنید یا یک fork تحت حساب خود بسازید. [1]

| مورد کنترل | مقدار مورد انتظار در این پروژه | دلیل |
|---|---|---|
| Repository | `Ali-Marandi/naca-airfoil-kit` | منبع رسمی کد |
| Branch | `main` | شاخهٔ انتشار فعلی |
| Entrypoint | `app.py` | فایل رابط Streamlit |
| Dependencies | `requirements.txt` | نصب خودکار کتابخانه‌های Python |
| Secrets | فعلاً لازم نیست | برنامهٔ فعلی کلید محرمانهٔ لازم ندارد |

### 2. ایجاد یا ورود به حساب Community Cloud

به [share.streamlit.io](https://share.streamlit.io/) بروید و با **GitHub** وارد شوید. اگر حساب Streamlit دارید اما GitHub هنوز متصل نیست، از منوی بالای سمت چپ **Workspaces** و سپس **Connect GitHub account** را انتخاب کنید. در GitHub، اطلاعات ورود را وارد کنید و در صفحهٔ OAuth دکمهٔ **Authorize streamlit** را بزنید. این اتصال ابتدا دسترسی به مخزن‌های عمومی را فراهم می‌کند. [1]

برای این مخزن عمومی، تنها همین سطح دسترسی کافی است. اگر بعدها نسخهٔ خصوصی پروژه را مستقر کردید، از مسیر **Settings → Linked accounts → Connect here** سطح دسترسی private repositories را جداگانه تأیید کنید. [1]

### 3. ساخت App جدید

در workspace، گزینهٔ **Create app** را بزنید و در پرسش «Do you already have an app?» گزینهٔ **Yup, I have an app** را انتخاب کنید. سپس مقادیر زیر را در فرم وارد کنید. مستندات Streamlit امکان واردکردن دستی مقادیر یا الصاق URL مستقیم فایل `app.py` در GitHub را نیز پیش‌بینی کرده است. [2]

| فیلد فرم Community Cloud | مقدار دقیق |
|---|---|
| Repository | `Ali-Marandi/naca-airfoil-kit` |
| Branch | `main` |
| Main file path | `app.py` |
| App URL / Custom subdomain | `naca-airfoil-kit-pro`، اگر آزاد است |

اگر نام پیشنهادی در App URL آزاد نباشد، یک نام جایگزین مانند `naca-airfoil-kit-air` انتخاب کنید. در صورت خالی‌گذاشتن این فیلد، Streamlit یک URL یکتا بر پایهٔ نام مالک، مخزن، entrypoint و در صورت لزوم hash ایجاد می‌کند. [2]

### 4. تنظیمات پیشرفته و Secrets

قبل از Deploy می‌توانید **Advanced settings** را باز کنید. Community Cloud به‌صورت پیش‌فرض Python 3.12 را انتخاب می‌کند و از نسخه‌های Python که هنوز به‌روزرسانی امنیتی دریافت می‌کنند پشتیبانی می‌کند. [2] برای این پروژه، Python 3.12 مناسب است؛ بنابراین تنظیم پیش‌فرض را نگه دارید مگر اینکه build log ناسازگاری مشخصی نشان دهد.

در حال حاضر هیچ Secret اجباری وجود ندارد. اگر در آینده اتصال به ذخیره‌سازی ابری واقعی، API تحلیلی یا احراز هویت اضافه شد، مقدارهای حساس را در فیلد **Secrets** وارد کنید. کلیدها و رمزها را هرگز در `app.py`، `requirements.txt` یا GitHub commit نکنید.

### 5. Deploy و بررسی اولیه

روی **Deploy** بزنید. Cloud وابستگی‌ها را نصب می‌کند و build log را نمایش می‌دهد. اغلب برنامه‌ها در چند دقیقه مستقر می‌شوند؛ افزودن یا تغییر وابستگی‌ها ممکن است چند دقیقهٔ دیگر طول بکشد. [2] پس از اتمام، URL عمومی برنامه را باز کنید و این آزمون کوتاه را اجرا نمایید.

| آزمون پذیرش | نتیجهٔ مورد انتظار |
|---|---|
| بارگذاری صفحه | عنوان NACA Airfoil Kit Pro نمایش داده شود |
| تولید هندسه | NACA 2412 با 100 نقطه بدون خطا ایجاد شود |
| تحلیل | مقادیر Cl، Cd و L/D نمایش داده شوند |
| نمودارها | تب‌های Geometry، Pressure Distribution و Flow Field باز شوند |
| پایگاه UIUC | جست‌وجو و انتخاب یک پروفایل عمومی قابل انجام باشد |

### 6. به‌روزرسانی، مشاهدهٔ لاگ و اشتراک‌گذاری

بعد از استقرار اولیه، push جدید به فایل‌های برنامه باید برنامه را به‌روزرسانی کند. تغییر dependency نیز شناسایی و نصب خواهد شد. لاگ‌های build و اجرا در صفحهٔ برنامه قابل مشاهده‌اند، اما خود Streamlit اعلام می‌کند این لاگ‌ها فقط برای کاربران دارای write access به مخزن دیده می‌شوند. [2] URL نهایی را با تیم یا کاربران به اشتراک بگذارید؛ در تنظیمات برنامه نیز امکان تغییر subdomain وجود دارد.

## بخش دوم — بررسی دقیق گزینهٔ Hugging Face Spaces

### وضعیت فعلی و نتیجهٔ بررسی

دو سند رسمی Hugging Face وجود دارد که باید با احتیاط تفسیر شوند. صفحهٔ قدیمی‌تر Streamlit Spaces هنوز یک SDK با مقدار `sdk: streamlit` و پورت 8501 را توضیح می‌دهد. [3] اما مرجع فعلی Spaces SDKها را فقط **Gradio، Docker و Static** معرفی می‌کند و تصریح می‌کند Spaceهای Docker و Gradio برای ایجاد به پلن پولی نیاز دارند. [4] مرجع پیکربندی نیز تنها `gradio`، `docker` و `static` را به‌عنوان مقادیر معتبر `sdk` فهرست می‌کند. [6]

بنابراین برای پروژهٔ جدید، مسیر Streamlit SDK قدیمی را انتخاب نکنید. اگر حساب Hugging Face شما دسترسی پولی یا مجاز به Docker Space دارد، از **Docker Space** استفاده کنید. این یک مسیر فنی پشتیبان است، نه پیشنهاد بدون‌کارت.

### مراحل فنی Docker Space

1. در [Hugging Face New Space](https://huggingface.co/new-space) وارد حساب شوید و یک Space با visibility عمومی بسازید.
2. در بخش SDK، گزینه **Docker** را انتخاب کنید.
3. در مخزن Space، فایل‌های پروژه را push کنید؛ از جمله `app.py`، `airfoil_pro.py`، `uiuc_database.json`، `requirements.txt`، `.streamlit/` و `Dockerfile`.
4. در ابتدای `README.md` مخزن Space، YAML زیر را قرار دهید. Docker Spaces SDK را از metadata فایل README تشخیص می‌دهد و `app_port` پورت در معرض اینترنت را مشخص می‌کند. [5] [6]

```yaml
---
title: NACA Airfoil Kit Pro
emoji: ✈️
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 8501
---
```

5. Dockerfile موجود پروژه، Streamlit را روی 8501 اجرا می‌کند و برای Space مناسب است. اگر Dockerfile دیگری جایگزین شد، باید برنامه را روی همان `app_port` اعلام‌شده اجرا کند.
6. پس از push، Space به‌طور خودکار image را build و برنامه را restart می‌کند. کد هر Space در یک مخزن Git نگه‌داری می‌شود و push جدید موجب rebuild می‌شود. [4]
7. هر secret آینده را در **Settings** همان Space تعریف کنید. Secrets و variables در محیط runtime در دسترس برنامه‌اند و نباید در کد commit شوند. [4] [5]

### محدودیت‌ها و ملاحظات Space

داده‌های روی دیسک Docker Space در restart از بین می‌روند، مگر اینکه از storage مجاز یا یک پایگاه دادهٔ خارجی استفاده شود. [5] همچنین سخت‌افزار رایگان ممکن است پس از عدم استفاده به حالت sleep برود. [4] برای ذخیره‌سازی پروژه‌های کاربران یا قابلیت اشتراک‌گذاری سازمانی، باید یک backend پایدار مانند S3-compatible storage و database مستقل به برنامه اضافه شود.

## بخش سوم — رفع خطاهای رایج

| نشانه | علت محتمل | اقدام پیشنهادی |
|---|---|---|
| مخزن در Streamlit دیده نمی‌شود | GitHub متصل نیست یا مجوز admin ندارید | اتصال GitHub را بررسی کنید؛ روی مخزن admin شوید یا fork بسازید [1] |
| `app.py` در فرم دیده نمی‌شود | پیشنهادهای UI کامل نیستند یا مسیر نادرست است | مسیر `app.py` را دستی وارد کنید [2] |
| build با `ModuleNotFoundError` شکست می‌خورد | کتابخانه در `requirements.txt` ثبت نشده | نام پکیج را اضافه و push کنید |
| UIUC Database خطا می‌دهد | دسترسی اینترنت outbound یا URL منبع مشکل دارد | ابتدا NACA Generator را آزمایش کنید؛ سپس loader و URL داده را بررسی کنید |
| Hugging Face گزینه Streamlit ندارد | SDK فعلی Streamlit در جریان استاندارد Space در دسترس نیست | از Docker Space با `sdk: docker` استفاده کنید یا Streamlit Community Cloud را انتخاب کنید [4] [6] |

## منابع

[1]: https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account "Connect your GitHub account — Streamlit Community Cloud"
[2]: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy "Deploy your app on Community Cloud — Streamlit documentation"
[3]: https://huggingface.co/docs/hub/en/spaces-sdks-streamlit "Streamlit Spaces — Hugging Face documentation"
[4]: https://huggingface.co/docs/hub/en/spaces-overview "Spaces Overview — Hugging Face documentation"
[5]: https://huggingface.co/docs/hub/en/spaces-sdks-docker "Docker Spaces — Hugging Face documentation"
[6]: https://huggingface.co/docs/hub/en/spaces-config-reference "Spaces Configuration Reference — Hugging Face documentation"
