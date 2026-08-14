# گزارش آزمون یکپارچه Pareto Explorer

**تاریخ اجرا:** 14 اوت 2026  
**دامنه:** Pareto Explorer، مسیر NACA generated و مسیر هندسه‌های نام‌دار UIUC.  
**مرز اعتبار:** نتایج aerodynamic این گزارش خروجی مدل panel/empirical هستند و برای اعتبارسنجی فیزیکی یا انتخاب نهایی طراحی کافی نیستند.

## suite یکپارچه افزوده‌شده

فایل `test_pareto_integration_catalog.py` دو مسیر مستقل را کنترل می‌کند. مسیر نخست، ماتریس deterministic شامل **120** هندسه NACA 4-digit را از ترکیب چهار camber، پنج موقعیت camber و شش thickness تولید می‌کند. مسیر دوم، API عمومی `ParetoExplorer.screen_geometries()` را با شش هندسه نام‌دار کنترل می‌کند تا catalogهای خارجیِ دریافت‌شده از منابع معتبر نیز از همان pipeline استفاده کنند.

| کنترل | انتظار | نتیجه |
|---|---|---|
| پوشش catalog بزرگ | 120 candidate و 120 polar | موفق |
| completeness ranking | نام یکتا، `pareto_rank >= 1` و حداقل یک front | موفق |
| dominance property | هیچ عضو Pareto front توسط candidate دیگر dominate نشود | موفق |
| integrity polar | شمار نتیجه alpha برای هر candidate برابر sweep باشد | موفق |
| named external geometries | screen_geometries با هدف `Cl @ design alpha` کار کند | موفق |

اجرای `python -m unittest -v test_pareto_integration_catalog.py` با موفقیت هر دو test را گذراند.

## اجرای کاتالوگ واقعی UIUC

runner جدید `scripts/run_pareto_uiuc_catalog.py` یک مجموعه محدود اما واقعی از **24** پروفایل NACA را از ایندکس UIUC بارگذاری می‌کند. این انتخاب bounded است تا CI و منبع عمومی زیر فشار bulk download قرار نگیرند؛ URL هر پروفایل در manifest ثبت می‌شود. داده‌های مختصات UIUC از دانشگاه Illinois گرفته شده‌اند. [1]

| پارامتر | مقدار اجرا |
|---|---:|
| پروفایل‌های درخواست‌شده | 24 |
| پروفایل‌های بارگذاری‌شده | 24 |
| profile ناموفق/مفقود | 0 |
| Reynolds | 1,000,000 |
| roughness k/c | 0 |
| alpha envelope | −4° تا 12°، گام 1° |
| objectives | بیشینه L/D و بیشینه Cl در envelope |
| Pareto front در همین run | UIUC NACA6412 |

این runner سه artifact قابل بازتولید می‌سازد: `pareto_uiuc_rankings.csv`، `pareto_uiuc_catalog.png` و `pareto_uiuc_manifest.json`. manifest شامل زمان اجرا، conditions، URLهای منبع، countهای load/failure و اعضای front است.

> **تفسیر:** تنها عضویت `UIUC NACA6412` در Pareto front مربوط به همین مدل، همین profile files، همین Reynolds و همین objectiveهاست. این نتیجه یک ادعای برتری عمومی یا اعتبارسنجی experiment نیست.

## اجرای مجدد

```bash
python scripts/run_pareto_uiuc_catalog.py \
  --reynolds 1000000 \
  --alpha-start -4 --alpha-end 12 --alpha-step 1 \
  --output-dir analysis_outputs/pareto_uiuc_catalog
```

برای تبدیل objective به Cl در alpha طراحی، `--design-alpha 4` را اضافه کنید. alpha طراحی باید در envelope انتخاب‌شده قرار گیرد.

## منابع

[1]: https://m-selig.ae.illinois.edu/ads/coord_database.html "UIUC Airfoil Coordinates Database"
