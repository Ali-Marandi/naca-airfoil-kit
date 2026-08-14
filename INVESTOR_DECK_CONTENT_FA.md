# محتوای ارائهٔ سرمایه‌گذار — NACA Airfoil Kit Pro

**مخاطب:** سرمایه‌گذار early-stage و design partner
**مبنای زمانی:** ۱۴ اوت ۲۰۲۶
**قاعدهٔ ارائه:** قابلیت‌های product و CI، facts فعلی‌اند؛ market size، customer traction، willingness-to-pay، درآمد، retention و نتایج مصاحبه تا زمان دریافت دادهٔ واقعی، **اثبات‌نشده** باقی می‌مانند.

## Cover

**NACA Airfoil Kit Pro**
**از هندسه تا تصمیم غربال‌گری قابل‌ردیابی**
مسیر آزمایشی برای تبدیل workflow مهندسی اولیه به evidence-ready studies

## Slide 1

### تصمیم مقدماتی aero هنوز پراکنده و کم‌ردیابی است

- در مرحلهٔ concept، geometry، solver، spreadsheet، chart و report اغلب در ابزارها و فایل‌های جداگانه‌اند.
- ابزارهای موجود از free desktop تا CFD حرفه‌ای گسترده‌اند؛ اما دامنهٔ fidelity و workflow آن‌ها یکسان نیست. [1] [2] [3]
- فرصت پیشنهادی، «موتور محاسباتی دیگر» نیست؛ بلکه ایجاد study package قابل‌مرور برای تیم‌های کوچک طراحی است.

**پیام کلیدی:** مسئله‌ای که باید در discovery اثبات شود، درد workflow و handoff است؛ نه علاقهٔ کلی به airfoil analysis.

## Slide 2

### محصول، غربال‌گری را به یک پروندهٔ قابل‌بازبینی تبدیل می‌کند

- Web و desktop در کنار generation/import geometry، polar، QA، validation residual، robustness و Pareto multi-Re ارائه می‌شوند.
- Evidence readiness، نتیجه را به screening-only، informational comparison یا metadata-complete review طبقه‌بندی می‌کند.
- audit manifest هندسه، شرایط و provenance solver را ثبت می‌کند؛ PDF desktop نیز scope/evidence status را نمایش می‌دهد.

**شاهد داخلی:** ۵۷ تست محلی و CI چهارنسخه‌ای Python در آخرین انتشار موفق بوده‌اند. [4]

## Slide 3

### مزیت: تصمیم چندشرایطی، نه انتخاب یک نقطهٔ L/D

- robust multi-Re Pareto به‌جای ranking در یک Reynolds، candidateها را در مجموعهٔ شرایط تعریف‌شده بررسی می‌کند.
- در اجرای تکرارپذیر ۲۴ پروفیل UIUC و Re=100k تا 2.0M، NACA6412 تنها عضو front مدل حاضر بود؛ این فقط نتیجهٔ candidate set و model scope است. [5]
- sensitivity envelope و validation workflow برای نشان‌دادن uncertainty/limitation طراحی شده‌اند، نه پنهان‌کردن آن‌ها.

**پیام کلیدی:** روش محصول، trade-off و evidence gap را قابل‌دیدن می‌کند؛ ادعای recommendation نهایی ندارد.

## Slide 4

### مسیر solver و deployment با guardrail امنیتی ساخته شده است

- XFOIL adapter از allowlist، temporary-directory isolation، timeout و shell-free execution استفاده می‌کند.
- worker FastAPI fail-closed authentication، request quota، headers، non-root container و CI supply-chain artifacts دارد.
- Kubernetes manifest شامل internal service، restricted runtime و DNS-only NetworkPolicy است؛ production به CNI enforcing، secret management و image-digest pinning وابسته است. [6]

**پیام کلیدی:** foundation فنی برای fidelity بالاتر وجود دارد؛ production solver service هنوز یک milestone، نه revenue claim است.

## Slide 5

### beachhead پیشنهادی: تیم‌های کوچک UAS/rotor و مشاوران

- FAA، UAS و AAM را در forecast رسمی ۲۰۲۶–۲۰۴۶ خود در نظر می‌گیرد؛ EASA نیز بیش از ۱.۶ میلیون operator ثبت‌شده را گزارش می‌کند. [7] [8]
- این داده‌ها evidence یک ecosystem گسترده‌اند، نه TAM مستقیم نرم‌افزار حاضر.
- ICP اولیه، تیم‌هایی هستند که قبل از CFD/آزمایش به shortlist، handoff و review سریع نیاز دارند.

**پیام کلیدی:** این beachhead یک hypothesis با اطمینان متوسط است و باید با discovery آزموده شود.

## Slide 6

### pricing به‌صورت آزمایش کنترل‌شده، نه price list قطعی

| Offer | Scope مختصر | قیمت آزمایشی |
|---|---|---:|
| Founding Design Partner | ۳ geometry، یک review cycle، evidence package | $1,500 |
| Standard Evidence Pilot | ۵ geometry، robust study، دو check-in | $3,500 |
| Extended Workflow Pilot | workflow mapping و handoff workshop | $5,000 |

- price ladder با scope و support متفاوت همراه است؛ discount بدون concession داده‌ای ممنوع است.
- DesignFOIL، AeroFoil و AirShaper تنها برای context range بررسی شده‌اند؛ محصولات هم‌سطح نیستند. [1] [2] [3]
- هیچ نرخ پرداخت، conversion یا ARR واقعی هنوز ثبت نشده است.

## Slide 7

### cohort پنج‌تایی، سریع‌ترین مسیر از فرضیه به evidence است

- دو تیم UAS/rotor، یک مشاور aero، یک آزمایشگاه حرفه‌ای و یک candidate جایگزین برای جلوگیری از dropout پیشنهاد می‌شود.
- هر پایلوت چهار هفته، سه جلسهٔ synchronous و scope ثابت دارد.
- gateهای پیشنهادی: paid/LOI از حداقل ۳ partner، activation حداقل ۷۰٪، و حداقل سه evidence package مورد استفاده در review.

| سناریوی ظرفیت | ترکیب | مبلغ ناخالص نمونه |
|---|---|---:|
| حداقل | ۳ × Founding | $4,500 |
| Core | ۲ × Founding + ۲ × Standard | $10,000 |
| Full cohort | ۲ × Founding + ۲ × Standard + ۱ × Extended | $15,000 |

**یادداشت:** مبالغ capacity scenario هستند، نه forecast یا revenue محقق‌شده. [9]

## Slide 8

### discovery status: برنامه وجود دارد، اما evidence مشتری هنوز باید جمع‌آوری شود

- ممیزی مخزن هیچ transcript، CRM export، survey response یا مصاحبهٔ ثبت‌شده‌ای از ۱۰ discovery call پیدا نکرد.
- بنابراین pain ranking، willingness-to-pay، churn risk و conversion فعلاً unknown هستند.
- استاندارد ثبت discovery و gateهای stop/go اکنون آماده‌اند تا feedback به دادهٔ قابل‌استفاده برای محصول تبدیل شود. [10]

**پیام کلیدی:** سرمایه برای feature sprawl درخواست نمی‌شود؛ سرمایه برای اثبات ICP، pricing و repeatable use اختصاص می‌یابد.

## Slide 9

### سرمایه‌گذاری پیشنهادی روی proof points مرحله‌ای متمرکز است

| مرحله | proof point | تصمیم |
|---|---|---|
| Discovery | ۱۰ مصاحبهٔ ساخت‌یافته و ≥۷ پاسخ کامل | confirm/revise ICP |
| Pilot | ۳–۵ partner و ≥۳ paid/LOI | confirm value metric و price corridor |
| Product | activation ≥۷۰٪ و evidence usage ≥۶۰٪ | build private-study / team workflow |
| Scale | repeat study ≥۵۰٪ و referenceable outcomes | آماده‌سازی GTM محدود |

- مسیر مالی/فنی بزرگ‌تر فقط پس از اثبات stage gateها دنبال می‌شود.
- این ساختار، burn روی integrationهای enterprise یا featureهای کم‌تقاضا را محدود می‌کند.

## Slide 10

### درخواست: design partner و سرمایهٔ اعتبارسنجی مرحله‌ای

- معرفی به ۳ تا ۵ تیم UAS/rotor یا مشاور با تصمیم design واقعی در ۹۰ روز آینده.
- پشتیبانی از اجرای discovery، pilot cohort و measurement discipline.
- همراهی برای تبدیل evidence واقعی به product roadmap و pricing قابل‌تکرار.

**هدف:** ساخت مسیر قابل‌اعتماد از geometry به decision؛ ابتدا برای screening، سپس با evidence کافی برای team workflowهای حرفه‌ای‌تر.

## References

[1]: https://www.dreesecode.com/ "DreeseCODE — DesignFOIL"
[2]: https://aerofoilengineering.com/ "AeroFoil Engineering — AeroFoil"
[3]: https://airshaper.com/pricing "AirShaper — Pricing"
[4]: https://github.com/Ali-Marandi/naca-airfoil-kit/actions/runs/31761727717 "GitHub Actions — tests, commit e65f8ee"
[5]: ./PARETO_MULTI_RE_ANALYSIS.md "Robust multi-Re Pareto analysis"
[6]: ./SECURITY_AUDIT_XFOIL_WORKER.md "XFOIL Worker security audit"
[7]: https://www.faa.gov/data_research/aviation/aerospace_forecasts "FAA Aerospace Forecasts"
[8]: https://www.easa.europa.eu/en/domains/civil-drones "EASA — Drones & Air Mobility"
[9]: ./LIMITED_PILOT_EXECUTION_AND_PRICING_PLAN_FA.md "Limited Pilot Execution and Pricing Plan"
[10]: ./PROBLEM_DISCOVERY_EVIDENCE_AUDIT_FA.md "Problem-Discovery Evidence Audit"
