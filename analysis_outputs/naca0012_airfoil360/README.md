# NACA 0012 — Airfoil 360 comparison output

این پوشه خروجی تکرارپذیر اسکریپت [`scripts/compare_naca0012_airfoil360.py`](../../scripts/compare_naca0012_airfoil360.py) است. نمودار و فایل‌های metrics/residuals، NACA 0012 مدل preliminary پروژه را در نقاط زاویه یکسان با دادهٔ آزمایشگاهی **Airfoil 360 v2022** مقایسه می‌کنند.

| فایل | محتوا |
|---|---|
| `naca0012_airfoil360_comparison.png` | نمودار Cl و Cd آزمایش در برابر مدل فعلی در Re = 50,000 و 100,000 |
| `naca0012_airfoil360_metrics.json` | MAE، RMSE، bias و metadata مقایسه |
| `naca0012_airfoil360_residuals.csv` | residual نقطه‌به‌نقطه برای بازبینی مستقل |

دادهٔ آزمایش از Stringer, D. Blake (2022)، *Airfoil 360 v2022: Wind Tunnel Data*، Mendeley Data، DOI [10.17632/dz4bv26ncd.1](https://data.mendeley.com/datasets/dz4bv26ncd/1)، مجوز CC BY 4.0، دریافت شده است. خروجی تنها تفاوت مدل فعلی را در دامنه مشخص‌شده نشان می‌دهد و **نه** calibration مدل، نه اعتبارسنجی کامل و نه تایید برای استفاده ایمنی‌محور محسوب می‌شود.

برای تولید دوباره:

```bash
python scripts/compare_naca0012_airfoil360.py \
  --workbook Airfoil360_wind_tunnel_data_v2022.xlsx \
  --output-dir analysis_outputs/naca0012_airfoil360 \
  --alpha-min 0 --alpha-max 8.1
```
