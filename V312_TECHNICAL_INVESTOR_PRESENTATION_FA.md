# روایت و اسکریپت ارائهٔ v3.1.2 — مخاطب فنی و سرمایه‌گذار

**مدت پیشنهادی:** ۱۲ تا ۱۵ دقیقه، به‌علاوهٔ پرسش‌وپاسخ.  
**موضع محصول:** NACA Airfoil Kit Pro یک workflow تجاری برای **غربال‌گری مقدماتی و قابل‌ردیابی** ایرفویل است؛ نتیجه‌ها به‌صراحت جایگزین تحلیل viscous معتبر، CFD با fidelity بالا، تونل باد یا تصمیم safety-critical نیستند.

## Cover

**عنوان:** NACA Airfoil Kit Pro v3.1.2  
**زیرعنوان:** از هندسهٔ ایرفویل تا تصمیم غربال‌گری قابل‌ردیابی، مقاوم و آمادهٔ استقرار  
**ارائه‌کننده:** تیم محصول و مهندسی

**متن ارائه:** «v3.1.2 یک هدف روشن دارد: کوتاه‌کردن زمان تبدیل ایدهٔ هندسی به shortlist قابل‌پیگیری، بدون پنهان‌کردن محدودیت‌های مدل. امروز ابتدا زیرساخت فنی و evidence را مرور می‌کنیم و سپس نشان می‌دهیم چرا همین شفافیت، پایهٔ مسیر تجاری محصول است.»

## Slide 1

**عنوان:** v3.1.2، یک workflow است نه صرفاً generator

| نکتهٔ روی اسلاید | متن ارائه |
|---|---|
| ۴ و ۵ رقمی NACA، UIUC catalog و geometry QA | «هندسه از generator یا کاتالوگ UIUC وارد می‌شود؛ سپس QA و signature هندسی، ورودی قابل‌بازتولید برای تحلیل می‌سازند.» |
| Polar، robustness، flap، validation و audit | «جریان کار در یک Cl یا L/D متوقف نمی‌شود؛ envelope حساسیت، flap مقدماتی، مقایسه با داده و audit manifest در همان محصول حضور دارند.» |
| Preliminary by design | «در هر رابط و خروجی، محدودهٔ اعتبار شفاف است: مدل اصلی screening است و باید با solver viscous یا دادهٔ آزمایش تأیید شود.» |

**یادداشت منبع:** مختصات UIUC، بیش از ۱٬۶۰۰ ایرفویل و قراردادهای فایل را مستند می‌کند. [1]

## Slide 2

**عنوان:** تصمیم طراحی از یک زنجیرهٔ قابل‌ردیابی عبور می‌کند

| گام | متن ارائه |
|---|---|
| Geometry → Analysis | «کاربر هندسه، Reynolds، alpha و roughness را تعریف می‌کند؛ موتور مدل panel/empirical خروجی مقدماتی تولید می‌کند.» |
| Analysis → Evidence | «Validation Studio، residualهای Cl/Cd و MAE/RMSE/bias را جدا می‌کند تا خوب‌بودن lift به‌اشتباه به‌عنوان اعتبار drag برداشت نشود.» |
| Evidence → Decision | «Robustness، Pareto و audit manifest، shortlist، شرایط و hash geometry را برای بازبینی تیمی نگه می‌دارند.» |

**متن تکمیلی:** «این معماری، سرعت iteration را با قابلیت توضیح و بازتولید ترکیب می‌کند؛ همان حلقه‌ای که ابزارهای پراکندهٔ محاسباتی معمولاً از دست می‌دهند.»

## Slide 3

**عنوان:** Pareto جدید، رینولدز را وارد تعریف “robust” می‌کند

| دادهٔ اجرا | مقدار |
|---|---:|
| کاندیدهای واقعی UIUC NACA | 24 |
| شرایط Reynolds | 100k تا 2.0M در 5 نقطه |
| envelope α | −4° تا +12° با گام 1° |
| objectiveها در هر Re | بیشینهٔ L/D و Cl در α=4° |
| عضو front در این set | UIUC NACA6412 |
| میانگین / بدترین L/D NACA6412 | 46.08 / 32.74 |

**متن ارائه:** «روش جدید، یک میانگین ساده نیست. کاندید فقط زمانی روی front قرار می‌گیرد که هیچ رقیبی نتواند هم‌زمان در L/D و Cl، در *تمام* شرایط Reynolds، بر آن غالب شود. NACA6412 تنها عضو front این اجرای محدود شد. این نتیجه رتبه‌بندی مدل برای همین candidate set است؛ نه حکم برتری فیزیکی یا مجوز طراحی.»

**یادداشت منبع:** پروفیل‌ها از UIUC؛ output کامل در `pareto_multi_re_manifest.json` و `PARETO_MULTI_RE_ANALYSIS.md` ثبت شده است. [1]

## Slide 4

**عنوان:** اعتبار فیزیکی، در مرکز تصمیم است

| آنچه اکنون داریم | آنچه باید قبل از design release افزوده شود |
|---|---|
| overlay دادهٔ آزمایش، MAE/RMSE/bias، audit trail | polar viscous با transition/Ncrit مستند، validation هم‌شرط و uncertainty |
| محدودهٔ روشن برای flap و panel model | separation/post-stall، roughness و manufacturing tolerance در evidence package |

**متن ارائه:** «ارزش تجاری ابزار از ادعای دقت غیرواقعی نمی‌آید؛ از آشکارکردن فاصلهٔ model تا evidence می‌آید. خروجی بزرگ multi-Re باید به‌عنوان trigger validation دیده شود، زیرا مدل سبک وابستگی‌های viscous کامل را حل نمی‌کند.»

> «XFOIL برای تحلیل زیرصوت ایرفویل و polarهای Reynolds/Mach طراحی شده است؛ این یک مسیر ارتقای solver است، نه جایگزین validation آزمایشگاهی.» [2]

## Slide 5

**عنوان:** XFOIL در یک worker محدود و قابل‌کنترل جدا شده است

| لایه | نقش |
|---|---|
| Streamlit / Desktop UI | تعریف study، visualization، validation و download؛ بدون اجرای command دلخواه کاربر |
| XFOIL adapter | batch allowlisted، `shell=False`، tempdir مستقل، timeout و manifest failure |
| FastAPI worker | API key fail-closed، body limit، quota per credential، semaphore concurrency، `/healthz` و `/readyz` |
| container / Kubernetes | اجرای non-root، filesystem فقط‌خواندنی، capability drop، ClusterIP و secret mount |

**متن ارائه:** «design اصلی separation of concerns است. رابط کاربر نمی‌تواند command XFOIL تزریق کند. adapter فقط workflow اجازه‌داده‌شده را می‌سازد و worker failure را به status ساخت‌یافته تبدیل می‌کند؛ timeout یا process error به 500 مبهم تبدیل نمی‌شود.»

## Slide 6

**عنوان:** کنترل‌های امنیتی به policy قابل‌آزمون تبدیل شده‌اند

| کنترل | شواهد خودکار |
|---|---|
| auth و readiness fail-closed | بدون secret، polar API با 503 و readiness با 503 رد می‌شود |
| محدودیت resource و runtime | non-root، read-only root، seccomp RuntimeDefault، cap drop ALL و resource limits |
| network boundary | ingress فقط از namespace و pod label قراردادشده؛ egress فقط DNS kube-system |
| resilience regression | timeout، OSError، executable missing، quota و body-size boundary در testها پوشش دارند |
| in-cluster validation | runner پنج health call مجاز، readiness، DNS egress worker و denial caller بدون label را تست می‌کند |

**متن ارائه:** «Static test، صحیح‌بودن policy source را تضمین می‌کند. تست درون‌خوشه‌ای ثابت می‌کند CNI واقعاً policy را enforce می‌کند. این تمایز مهم است، چون NetworkPolicy بدون CNI enforcing فقط یک YAML زیبا است.» [3]

## Slide 7

**عنوان:** مسیر استقرار، از دمو تا عملیات کنترل‌شده

| مرحله | مناسب برای | مرز روشن |
|---|---|---|
| Streamlit Community Cloud | دمو، آموزش و نسخه عمومی بدون نصب | worker خارجی، secret عملیاتی و SLA در این لایه قرار نمی‌گیرد |
| Internal worker + Kubernetes | solver کنترل‌شده، policy، observability و scale | نیازمند digest pinning، secret rotation، gateway TLS/mTLS یا JWT و CNI enforcing |
| Production platform | مشتری سازمانی و SLA | SLO، monitoring، backup، capacity و incident process مالک مشخص می‌خواهند |

**متن ارائه:** «این مسیر، سرمایه‌گذاری زیرساخت را با کشش واقعی بازار هماهنگ می‌کند. محصول عمومی مستقل از solver production قابل نمایش است و worker تنها در مرز داخلیِ کنترل‌شده فعال می‌شود.»

## Slide 8

**عنوان:** تمایز محصول، کاهش چرخهٔ تصمیم با شفافیت است

| نیاز مشتری | پاسخ v3.1.2 | ارزش تجاری |
|---|---|---|
| iteration سریع geometry | NACA، UIUC import، comparison و batch/Pareto | کاهش زمان shortlist اولیه |
| تصمیم قابل بازبینی | audit manifest، conditions و hash geometry | همکاری تیمی و traceability |
| کاهش ریسک مدل | validation metrics، sensitivity و disclosure محدودیت | جلوگیری از overclaim و rework دیرهنگام |
| راه رشد solver | adapter/worker جدا و policy-controlled | مسیر ارتقا بدون بازنویسی رابط‌ها |

**متن ارائه:** «ما نرم‌افزار را با یک solver تنها تعریف نمی‌کنیم. مزیت، workflow منسجم از geometry تا evidence است که هم برای engineer کاربردی و هم برای team lead قابل دفاع است.»

## Slide 9

**عنوان:** roadmap، از screening به evidence-backed design workspace

| افق | اولویت | معیار خروج |
|---|---|---|
| 0–3 ماه | XFOIL worker staging، validation pack NACA 0012، monitoring | گزارش reproducible و policy test پاس‌شده در CNI enforcing |
| 3–6 ماه | multi-condition optimization با thickness/moment/manufacturing constraints | objectiveهای mission-based و sensitivity report |
| 6–12 ماه | workspace سازمانی، مطالعه‌های خصوصی، collaboration و audit governance | کنترل دسترسی، storage policy و lifecycle study |

**متن ارائه:** «roadmap بر ادعای feature بیشتر متمرکز نیست؛ بر افزایش fidelity evidence و کاهش ریسک adoption متمرکز است. هر مرحله معیار فنیِ قابل‌اندازه‌گیری دارد.»

## Slide 10

**عنوان:** درخواست تصمیم: اعتبارسنجی، pilot و بسته‌بندی تجاری

**زیرعنوان:** v3.1.2 آمادهٔ اثبات ارزش در یک pilot کنترل‌شده است

**متن ارائه:** «در این نقطه محصول یک پایهٔ مهندسی و operational قابل‌دفاع دارد: screening، validation workflow، robust Pareto، worker امن و deployment path. تصمیم بعدی، انتخاب یک mission محدود برای pilot، ثبت دادهٔ مرجع و تبدیل نتایج به evidence package است. هدف، فروش یک نمودار نیست؛ ارائهٔ یک مسیر قابل‌اعتماد از geometry تا تصمیم است.»

## References

[1]: https://m-selig.ae.illinois.edu/ads/coord_database.html "UIUC Airfoil Coordinates Database"
[2]: https://web.mit.edu/drela/Public/web/xfoil/ "XFOIL — Mark Drela, MIT"
[3]: https://kubernetes.io/docs/concepts/services-networking/network-policies/ "Kubernetes Network Policies"
