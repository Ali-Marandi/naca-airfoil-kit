# تحلیل آموزشی cohort فرضی Discovery و Qualification

> **SYNTHETIC DEMO — NOT CUSTOMER EVIDENCE.** این تحلیل فقط از ۱۰ رکورد ساختگیِ دست‌نویس تولید شده است. هیچ‌یک از درصدها، واکنش‌های قیمت، painها، candidateها یا پیشنهادها دادهٔ مشتری، traction، proof of demand، پیش‌بینی درآمد یا مبنای جذب سرمایه نیستند.

## خروجی pipeline در این مثال

| شاخص | نتیجهٔ مصنوعی | برداشت مجاز |
|---|---:|---|
| رکوردهای نمونه | 10 | فقط نشان می‌دهد pipeline برای cohort ده‌تایی چگونه کار می‌کند. |
| pain score برابر 4 یا 5 | 6 از 10 | توزیع سناریوسازی‌شده برای نمایش segmentation است؛ prevalence واقعی نیست. |
| واکنش `accept` | 3 از 10 | نمونه‌ای از کدگذاری پاسخ است؛ conversion rate نیست. |
| واکنش `conditional_accept` | 2 از 10 | نشان می‌دهد شرط‌ها باید جدا از acceptance ثبت شوند. |
| objection با کد budget | 3 از 10 | نمونه‌ای از taxonomy مانع خرید است؛ sensitivity واقعی قیمت نیست. |
| priority design partner | 6 از 10 | output synthetic scorecard پیش از اعمال سقف ظرفیت cohort است. |
| cohort انتخابی | 5 از 10 | ظرفیت مصنوعی پنج‌نفره برای تمرین قواعد selection است. |

## تفسیر آموزشی واکنش به قیمت

در این مثال، سه record با `accept` و دو record با `conditional_accept` کدگذاری شده‌اند. تحلیلگر نباید این دو گروه را در یک نرخ واحد ادغام کند. `conditional_accept` به‌تنهایی نمی‌گوید customer پرداخت خواهد کرد؛ ممکن است شرط scope، privacy، security، budget approval یا timing داشته باشد. در دادهٔ واقعی، هر شرط باید به source note و owner follow-up متصل شود.

دو record نیز `not_discussed` دارند. آن‌ها نباید در numerator یا denominator conversion قرار گیرند، مگر اینکه تعریف metric از پیش مشخص کند که «rate among all interviews» مدنظر است. این مثال نشان می‌دهد که metric definition قبل از جمع‌بندی حیاتی است.

## تفسیر آموزشی objectionها

| objection synthetic | شمار | follow-up آموزشی مناسب |
|---|---:|---|
| budget | 3 | owner بودجه، cycle خرید و baseline cost workflow ثبت شود. |
| trust_accuracy | 1 | scope screening-only، validation boundary و evidence package مرور شود. |
| security_privacy | 1 | data-minimization، retention و deployment boundary مشخص شود. |
| scope_mismatch | 1 | package را کوچک‌تر یا job-to-be-done را بازتعریف کنید؛ feature promise ندهید. |
| timing / no current project | 2 | nurture با trigger-date؛ به زور وارد cohort نشود. |

این جدول صرفاً فرآیند پاسخ‌دهی را نمایش می‌دهد. هیچ‌کدام از موضوع‌ها به‌عنوان «top objection بازار» یا نیاز واقعی محصول قابل‌اعلام نیستند.

## تمرین Qualification Scorecard

در سناریوی ساختگی، شش candidate امتیاز ۱۰ یا بیشتر می‌گیرند؛ اما cohort تنها پنج ظرفیت دارد. قواعد تساوی باعث می‌شوند پنج candidate با مجموع بالاتر و readiness مناسب‌تر انتخاب شوند. candidate ششم به‌عنوان reserve یا waiting list باقی می‌ماند.

| اولویت synthetic | candidate | score / 12 | وضعیت | offer آموزشی |
|---:|---|---:|---|---|
| 1 | PILOT-01 | 12 | Priority design partner | Standard Evidence Pilot |
| 2 | PILOT-10 | 12 | Priority design partner | Extended Workflow Pilot |
| 3 | PILOT-02 | 11 | Priority design partner | Extended Workflow Pilot |
| 4 | PILOT-03 | 11 | Priority design partner | Standard Evidence Pilot |
| 5 | PILOT-06 | 11 | Priority design partner | Standard Evidence Pilot |
| Reserve | PILOT-07 | 10 | Priority design partner | Founding Design Partner |

## مسیر واقعی پس از جایگزینی داده

پس از دریافت notes واقعی، این workflow دوباره اجرا می‌شود اما synthetic records، نمودارها و selection table کنار گذاشته می‌شوند. گزارش واقعی باید برای هر insight تعداد پاسخ‌های پشتیبان، segment، data completeness و quotation ناشناس داشته باشد. اگر داده کامل نیست، خروجی باید `insufficient evidence` باشد، نه یک داستان منسجم مصنوعی.
