# ممیزی شواهد Problem-Discovery — NACA Airfoil Kit Pro

**تاریخ مرجع:** ۱۴ اوت ۲۰۲۶
**دامنهٔ ممیزی:** مخزن GitHub، اسناد راهبردی و دارایی‌های محلی پروژه تا commit `e65f8ee`.
**هدف:** تعیین اینکه آیا واقعاً ۱۰ مصاحبهٔ problem-discovery اجرا و ثبت شده‌اند یا خیر؛ سپس تعیین اینکه کدام نتایج برای تصمیم محصول/قیمت‌گذاری قابل‌استفاده‌اند.

## نتیجهٔ اصلی

> **هیچ رکورد قابل‌ممیزی از اجرای ۱۰ مصاحبه، پاسخ شرکت‌کننده، transcript، یادداشت جلسه، CRM export، survey response یا outcome پرداختی در مخزن موجود نیست.**

بنابراین در این مرحله هیچ «بازخورد مشتری» یا «نرخ تبدیل مصاحبه» نباید به‌عنوان fact در deck سرمایه‌گذار، pricing model یا roadmap مطرح شود. اسناد موجود، انجام حداقل ۱۰ مصاحبه و ۳ تا ۵ پایلوت را به‌عنوان **برنامهٔ اعتبارسنجی آینده** تعریف می‌کنند، نه کار تکمیل‌شده. [1] [2]

## مواردی که واقعاً در دسترس است

| دستهٔ شواهد | وضعیت | آنچه می‌توان با اطمینان گفت | آنچه نمی‌توان گفت |
|---|---|---|---|
| قابلیت محصول | موجود | نسخهٔ web/desktop، robust multi-Re، validation workflow، audit manifest و مسیر worker امن پیاده‌سازی شده‌اند. | اینکه مشتری حاضر است برای آن‌ها پول بپردازد یا مرتب استفاده کند. |
| benchmark فنی | موجود | regressionهای محلی و CI، و artifactهای تحلیل/validation در مخزن وجود دارند. | اینکه accuracy برای یک mission مشتری یا approval خارجی کافی است. |
| market / competitor research | موجود | جایگزین‌ها و rangeهای قیمت رسمی آن‌ها برای context گردآوری شده است. [2] | اندازهٔ TAM/SAM/SOM نهایی یا توان pricing محصول حاضر. |
| مصاحبهٔ problem-discovery | موجود نیست | فقط design پیشنهادی برای اجرای آن داریم. [1] | pain ranking، budget، buyer، objection، frequency یا WTP واقعی. |
| پایلوت محدود | موجود نیست | package و success gate قابل‌طراحی است. | conversion، expansion، retention یا referenceability. |

## تفکیک «فرضیه» از «یافته»

| موضوع | وضعیت فعلی | برچسب مورد نیاز در اسناد و اسلایدها |
|---|---|---|
| Beachhead: تیم‌های کوچک UAS/rotor و مشاوران | فرضیه با اطمینان متوسط | `Hypothesis — pending discovery` |
| درد: پراکندگی geometry، solver، spreadsheet و report | فرضیه قابل‌آزمون | `Problem to validate` |
| ارزش: evidence-ready study package | قابلیت محصول + ارزش پیشنهادی | `Product capability; buyer value unvalidated` |
| قیمت Individual/Team/Pilot | range آزمایشی | `Experimental offer; not realized pricing` |
| willingness-to-pay | نامشخص | `No customer evidence yet` |
| attraction/retention/conversion | نامشخص | `No cohort evidence yet` |

## استاندارد حداقلی برای ثبت ۱۰ مصاحبه

هر مصاحبه باید با consent مناسب و بدون ثبت دادهٔ حساس غیرضروری، حداقل موارد زیر را در یک template یکسان نگه دارد.

| فیلد | هدف تصمیم‌گیری |
|---|---|
| شناسهٔ ناشناس، segment، region، اندازه تیم و نقش | تعیین ICP بدون افشای هویت |
| آخرین تصمیم واقعی airfoil/rotor | جلوگیری از پاسخ فرضی و generic |
| workflow فعلی، ابزارها و زمان/اصطکاک | تعیین job-to-be-done و switching cost |
| consequence تصمیم ضعیف یا تأخیر | سنجش شدت pain، نه فقط علاقه |
| منبع داده/validation موجود | تعیین product readiness و evidence gap |
| بودجه/صاحب بودجه/procurement | فرق user، champion و economic buyer |
| واکنش به study package و objectionها | آزمون positioning |
| price reaction با ladder ثابت | ثبت WTP قابل‌مقایسه، نه سؤال «چه مبلغی می‌پردازید؟» |
| follow-up/pilot eligibility | ساخت pipeline با consent |
| نقل‌قول paraphraseشده و confidence interviewer | جلوگیری از overgeneralization |

## معیار پایان discovery

پس از ۱۰ مصاحبه، فقط زمانی می‌توان نتیجه‌گیری اولیه کرد که حداقل هفت رکورد کامل باشند و هر نتیجه با frequency، شدت pain و evidence واقعی پشتیبانی شود. تصمیم ادامهٔ پایلوت باید بر مبنای تعداد داوطلبان واجد شرایط، پذیرش scope، willingness to provide real study data، و واکنش به offer باشد؛ نه تعداد likes یا تعریف شفاهی.

### Gate پیشنهادی

| outcome | تفسیر | اقدام |
|---|---|---|
| حداقل ۶ نفر از ۱۰ نفر یک workflow تکرارشونده با study handoff توصیف کنند | signal اولیهٔ problem frequency | ادامه به pilot design |
| حداقل ۴ نفر از ۱۰ نفر data/geometry واقعی برای review ارائه کنند | signal اولیهٔ urgency و trust | انتخاب design partner |
| حداقل ۳ نفر scope پایلوت و price ladder را بررسی کنند | signal اولیهٔ economic conversation | ارائهٔ pilot offer |
| کمتر از ۳ نفر pain را high-priority بدانند | positioning یا ICP نامناسب است | توقف build و بازتعریف discovery |

## ورودی مورد نیاز برای تبدیل این ممیزی به «نتایج واقعی»

کاربر یا تیم باید یکی از این موارد را ارائه کند: فایل CSV/Sheet، noteهای مصاحبه، transcriptهای خلاصه‌شده، CRM export یا پاسخ survey. پس از دریافت، داده‌ها با شناسهٔ ناشناس نرمال‌سازی می‌شوند، frequency/segment/pain/WTP تحلیل می‌شود و deck با **نتایج واقعی** به‌روزرسانی خواهد شد. تا پیش از آن، deck تنها می‌تواند یک اسلاید «Discovery status: planned / evidence pending» داشته باشد.

## منابع

[1]: ./GLOBAL_BUSINESS_PRODUCT_STRATEGY_FA.md "طرح تجاری و محصول جهانی — NACA Airfoil Kit Pro"
[2]: ./research/MARKET_COMPETITOR_RESEARCH_NOTES_FA.md "یادداشت‌های پژوهش بازار، رقبا و رگولاتوری"
