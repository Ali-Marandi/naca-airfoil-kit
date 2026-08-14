# مقایسه Reynolds: Pareto-front در برابر NACAهای مرجع

**تاریخ اجرا:** 14 اوت 2026  
**هدف:** مقایسه profile منتخب Pareto در کاتالوگ UIUC، یعنی **NACA 6412**، با NACA 0012، NACA 2412 و NACA 4412 در یک sweep Reynolds قابل‌بازتولید.  
**دامنه اعتبار:** این خروجی، یک **preliminary panel/empirical screening** است؛ نه polar viscous، نه CFD تأییدشده و نه داده تونل باد.

## روش و داده

مختصات چهار profile از UIUC Airfoil Coordinates Database دریافت شد. [1] profile NACA 6412 در اجرای پیشین Pareto روی 24 profile UIUC، با دو objective «حداکثر L/D در envelope» و «حداکثر Cl در envelope»، تنها عضو front بود. در این گزارش همان profile با سه NACA مرجع مقایسه شده است.

| پارامتر | مقدار |
|---|---|
| Profile Pareto-front | UIUC NACA6412 |
| Profileهای مرجع | UIUC NACA0012، NACA2412 و NACA4412 |
| Reynolds | 50k، 100k، 250k، 500k، 1.0M و 2.0M |
| roughness | `k/c = 0` |
| alpha envelope | −4° تا 12°، گام 1° |
| نقطه طراحی | α = 4° |
| خروجی | L/D بیشینه در envelope، Cl بیشینه، Cd و L/D در α = 4° |

> عبارت «بهترین L/D» در تمام profileها در α = 12° رخ داد؛ بنابراین **maximum داخل sweep** است و نباید به‌عنوان optimum فیزیکی یا پس از stall تعبیر شود.

## خروجی‌های عددی منتخب

| Profile | max L/D در Re=50k | max L/D در Re=2.0M | Cl,max | L/D در α=4°، Re=50k | L/D در α=4°، Re=2.0M |
|---|---:|---:|---:|---:|---:|
| Pareto-front NACA6412 | 27.89 | 59.46 | 0.587 | 23.97 | 51.10 |
| NACA0012 | 19.20 | 40.94 | 0.404 | 14.84 | 31.64 |
| NACA2412 | 5.95 | 12.68 | 0.125 | 5.21 | 11.10 |
| NACA4412 | 6.31 | 13.45 | 0.133 | 5.53 | 11.79 |

در همین model و conditions، NACA6412 نسبت به NACA0012 در تمام نقاط Reynolds حدود **45.25%** L/D بیشینهٔ بالاتر و حدود **61.50%** L/D بالاتر در α = 4° نشان داد. در مقایسه با NACA2412 و NACA4412، model اختلاف‌های بزرگ‌تری گزارش کرد؛ به‌ترتیب تقریباً 369% و 342% در L/D بیشینه. این اعداد تنها برای ranking داخل model هستند و به معنی improvement تأییدشده در دنیای واقعی نیستند.

## روند Reynolds و تفسیر

در هر چهار profile، Cd مدل در α = 4° از حدود 0.0211 در Re=50k به حدود 0.00988 در Re=2.0M کاهش یافت؛ به همین دلیل L/D با رشد Reynolds افزایش یافت. در مقابل، Cl,max مدل در کل sweep ثابت ماند، زیرا بخش lift این solver سبک عمدتاً inviscid است. همچنین Cd تقریباً برای همه profileها برابر گزارش شد؛ بنابراین بخش بزرگی از اختلاف L/D در این sweep از اختلاف Cl پیش‌بینی‌شده می‌آید، نه تفاوت drag profile-specific.

این دو رفتار، محدودیت کلیدی این مقایسه‌اند. برای نتیجه‌گیری performance واقعی باید این sweep با XFOIL/QFoil و transition/roughness مشخص اجرا شود، نقاط همگرایی بررسی شوند و برای profileهای نهایی با polar آزمایشگاهی مقایسه گردد. خصوصاً اختلاف بزرگ NACA6412 با NACA2412/4412 نباید بدون این مراحل به انتخاب طراحی تبدیل شود.

## بازتولید

```bash
python scripts/compare_pareto_reynolds.py \
  --output-dir analysis_outputs/pareto_reynolds_comparison
```

دستور سه artifact تولید می‌کند: `pareto_reynolds_metrics.csv`، `pareto_reynolds_comparison.png` و `pareto_reynolds_manifest.json`. برای خلاصه درصد اختلاف‌ها نیز اجرا کنید:

```bash
python scripts/summarize_pareto_reynolds.py \
  --metrics analysis_outputs/pareto_reynolds_comparison/pareto_reynolds_metrics.csv \
  --output analysis_outputs/pareto_reynolds_comparison/pareto_reynolds_summary.json
```

## منابع

[1]: https://m-selig.ae.illinois.edu/ads/coord_database.html "UIUC Airfoil Coordinates Database"
