# استقرار بدون کارت NACA Airfoil Kit Pro – نسخه وب

**تهیه‌کننده: Manus AI**

## جمع‌بندی اجرایی

برای نسخه وب فعلی، **Streamlit Community Cloud** توصیهٔ اصلی است. این سرویس برای اپلیکیشن‌های Streamlit طراحی شده، رایگان است، با انتخاب مخزن، شاخه و فایل اصلی برنامه استقرار را انجام می‌دهد و پس از هر `git push` برنامه را به‌روزرسانی می‌کند. [1] [2] این مسیر با ساختار حاضر پروژه سازگار است و به Docker، سرور مجازی یا کارت پرداخت نیاز ندارد.

> «Pick a repo, branch, and file» و سپس «Click Deploy»؛ Community Cloud اپلیکیشن را از مخزن GitHub می‌سازد و منتشر می‌کند. [1]

| معیار | Streamlit Community Cloud | Hugging Face Spaces | Render در حساب فعلی |
|---|---|---|---|
| نیاز به کارت پرداخت در مسیر بررسی‌شده | ندارد | مسیر پایهٔ Space عمومی نیازمند کارت نیست | Render پنجرهٔ Add Card و تأیید موقت ۱ دلار نمایش داد |
| سازگاری با `app.py` فعلی | مستقیم | مستقیم، با SDK Streamlit | مستقیم، از Dockerfile |
| منبع کد | مخزن GitHub موجود | مخزن جداگانهٔ Space | مخزن GitHub موجود |
| بهترین کاربرد | استقرار عمومی و سریع همین برنامه | راهکار جایگزین یا نمایش در اکوسیستم Hugging Face | محیط production با کنترل و منابع بیشتر |

## وضعیت فنی آماده‌شده در مخزن

مخزن `Ali-Marandi/naca-airfoil-kit` در شاخه `main` برای Community Cloud آماده شده است. فایل `app.py` نقطهٔ ورود رابط وب است و `requirements.txt` وابستگی‌های Python را تعیین می‌کند. پیکربندی `.streamlit/config.toml` نیز پورت ثابت را حذف کرده است تا هم با Community Cloud و هم با Hugging Face Spaces سازگار بماند. این تصمیم با الزام رسمی Spaces برای استفاده از پورت پیش‌فرض 8501 هم‌راستا است. [3]

| پرونده | نقش در استقرار بدون کارت | وضعیت |
|---|---|---|
| `app.py` | فایل اصلی برنامه Streamlit | آماده |
| `requirements.txt` | نصب Streamlit، NumPy، Matplotlib، Pillow و وابستگی‌های پشتیبان | آماده |
| `.streamlit/config.toml` | تم، اجرای headless و تنظیمات کاربر بدون اجبار پورت | آماده |
| `NO_CARD_DEPLOYMENT.md` | راهنمای عملی و مستند این مسیر | آماده |

## روش پیشنهادی: Streamlit Community Cloud

ابتدا به [Streamlit Community Cloud](https://share.streamlit.io/) بروید و با حساب GitHub وارد شوید. Community Cloud می‌تواند به مخزن‌های عمومی یا خصوصی GitHub متصل شود و اغلب برنامه‌ها را در چند دقیقه اجرا می‌کند. [2] سپس گزینه **Create app** را انتخاب کنید و تنظیمات زیر را وارد نمایید.

| فیلد در فرم Streamlit | مقدار پیشنهادی |
|---|---|
| Repository | `Ali-Marandi/naca-airfoil-kit` |
| Branch | `main` |
| Main file path | `app.py` |
| App URL | `naca-airfoil-kit-pro`، در صورت آزاد بودن |

پس از انتخاب **Deploy**، سرویس وابستگی‌ها را از `requirements.txt` نصب می‌کند و برنامه را اجرا خواهد کرد. نشانی نهایی معمولاً در دامنه `streamlit.app` ارائه می‌شود؛ نام دقیق آن را پلتفرم هنگام ساخت تأیید می‌کند. از این پس، انتشار هر commit جدید روی شاخه `main` به‌روزرسانی برنامه را فعال می‌کند. [1]

## گزینهٔ پشتیبان: Hugging Face Spaces

اگر Community Cloud قابل استفاده نبود، یک Space عمومی در [Hugging Face Spaces](https://huggingface.co/new-space) بسازید و هنگام ایجاد، SDK را **Streamlit** انتخاب کنید. طبق مستندات رسمی، Space از یک مخزن Git تشکیل شده و با `requirements.txt` وابستگی‌ها را نصب می‌کند؛ برای Streamlit باید پورت پیش‌فرض 8501 حفظ شود. [3]

در این مسیر، کد پروژه را به مخزن Space منتقل یا همگام‌سازی می‌کنید. چون Space و GitHub دو مخزن مستقل هستند، هر تغییر آتی باید به Space نیز push شود یا با یک workflow جداگانه همگام‌سازی شود. این روش برای نمایش عمومی مناسب است، اما Community Cloud برای نگه‌داری مستقیم پروژهٔ فعلی ساده‌تر خواهد بود.

## الزامات امنیتی و عملیاتی

نسخه فعلی داده‌های عمومی و فایل `uiuc_database.json` را داخل مخزن دارد. اگر در آینده ذخیره‌سازی ابری واقعی، کلید API یا حساب‌های کاربری به برنامه افزوده شوند، کلیدها نباید در GitHub قرار گیرند. آن‌ها را فقط از بخش Secrets پلتفرم میزبان تزریق کنید. همچنین سرویس‌های بدون کارت برای دمو، نمونه‌کار و استفاده سبک مناسب هستند؛ استقرار تجاری با تضمین در دسترس‌بودن، دامنه سازمانی، ظرفیت کاربران هم‌زمان یا محاسبات سنگین، به یک سرویس پولی یا VPS نیاز خواهد داشت.

## منابع

[1]: https://streamlit.io/cloud "Streamlit Community Cloud"
[2]: https://docs.streamlit.io/deploy/streamlit-community-cloud "Streamlit Community Cloud documentation"
[3]: https://huggingface.co/docs/hub/en/spaces-sdks-streamlit "Hugging Face Streamlit Spaces documentation"
