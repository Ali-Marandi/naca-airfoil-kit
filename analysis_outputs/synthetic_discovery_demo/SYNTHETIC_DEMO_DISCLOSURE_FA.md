# افشای اجباری — نمایش آموزشی تحلیل Discovery با دادهٔ فرضی

**وضعیت:** Synthetic / Illustrative / Non-customer evidence
**مالک داده:** هیچ مشتری یا مصاحبه‌شوندهٔ واقعی در این مجموعه وجود ندارد.
**هدف مجاز:** نمایش pipeline تحلیل، qualification scorecard، طراحی نمودار و ساختار deck.
**هدف غیرمجاز:** اثبات traction، willingness-to-pay، conversion، revenue، retention، TAM، product-market fit یا استفاده در جذب سرمایه بدون برچسب synthetic.

## فرضیات مصنوعی

این demo شامل دقیقاً ۱۰ رکورد ساختگی است تا شکل داده و جریان تحلیل را نشان دهد. رکوردها به‌طور عمدی بین تیم‌های UAS/rotor، مشاوران آئرودینامیک و آزمایشگاه‌ها پخش شده‌اند. واکنش‌های قیمت، شدت pain، آمادگی داده، ownership و objectionها سناریوهای آموزشی‌اند و از مصاحبه یا survey واقعی استخراج نشده‌اند.

## قواعد برچسب‌گذاری

تمام artifactهای زیر باید در title، caption یا footer دارای عبارت `SYNTHETIC DEMO — NOT CUSTOMER EVIDENCE` باشند:

| artifact | برچسب الزامی |
|---|---|
| CSV داده | نام فایل و ستون `data_status` |
| گزارش تحلیل | عنوان، executive summary و نتیجه‌گیری |
| نمودار | title یا caption |
| qualification ranking | header جدول |
| اسلایدها | cover و footer هر اسلاید محتوایی |
| پیام تحویل | هشدار روشن دربارهٔ عدم قابلیت استناد |

## جایگزینی با دادهٔ واقعی

هنگام دریافت دادهٔ واقعی، این مجموعه نباید با دادهٔ واقعی ادغام شود. analysis جدید در directory جداگانه تولید می‌شود، reference date و source file ثبت می‌گردد، و همهٔ metricها از نو محاسبه می‌شوند. هیچ نتیجه‌ای از synthetic cohort به analysis واقعی منتقل نمی‌شود.
