# یافته‌های پژوهشی اعتبارسنجی تونل باد

## منابع مرجع انتخاب‌شده

| منبع | پروفایل و شرایط | کاربرد در اعتبارسنجی |
|---|---|---|
| NASA TM-100019 | NACA 0012؛ فراتحلیل بیش از 40 تونل باد، دامنه‌های وسیع Mach، Reynolds و alpha | مرجع benchmark و هشدار درباره تفاوت امکانات آزمایشگاهی [1] |
| NASA CR-197497 | NACA 2412؛ Re = 2.2×10⁶، M = 0.13، alphaهای 12.4°، 14.4° و 16.4° | ارزیابی ناحیه جدایش، Cp و نزدیکی stall [2] |
| NACA TR-647 | NACA 0012؛ Re حدود 1.7×10⁶ تا 7.0×10⁶ در آزمون‌های lift/drag | benchmark کلاسیک برای ناحیه Re بالا [3] |
| Airfoil 360 v2022 | NACA 0012 و 2412؛ Re = 50,000 و 100,000، زاویه حمله تا 360° | اعتبارسنجی low-Re و پس از stall؛ داده با مجوز CC BY 4.0 [4] |

## نکات روش‌شناسی

نتایج یک تونل باد نباید بدون metadata با نتایج یک حل‌گر مقایسه شود. برای هر polar باید geometry revision، chord، Reynolds، Mach، سطح roughness/transition، turbulence intensity، wall/blockage correction، alpha convention، دمای هوا و روش محاسبه ضرایب ثبت شود. گزارش NASA درباره NACA 0012 تأکید می‌کند که هیچ آزمایش منفردی مجموعه کامل داده‌های قابل اعتماد در همه شرایط نداشته است؛ بنابراین هر ردیف آزمایشی به‌عنوان یک dataset دارای دامنه اعتبار مشخص نگهداری می‌شود. [1]

برای اعتبارسنجی باید فقط نقاطی مقایسه شوند که شرایطشان با tolerance تعریف‌شده منطبق است. پیشنهاد عملی برای نسخه فعلی: تطبیق Re در ±5٪ و Mach در ±0.02، مگر آنکه کاربر tolerance دیگری تعریف کند. سپس برای Cl و Cd به‌ترتیب MAE، RMSE و bias محاسبه می‌شود. اختلاف زاویه‌ای صفر-برا (Δα0)، اختلاف بیشینه Cl و اختلاف L/D بیشینه نیز گزارش می‌گردد. ناحیه stall به‌صورت جداگانه برچسب‌گذاری می‌شود و با RMSE خطی پیش از stall مخلوط نمی‌شود.

## منابع

[1]: https://ntrs.nasa.gov/citations/19880002254 "A Critical Assessment of Wind Tunnel Results for the NACA 0012 Airfoil"
[2]: https://ntrs.nasa.gov/citations/19950002355 "Experimental Studies of Flow Separation of the NACA 2412 Airfoil at Low Speeds"
[3]: https://ntrs.nasa.gov/citations/19930091723 "Tests of NACA 0009, 0012, and 0018 Airfoils in the Full-Scale Tunnel"
[4]: https://data.mendeley.com/datasets/dz4bv26ncd "Airfoil 360 v2022: Wind Tunnel Data"
