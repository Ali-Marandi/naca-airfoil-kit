# طرح اجرایی ادغام XFOIL در NACA Airfoil Kit Pro

**وضعیت سند:** طراحی پیشنهادی برای نسخهٔ بعدی؛ هنوز پیاده‌سازی نشده است.

> هدف، تبدیل XFOIL به یک backend اختیاری، قابل‌ردیابی و ایمن است؛ نه جایگزین‌کردن کورکورانهٔ مدل سریع کنونی و نه ارائهٔ خروجی XFOIL به‌عنوان دادهٔ آزمایشگاهی.

## 1. چرایی و محدوده

مدل فعلی برای غربال‌گری سریع مناسب است، اما drag، transition و جدایش را با یک حل viscous coupled حل نمی‌کند. XFOIL قابلیت تحلیل viscous/inviscid، transition آزاد یا اجباری، polar sweep و خروجی Cp/BL را ارائه می‌کند. با این حال، خود XFOIL در جدایش گسترده و نزدیک/بالاتر از stall محدودیت دارد؛ بنابراین integration باید **quality flags**، علائم عدم‌همگرایی و دامنه اعتبار را به کاربر نشان دهد. [1] [2]

| لایه | مسئولیت | نتیجه مورد انتظار |
|---|---|---|
| `airfoil_pro.py` | geometry و model سریع فعلی | screening فوری و fallback شفاف |
| `xfoil_adapter.py` | ساخت input، اجرای sandboxed و parser | یک `SolverRunResult` بدون وابستگی UI |
| `study_store.py` | manifest، فایل‌های خام و checksum | بازتولیدپذیری و audit trail |
| `app.py` / `gui.py` | انتخاب solver، progress و visual comparison | workflow یکسان برای web و desktop |
| worker/container اختیاری | اجرای executable در محیط کنترل‌شده | قابلیت production بدون shell در UI |

## 2. مدل دادهٔ پیشنهادی

هر درخواست باید immutable و serializable باشد. نمونهٔ schema پیشنهادی:

```python
SolverRunSpec(
    solver="xfoil",
    airfoil_name="NACA 0012",
    coordinates_xy=[...],
    reynolds=100_000,
    mach=0.0,
    ncrit=9.0,
    xtr_top=1.0,
    xtr_bottom=1.0,
    alpha_start=-4.0,
    alpha_end=12.0,
    alpha_step=0.5,
    iteration_limit=100,
    viscous=True,
)
```

`SolverRunResult` باید علاوه بر rows استاندارد `alpha_deg, cl, cd, cm, cdp, top_xtr, bottom_xtr`، فیلدهای `point_status`, `converged`, `solver_version`, `duration_ms`, `geometry_sha256`, `stdout_tail`, `input_manifest` و مسیر artifactهای raw را نگه دارد. یک نقطهٔ ناموفق باید به صورت `status="not_converged"` ذخیره شود و هرگز با صفر یا interpolation پنهان جایگزین نشود.

## 3. پروتکل اجرای XFOIL

### آماده‌سازی هندسه

مختصات به یک فایل labelled `.dat` در پوشهٔ موقت اختصاصی run نوشته می‌شوند. قبل از اجرا، runner باید این کنترل‌ها را انجام دهد: حداقل تعداد نقطه، حذف duplicate point، contour بسته/قابل‌قبول، chord normalization، محدودیت طول ورودی و SHA-256 مختصات. XFOIL با `LOAD` هندسه را می‌خواند و می‌تواند با `PANE` بازپنل‌بندی کند؛ در نتیجه تعداد نقاط input و تنظیم paneling نیز بخشی از manifest است. [1]

### ساخت script کنترل‌شده

UI هرگز command آزاد از کاربر دریافت نمی‌کند. adapter تنها از پارامترهای allowlisted برای تولید یک script batch استفاده می‌کند: `LOAD/PANE`، `OPER`، حالت viscous، Reynolds، Mach، `VPAR` شامل Ncrit و transition اجباری، limit iteration، `PACC` و `ASEQ`. XFOIL برای polar accumulation از `PACC` و برای sweep alpha از `ASEQ` پشتیبانی می‌کند. [3]

```text
LOAD geometry.dat
PANE
OPER
VISC <Re>
MACH <Mach>
VPAR
N <Ncrit>
XTR <top> <bottom>
<return to OPER>
ITER <limit>
PACC
polar.txt
dump.txt
ASEQ <alpha_start> <alpha_end> <alpha_step>
PACC
QUIT
```

> متن بالا **الگوی protocol** است. adapter باید syntax دقیق executable مورد استفاده را با golden test تأیید کند؛ گزینه‌ها و promptها بین buildهای مختلف XFOIL ممکن است تفاوت داشته باشند.

### اجرای امن

`subprocess.run` باید با `shell=False`، آرگومان ثابت executable، `cwd` برابر پوشهٔ موقت run، `stdin` از script تولیدشده، `timeout` سخت، اندازه input محدود و خروجی capture شده اجرا شود. مسیر executable فقط از configuration administrator خوانده می‌شود؛ path یا command از کاربر پذیرفته نمی‌شود. در backend production، worker باید با non-root user، filesystem موقت و read-only root filesystem اجرا شود.

| کنترل | سیاست نسخه بعد |
|---|---|
| time-out | پیش‌فرض 30 s برای polar معمولی؛ قابل تنظیم فقط توسط administrator |
| concurrency | صف worker با سقف job؛ جلوگیری از اشباع Streamlit process |
| memory/CPU | محدودیت container یا process supervisor |
| geometry files | پوشهٔ موقت per-run و حذف پس از archive یا TTL |
| log | tail محدودشده؛ حذف pathهای داخلی و اطلاعات حساس |
| cancellation | termination کنترل‌شدهٔ process و ثبت `cancelled` در manifest |

## 4. پارامترهای viscous و قرارداد UX

کاربر باید بداند solver چه مسئله‌ای را حل کرده است. فیلدهای Reynolds، Mach، Ncrit، transition top/bottom، alpha sweep و iteration limit همگی در فرم قابل مشاهده‌اند. Ncrit پارامتر مدل transition `e^n` است و به محیط disturbance وابسته است؛ مستندات نمونه مقدار حدود 10–12 را برای clean wind tunnel و حدود 9 را برای average wind tunnel ذکر می‌کنند. این مقادیر نقطه شروع هستند و نباید بدون evidence از محیط آزمایش به عنوان calibration عمومی به کار روند. [2]

| تنظیم | نمایش در UI | رفتار پیش‌فرض پیشنهادی |
|---|---|---|
| Reynolds | اجباری | مقدار مطالعهٔ فعال |
| Mach | اجباری، پیش‌فرض 0 | warn برای دامنه نامناسب/نزدیک transonic |
| Ncrit | advanced | 9.0 با tooltip و provenance |
| XTR top/bottom | advanced | 1.0 / 1.0 برای transition آزاد؛ UI trip را واضح برچسب می‌زند |
| Iteration limit | advanced | 100؛ point failure به‌صورت صریح |
| alpha grid | عادی | start/end/step با هزینهٔ تخمینی |

## 5. Parser و canonical polar schema

adapter فایل raw polar را بدون تغییر archive می‌کند و سپس به schema داخلی تبدیل می‌کند. parser باید header XFOIL را robust پیدا کند، ستون‌ها را با نام map کند و rows ناقص را حفظ کند. خروجی canonical باید `model_name`, `model_version`, `run_id`, `airfoil_sha256`, `reynolds`, `mach`, `ncrit`, `transition`, `alpha_deg`, `cl`, `cd`, `cm`, `top_xtr`, `bottom_xtr`, `converged` و `warning_codes` داشته باشد. QBlade نیز polarها را با پارامترهایی مانند Re، Mach، N-Crit و transition top/bottom مدیریت می‌کند؛ این الگو برای schema محصول مناسب است. [4]

## 6. مقایسه، validation و گزارش

در صفحه Polar، کاربر باید بتواند مدل سریع و XFOIL را با رنگ و legend متفاوت ببیند. در صفحه Validation، هر دو solver می‌توانند در برابر CSV experiment در alphaهای measurement سنجیده شوند. جدول خروجی باید metrics را به تفکیک solver، ناحیه alpha و Cl/Cd نشان دهد. Cp و boundary-layer dump فقط برای یک operating point انتخابی و همراه Re/Mach/Ncrit نشان داده می‌شوند.

| برچسب نتیجه | معنی |
|---|---|
| `screening` | مدل سریع فعلی؛ مناسب برای triage اولیه |
| `numerical_viscous` | خروجی XFOIL؛ هنوز experiment نیست |
| `validated_range` | فقط وقتی dataset، conditions و metric threshold ثبت شده‌اند |
| `out_of_range` | نقطه پس از stall، عدم‌همگرایی یا شرایط خارج از validation domain |

## 7. مسیر استقرار

نسخه desktop می‌تواند executable XFOIL تأییدشده را همراه installer یا در مسیر admin-configured اجرا کند. نسخه Docker می‌تواند XFOIL را در image build کند و runner را در یک worker process جدا نگه دارد. در Streamlit Community Cloud باید availability executable، timeout و policy platform پیش از فعال‌سازی بررسی شود؛ طراحی پیشنهادی این است که web UI روی Community Cloud فقط job را به یک worker/API کنترل‌شده ارسال کند یا در نبود backend، XFOIL را با پیام صریح «solver backend unavailable» غیرفعال کند. اجرای solver خارجی در process اصلی Streamlit برای workload چندکاربره توصیه نمی‌شود.

## 8. برنامه اجرا در چهار milestone

| milestone | خروجی قابل پذیرش | معیار تکمیل |
|---|---|---|
| M1 — adapter محلی | writer، executor امن، parser و golden NACA 0012 case | run تکرارپذیر با raw artifacts و test parser |
| M2 — desktop integration | انتخاب solver، progress، polar overlay و CSV/manifest | هیچ freeze در UI و نمایش failure pointها |
| M3 — Docker worker | queue، timeout، concurrency limit و health endpoint | load test محدود و log/audit کامل |
| M4 — validation release | dataset manifest، report template و solver comparison | baseline NACA 0012/2412 با conditions ثبت‌شده |

## 9. آزمون و پذیرش

آزمون واحد باید coordinate writer، script generator، parser و taxonomy خطا را پوشش دهد. آزمون integration باید executable pinned را با NACA 0012 و یک alpha sweep کوتاه اجرا کند. آزمون regression باید فایل polar known-good را به parser بدهد. آزمون UI باید نشان دهد solver failure منجر به crash یا نتیجه صفر نمی‌شود. release pipeline باید license، checksum/binary provenance و version executable را در release manifest ثبت کند.

## منابع

[1]: https://web.mit.edu/aeroutil_v1.0/xfoil_doc.txt "Drela & Youngren, XFOIL 6.9 User Primer"
[2]: https://v0xnihili.github.io/xfoil-docs/analysis/ "XFOIL Analysis and Transition"
[3]: https://v0xnihili.github.io/xfoil-docs/plotting/ "XFOIL Polar Calculations and Plotting"
[4]: https://docs.qblade.org/src/user/airfoil/airfoil_analysis.html "QBlade Airfoil Analysis Overview"
