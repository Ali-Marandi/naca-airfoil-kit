# راهنمای ارسال و تحلیل دادهٔ ۱۰ مصاحبهٔ Problem-Discovery

**هدف:** تبدیل یادداشت‌های مصاحبهٔ واقعی به تحلیل قابل‌ردیابی برای ICP، pain، workflow، willingness-to-pay، qualification و طرح پایلوت.

## روش ارسال

می‌توانید یکی از سه روش زیر را استفاده کنید. روش نخست برای تحلیل دقیق‌تر توصیه می‌شود.

| روش | فایل یا محتوا | مناسب برای |
|---|---|---|
| قالب CSV | `templates/problem_discovery_interviews_template.csv` را تکمیل و بارگذاری کنید | تحلیل مقایسه‌ای، جدول و نمودار |
| Excel/Google Sheets export | CSV یا XLSX با یک ردیف برای هر مصاحبه | دادهٔ CRM یا research repository موجود |
| یادداشت متنی | برای هر مصاحبه، بخش‌های مشخص‌شدهٔ زیر را ارسال کنید | یادداشت‌های آزاد یا transcript خلاصه‌شده |

## حریم خصوصی و کمینه‌سازی داده

فقط اطلاعات لازم برای تحلیل تجاری را ارسال کنید. نام شخص، ایمیل، شماره‌تلفن، نام مشتری، موقعیت دقیق، اطلاعات قراردادی، هندسهٔ محرمانه، export فنی حساس یا هر شناسهٔ شخصی را حذف یا با شناسهٔ ناشناس جایگزین کنید. به‌جای نام سازمان از segment و team-size band استفاده کنید؛ برای مثال `EU rotor consultancy / 2–10 people`.

> نمونهٔ خوب: «INT-03، مشاور آئرودینامیک، EMEA، تیم ۲–۱۰ نفر، تصمیم rotor در ۳۰ روز.»
> نمونهٔ نامناسب: نام فرد، ایمیل، نام مشتری نهایی یا پیوست محرمانهٔ هندسه.

## فیلدهای ضروری برای هر مصاحبه

| فیلد | چگونه ثبت شود | چرا مهم است |
|---|---|---|
| `interview_id` | `INT-01` تا `INT-10` | ردگیری بدون هویت شخصی |
| `segment` و `role` | UAS team / rotor consultancy / lab؛ engineer / founder / buyer | تفکیک ICP و نقش خریدار |
| `last_real_design_decision` | یک تصمیم واقعی و اخیر، نه نظر کلی | کاهش پاسخ‌های فرضی |
| `workflow_current` و `tools_current` | گام‌ها و ابزارهای فعلی | سنجش switching cost |
| `workflow_frequency` و `decision_timeline_days` | چندبار در ماه/فصل و deadline | سنجش شدت و فوریت |
| `pain_summary` و `pain_severity_1_5` | مشکل مشخص + نمره | اولویت‌بندی pain |
| `consequence_of_delay` | هزینه، rework، تأخیر review یا missed milestone | تفکیک pain واقعی از علاقه |
| `price_offer_shown_usd` و `price_reaction` | فقط offer واقعی نمایش‌داده‌شده + واکنش | WTP مبتنی بر رفتار |
| `economic_buyer_identified` و `budget_owner_or_path` | yes/no و مسیر خرید | تشخیص امکان پایلوت پولی |
| `primary_objection` | value / price / timing / trust / security / procurement / other | تحلیل مانع تبدیل |
| `pilot_eligibility_1_5` و `follow_up_status` | نمره و next step | ساخت pipeline عملیاتی |

## واژه‌نامهٔ کدگذاری پاسخ‌ها

| فیلد | مقادیر قابل‌قبول |
|---|---|
| `geometry_data_ready` | `yes` / `partial` / `no` |
| `economic_buyer_identified` | `yes` / `no` / `unknown` |
| `price_reaction` | `accept` / `conditional_accept` / `consider` / `too_high` / `too_low` / `no_budget` / `not_discussed` |
| `primary_objection` | `value_unclear` / `budget` / `timing` / `scope_mismatch` / `trust_accuracy` / `security_privacy` / `procurement` / `competitor_tool` / `no_current_project` / `other` |
| `study_package_reaction` | `strong` / `moderate` / `weak` / `not_discussed` |
| `follow_up_status` | `pilot_candidate` / `follow_up` / `nurture` / `disqualified` |
| `consent_for_anonymized_use` | `yes` / `no` / `pending` |

## مقیاس‌دهی

`pain_severity_1_5`: ۱ یعنی صرفاً کنجکاوی و ۵ یعنی درد فوری با consequence روشن. `pilot_eligibility_1_5`: ۱ یعنی عدم تناسب و ۵ یعنی decision واقعی، data آماده، champion و زمان follow-up مشخص. `interviewer_confidence_1_5`: اطمینان interviewer به کامل و دقیق بودن یادداشت، نه کیفیت prospect.

## قالب یادداشت متنی جایگزین

```text
Interview ID: INT-01
Segment / role / region / team band:
Last real decision and deadline:
Current workflow and tools:
Frequency and pain (1–5):
Consequence of delay / rework:
Data and validation context:
Economic buyer and purchase path:
Offer shown and price reaction:
Objection(s):
Pilot eligibility (1–5) and next step:
Anonymized quote and consent status:
```

## آنچه پس از دریافت داده انجام می‌شود

تحلیل فقط با دادهٔ تحویلی انجام می‌شود و شامل completeness check، کدگذاری objectionها، distribution pain/frequency، segment comparison، pricing reaction، qualification ranking و synthesis quotations خواهد بود. هر نتیجه با تعداد پاسخ‌های پشتیبان، کیفیت یادداشت و limitation نمونه گزارش می‌شود؛ عدم پاسخ هرگز به‌معنای پاسخ منفی یا مثبت تلقی نخواهد شد.
