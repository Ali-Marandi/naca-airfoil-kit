# راهنمای عملیاتی Qualification Scorecard برای انتخاب شرکت‌کنندگان پایلوت

**هدف:** انتخاب ۳ تا ۵ design partner که هم مسئلهٔ واقعی دارند و هم می‌توانند در یک پایلوت محدود و screening-only همکاری کنند. این scorecard برای رتبه‌بندی prospectهاست، نه برای ارزیابی فنی محصول یا ارزش‌گذاری مشتری.

## قواعد پیش از امتیازدهی

هر candidate باید ابتدا از سه gate عبور کند. شکست در هر gate به‌معنای `Disqualified` است، حتی اگر مجموع امتیاز بالا باشد.

| Gate | سؤال عملیاتی | Pass | Disqualify / Hold |
|---|---|---|---|
| Scope safety | آیا pilot فقط برای preliminary screening است؟ | مشتری scope notice را می‌پذیرد. | certification، flight release، safety-critical sign-off یا performance guarantee می‌خواهد. |
| Data handling | آیا حداقل geometry/conditions representative بدون نقض محرمانگی قابل‌اشتراک است؟ | دادهٔ حداقلی یا نمونهٔ sanitize‌شده آماده است. | داده/شرایط لازم قابل‌اشتراک نیست یا policy نامشخص است. |
| Operating commitment | آیا champion زمان سه جلسه و close-out را می‌پذیرد؟ | owner و زمان مشخص است. | صرفاً علاقهٔ مبهم یا عدم دسترسی به کاربر اصلی. |

`Hold` به‌جای `Disqualify` زمانی استفاده می‌شود که مشکل با NDA، data-minimization plan یا تعیین owner حل‌شدنی است. Hold نباید بدون تاریخ follow-up بیش از ۱۴ روز باز بماند.

## ابعاد امتیازدهی

هر dimension امتیاز ۰ تا ۲ می‌گیرد. مجموع حداکثر ۱۲ است. امتیاز فقط پس از ثبت evidence کوتاه در همان ردیف معتبر است؛ نمرهٔ بدون شاهد باید `unscored` تلقی شود.

| Dimension | ۰ امتیاز | ۱ امتیاز | ۲ امتیاز | شاهد مورد نیاز |
|---|---|---|---|---|
| تکرار مسئله | کار یک‌باره، آموزشی یا بدون schedule | مسئله دوره‌ای با زمان‌بندی مبهم | تصمیم airfoil/rotor در ۹۰ روز آینده و تکرارشونده | آخرین تصمیم واقعی + timeline |
| ownership | فقط user بدون sponsor | champion اولیه، buyer نامشخص | champion و economic buyer یا مسیر خرید مشخص | نقش‌ها و نام/شناسهٔ ناشناس roleها |
| data readiness | geometry/conditions ندارد | داده ناقص یا نیازمند sanitize | geometry، conditions و review context آماده | checklist data |
| pain / urgency | کنجکاوی یا low priority | pain واقعی، consequence مبهم | deadline، rework، client review یا milestone مشخص | consequence و deadline |
| product fit | نیاز اصلی CFD/certification/enterprise integration | فقط بخشی از workflow fit است | concept screening، comparison یا handoff دقیقاً fit است | job-to-be-done |
| همکاری | feedback نامنظم یا یک جلسه | زمان محدود ولی پاسخگو | kickoff، midpoint و close-out را می‌پذیرد | calendar intent + owner |

## محاسبه و طبقه‌بندی

`Total = Problem Repetition + Ownership + Data Readiness + Pain/Urgency + Product Fit + Collaboration`

| مجموع | طبقه | اقدام استاندارد |
|---:|---|---|
| 10–12 | Priority design partner | پیشنهاد package متناسب، mutual success plan و kickoff |
| 8–9 | Eligible pilot candidate | discovery follow-up، رفع یک شکاف و سپس offer |
| 6–7 | Nurture / diagnostic | onboarding demo یا discovery تکمیلی؛ offer پولی ندهید |
| 0–5 | Do not pursue now | دلیل را ثبت و فقط با trigger جدید بازبینی کنید |

قانون پیشین «۸ یا بیشتر» به‌عنوان threshold eligibility حفظ می‌شود. بازهٔ ۱۰–۱۲ برای تعیین ترتیب allocation ظرفیت ایجاد شده است، نه برای افزایش threshold ورود.

## وزن‌دهی ممنوع و استثناهای کنترل‌شده

مدل پایه بدون weight است تا در cohort کوچک، قضاوت مبهم پیچیده نشود. دو عامل نباید با امتیاز بیشتر جبران شوند: **scope safety** و **data handling**. برای مثال candidate با امتیاز ۱۲ که sign-off safety-critical می‌خواهد، همچنان disqualified است.

اگر بعداً دادهٔ ۱۰ مصاحبه نشان دهد که یک dimension به‌طور سیستماتیک با paid conversion مرتبط است، weight جدید فقط با یک memo نسخه‌دار و بازامتیازدهی همهٔ candidateهای باز اعمال می‌شود. تغییر وزن در میانهٔ انتخاب یک candidate ممنوع است.

## فرآیند امتیازدهی

| مرحله | مسئول | زمان | کنترل کیفیت |
|---|---|---|---|
| Intake | interviewer | حداکثر ۲۴ ساعت پس از گفتگو | fieldهای mandatory تکمیل شوند |
| First score | interviewer | در همان روز | هر نمره شاهد متنی کوتاه داشته باشد |
| Calibration | product lead + interviewer | هفته‌ای یک‌بار | اختلاف بیش از یک امتیاز در هر dimension بحث و ثبت شود |
| Decision | product lead | پس از calibration | status: priority / eligible / nurture / no-go |
| Offer | founder یا owner تجاری | فقط برای priority/eligible | scope و package مطابق scorecard ثبت شود |
| Re-score | interviewer | پس از discovery جدید یا تغییر پروژه | نمرهٔ قبلی باقی بماند، نسخهٔ جدید اضافه شود |

## قواعد تساوی و تخصیص ظرفیت

اگر تعداد candidateهای eligible بیش از ظرفیت بود، ترتیب زیر اعمال می‌شود:

1. مجموع امتیاز بالاتر برنده است.
2. در تساوی، `Pain/Urgency` بالاتر برنده است.
3. سپس `Ownership` و `Data Readiness` بالاتر برنده‌اند.
4. سپس diversity cohort: بخش UAS/rotor، consultant و lab نباید ناخواسته در یک segment متمرکز شوند.
5. در تساوی باقی‌مانده، earliest real decision timeline مقدم است.

هیچ‌گاه با «برند»، آشنایی شخصی، حجم احتمالی آینده یا فشار فروش به scorecard امتیاز اضافه نشود. چنین اطلاعاتی، اگر لازم است، جداگانه در decision note ثبت می‌شود.

## Decision Record نمونه

| فیلد | نمونهٔ درست |
|---|---|
| Candidate ID | `PILOT-C04` |
| Gate status | `Pass` |
| Score | `10/12` |
| Missing point | ownership: economic buyer هنوز جلسه را تأیید نکرده است |
| Key evidence | rotor shortlist برای review مشتری در ۴۵ روز؛ geometry و Re موجود |
| Offer | Standard Evidence Pilot — $3,500 experimental offer |
| Decision | `Priority`؛ kickoff مشروط به buyer call |
| Owner / date | product lead / 2026-08-20 |
| Re-score trigger | عدم تأیید buyer تا ۱۴ روز |

## الگوهای خطای رایج

| خطا | چرا خطرناک است | کنترل |
|---|---|---|
| نمرهٔ high فقط به‌دلیل enthusiasm | علاقه، urgency یا budget نیست | آخرین تصمیم واقعی و timeline الزامی است |
| انتخاب دانشگاه برای اثبات pricing enterprise | economics و procurement متفاوت‌اند | segmentها جدا گزارش شوند |
| امتیازدادن به «مشهور بودن» candidate | bias شبکه‌ای و تعارض با learning objective | نام سازمان در scorecard حذف شود |
| تبدیل pilot به custom consulting | signal محصول با effort دستی مخلوط می‌شود | scope cap و out-of-scope log |
| حذف candidate low-score بدون ثبت | learning lost و selection bias ایجاد می‌شود | reason code الزامی است |

## شاخص‌های صحت scorecard

پس از اجرای cohort، کیفیت ابزار با این سه پرسش بررسی می‌شود: آیا high-scoreها واقعاً activation و follow-up بهتری داشتند؟ آیا rejectهای low-score به‌دلیل درست ثبت‌شده رد شدند؟ آیا یک dimension به‌طور مکرر فاقد evidence بود؟ پاسخ‌ها برای اصلاح نسخهٔ بعدی scorecard استفاده می‌شوند، نه برای بازنویسی گذشته.

## قالب داده

فایل `templates/pilot_qualification_scorecard_template.csv` دارای یک ردیف برای هر candidate و ستون‌های evidence/score/decision است. از آن برای calibration و audit استفاده کنید.
