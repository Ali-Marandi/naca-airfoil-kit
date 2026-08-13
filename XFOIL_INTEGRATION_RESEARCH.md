# یافته‌های طراحی یکپارچه‌سازی XFOIL

## قابلیت‌های مستندشده

XFOIL 6.9 یک ابزار تعاملی تحلیل و طراحی airfoil زیرصوت است که تحلیل viscous/inviscid، transition آزاد یا forced، محاسبه polar، خروجی Cp و برخی قابلیت‌های تغییر هندسه را ارائه می‌کند. حل viscous از مدل لایه مرزی integral coupled با جریان potential استفاده می‌کند و رفتار نزدیک/پس از stall محدودیت دارد. [1]

| موضوع | نتیجه طراحی برای NACA Airfoil Kit Pro |
|---|---|
| Polar batch | از `OPER`, `PACC` و `ASEQ` استفاده شود؛ فایل polar و dump جداگانه برای هر run نگهداری شود. [2] |
| شرط جریان | Re، Mach، Ncrit، forced transition top/bottom، iteration limit و alpha sweep باید explicit input و بخشی از manifest باشند. [3] |
| هندسه | مختصات نرمال‌شده و labelled coordinate file در temp working directory نوشته شود؛ checksum geometry و تعداد نقطه ثبت گردد. [1] |
| خروجی | Polar parser باید alpha, Cl, Cd, Cdp, Cm, Top_Xtr, Bot_Xtr را در model-neutral schema تبدیل کند. |
| شکست همگرایی | نقطه‌های ناقص باید status جداگانه داشته باشند؛ به‌هیچ‌وجه با interpolation پنهان یا صفر پر نشوند. |
| Cp و BL | خروجی `CPWR` و `DUMP` را فقط on-demand برای بررسی detailed case و validation overlay تولید کنید. [3] |
| مقایسه | نتایج XFOIL به‌عنوان `solver="xfoil"` و نسخه executable ثبت شوند و هرگز به‌جای data measurement برچسب experimental نخورند. |

## محدودیت‌های مهم

XFOIL برای جریان shockدار یا جریان transonic با دقت قابل اتکا طراحی نشده و در جدایش گسترده/نزدیک یا بالاتر از stall محدودیت دارد. همچنین پارامتر Ncrit صرفاً باید متناسب با محیط turbulence/transition ثبت شود؛ برای تونل باد تمیز مقدارهای حدود 10–12 و برای تونل متوسط حدود 9 در مستندات نمونه آمده‌اند، اما نباید بدون metadata آزمایش به‌عنوان calibration عمومی به‌کار روند. [1] [3]

## منابع

[1]: https://web.mit.edu/aeroutil_v1.0/xfoil_doc.txt "XFOIL 6.9 User Primer"
[2]: https://v0xnihili.github.io/xfoil-docs/plotting/ "XFOIL Polar Calculations and Plotting"
[3]: https://v0xnihili.github.io/xfoil-docs/analysis/ "XFOIL Analysis, Transition and Force Calculation"
[4]: https://docs.qblade.org/src/user/airfoil/airfoil_analysis.html "QBlade Airfoil Analysis Overview"
