# چارچوب راهبرد محصول جهانی — NACA Airfoil Kit Pro

**وضعیت:** مبنای تصمیم‌گیری برای تحقیقات بازار و توسعهٔ بعدی
**تاریخ مرجع:** ۱۴ اوت ۲۰۲۶
**طبقه‌بندی:** سند داخلی راهبرد محصول؛ ارقام مالی و اندازهٔ بازار در این سند درج نشده‌اند و در پژوهش مستند بعدی تأمین می‌شوند.

## جمع‌بندی مدیریتی

NACA Airfoil Kit Pro باید به‌عنوان یک **محیط تصمیم‌گیری و غربال‌گری مقدماتی ایرفویل، قابل‌ردیابی و evidence-driven** توسعه یابد، نه به‌عنوان جایگزینی برای CFD viscous، تونل باد یا ابزارهای certification. ارزش پیشنهادی فعلی ترکیب تولید/ورود هندسه، تحلیل سریع، مقایسه، validation، robust multi-Re Pareto، audit trail و مسیر ارتقای solver در یک workflow واحد است.

> اصل غیرقابل‌مذاکره: هر ادعای دقت، «validated»، یا مناسب‌بودن برای تصمیم تولیدی باید به geometry، dataset، محدودهٔ شرایط، solver version و evidence قابل بازبینی متصل باشد.

## تعریف بازار و محصول

| موضوع | تعریف کاری | وضعیت |
|---|---|---|
| دستهٔ محصول | نرم‌افزار مهندسی برای generation، screening، validation-oriented comparison و تحویل study قابل‌ردیابی برای airfoil section | مبتنی بر قابلیت‌های موجود مخزن |
| مسئلهٔ اصلی | کوتاه‌کردن زمان حرکت از هندسه به shortlist قابل‌بازبینی، بدون پنهان‌کردن محدودیت مدل | فرضیهٔ محصول؛ نیازمند مصاحبه و pilot |
| مشتری اولیهٔ پیشنهادی | مهندسان و تیم‌های کوچک طراحی UAV/eVTOL، rotor/propeller، سازندگان آموزشی/پژوهشی و مشاوران aero | فرضیهٔ بخش‌بندی؛ نیازمند اعتبارسنجی بازار |
| کاربر ثانویه | دانشگاه‌ها، آزمایشگاه‌ها و تیم‌های دانشجویی که workflow آموزشی و reproducible می‌خواهند | فرضیهٔ بخش‌بندی؛ نیازمند اعتبارسنجی پرداخت |
| عدم شمول | certification، تحلیل ساختاری، محاسبهٔ بار نهایی، CFD viscous جایگزین‌ناپذیر، یا تصمیم safety-critical بدون evidence بیرونی | واقعیت مهندسی مستند |

## واقعیت‌های محصول در مخزن

| واقعیت مستند | دلالت راهبردی |
|---|---|
| موتور اصلی vortex-panel سبک با drag/stall تجربی است | messaging باید بر **preliminary screening** متمرکز بماند؛ وعدهٔ «دقت نهایی» ممنوع است. |
| Validation Studio، residualهای Cl/Cd و MAE/RMSE/bias موجودند | ارزش محصول می‌تواند بر «اندازه‌گیری فاصلهٔ مدل از evidence» بنا شود. |
| Robustness و robust multi-Re Pareto موجودند | نقطهٔ تمایز اولیه: تصمیم در چند شرایط به‌جای یک نقطهٔ بهینه‌سازی. |
| XFOIL adapter/worker و hardening موجود است اما production deployment هنوز وابسته به secret management، CNI enforcing، image pinning و endpoint داخلی است | این قابلیت باید به‌صورت **roadmap/staged capability** فروخته شود، نه به‌عنوان سرویس production آماده. |
| Windows desktop و Streamlit web هر دو موجودند | مسیر توزیع می‌تواند به ترتیب self-serve web، حرفه‌ای desktop و enterprise/private deployment باشد. |

مستندات مبنا: [`README.md`](README.md)، [`COMMERCIAL_FEATURE_ROADMAP.md`](COMMERCIAL_FEATURE_ROADMAP.md)، [`VALIDATION_GUIDE.md`](VALIDATION_GUIDE.md)، [`SECURITY_AUDIT_XFOIL_WORKER.md`](SECURITY_AUDIT_XFOIL_WORKER.md) و [`PARETO_MULTI_RE_ANALYSIS.md`](PARETO_MULTI_RE_ANALYSIS.md).

## ارزش پیشنهادی و تمایز اولیه

**Core value proposition:** تبدیل سریع geometry به یک study قابل‌ردیابی شامل metricها، محدودیت‌ها، sensitivity و شواهد validation.

**Killer workflow پیشنهادی:** «Import/Generate → compare across Re/roughness → robust Pareto shortlist → validate against reference → export audit package». این workflow باید در onboarding، landing page و بستهٔ pilot محور پیام محصول باشد.

| لایهٔ مزیت | اقدام لازم | معیار موفقیت |
|---|---|---|
| Feature | robust Pareto، QA، validation و export یکپارچه | کاربر در کمتر از ۵ دقیقه یک study قابل‌اشتراک ایجاد کند. |
| Product | audit package و solver provenance | reviewer بتواند geometry، condition و source را بازتولید کند. |
| Distribution | نسخهٔ web قابل‌آزمون + desktop برای workflows محلی | نخستین ارزش بدون نصب یا پرداخت قابل مشاهده باشد. |
| Data | مجموعه‌های curate‌شدهٔ validation با metadata و شرایط | هر study نمونه به data lineage قابل‌رجوع متصل شود. |
| Switching cost | archive پروژه، comparison history و report templates | تیم بتواند decision history خود را در محصول نگه دارد. |
| Structural moat | study datasets + validation outcomes + workflow integration، با رضایت و حریم‌خصوصی مناسب | دادهٔ انباشته کیفیت recommendation و coverage را ارتقا دهد. |

## اصول Global-by-Default

محصول باید به‌صورت انگلیسی‌اول و آمادهٔ localize طراحی شود؛ ترجمه نباید موجب fork شدن محاسبات، validation logic یا report semantics شود. واحدها، currency، تاریخ، فرمت اعشاری، template گزارش و policyهای data residency باید به‌صورت configuration باشند، نه شرط‌های hard-coded در رابط.

در مرحلهٔ کنونی، **بین‌المللی‌سازی به معنی فروش هم‌زمان در همهٔ کشورها نیست**. beachhead باید پس از تحقیق با یک buyer/use case واضح انتخاب شود و هر بازار جدید فقط زمانی اضافه شود که evidence پرداخت، کانال توزیع، وضعیت پرداخت و هزینهٔ support آن تأیید شده باشد.

## قوانین اولویت‌بندی

| دسته | قانون |
|---|---|
| **Now** | اقداماتی که ریسک تصمیم مهندسی یا ریسک خرید را کم می‌کنند: onboarding شفاف، provenance، validation package، solver deployment staging و pilot design. |
| **Next** | constraint-aware optimization، collaboration، private study storage، API versioning و quality flags برای system-level modules. |
| **Later** | wing/rotor performance، marketplace، plugin ecosystem و AI copilot؛ فقط بعد از evidence استفاده و retention. |
| **Maybe** | community یا gamification؛ فقط در صورت مشاهدهٔ اثر بر activation/referral. |
| **Do not do** | ادعاهای certification، AI بدون KPI، marketplace قبل از نقدینگی عرضه/تقاضا و توسعهٔ هم‌زمان چند بازار بدون beachhead. |

## KPIهای اولیه و دروازه‌های تصمیم

| مرحله | North-star / KPI | دروازهٔ عبور |
|---|---|---|
| Activation | درصد کاربران جدیدی که یک study exportable می‌سازند | تعریف baseline از event instrumentation و بهبود معنادار پس از onboarding. |
| First value | زمان تا اولین robust/validation study | اثبات اینکه onboarding کمتر از پنج دقیقه به value می‌رسد. |
| Retention | بازگشت هفتگی تیم‌های pilot و تعداد studyهای تکرارشونده | evidence کافی از workflow recurring، نه صرفاً بازدید آموزشی. |
| Monetization | تبدیل pilot به plan پولی و willingness-to-pay | حداقل چند قرارداد/تعهد پرداختی مستقل از شبکهٔ شخصی. |
| Quality | نسبت studyهایی که provenance کامل دارند و validation coverage آن‌ها | عدم تبدیل محصول به «ماشین نمودار بدون evidence». |

## ریسک‌های اولیه و پاسخ راهبردی

| ریسک | احتمال اولیه | اثر | پاسخ |
|---|---|---|---|
| برداشت نادرست از screening model به‌عنوان solver نهایی | متوسط | بالا | disclosure در UI/export، quality flag و validation gate. |
| رقابت ابزارهای solver بالغ | بالا | بالا | تمرکز روی workflow، traceability، learning curve و pilot use case محدود؛ نه رقابت مستقیم صرف بر دقت solver. |
| نبود willingness-to-pay در مخاطب آموزشی | متوسط | متوسط | جداسازی education/free از commercial pilot و آزمون قیمت قبل از توسعهٔ گسترده. |
| هزینهٔ support و compliance enterprise زودهنگام | متوسط | بالا | self-serve محدود، private deployment مرحله‌ای و عدم تعهد SLA قبل از readiness. |
| دادهٔ validation ناکافی یا ناهم‌شرط | بالا | بالا | curate metadata، ثبت condition و منع label validated بدون زمینه. |

## اقدامات فوری

در مرحلهٔ بعد، تحقیقات بازار و رقبا باید سه پرسش را با منبع معتبر پاسخ دهد: **کدام buyer بیشترین درد و آمادگی پرداخت دارد؛ workflow موجود در کجا شکاف واقعی ایجاد می‌کند؛ و کدام beachhead از نظر کانال، رگولاتوری و قابلیت فروش کم‌ریسک‌تر است.** سپس مدل قیمت‌گذاری و سناریوی مالی باید صرفاً بر مبنای همین segment تعریف شود، نه بر فرض بازار کلی aerospace software.
