# یادداشت‌های پژوهش بازار، رقبا و رگولاتوری

**تاریخ مرجع:** ۱۴ اوت ۲۰۲۶
**کاربرد:** ورودی مستند برای انتخاب beachhead، مدل قیمت‌گذاری، معماری محصول و برنامهٔ عرضه.
**روش:** فقط منابع رسمی یا مستندات اولیهٔ ابزارها در این مرحله استفاده شده‌اند. ارقام تجاریِ ثالث یا پیش‌بینی‌های فاقد مبنای قابل‌بررسی در این یادداشت وارد نشده‌اند.

## یافته‌های بازار و buyer context

سازمان FAA در صفحهٔ پیش‌بینی هوافضا، forecast سال‌های ۲۰۲۶ تا ۲۰۴۶ را شامل fleetهای UAS، Advanced Air Mobility و remote pilot می‌داند؛ این موضوع وجود یک زیرساخت رسمی و بلندمدت برای برنامه‌ریزی اکوسیستم UAS را تأیید می‌کند، اما به‌تنهایی اندازهٔ بازار قابل‌دستیابی برای نرم‌افزار حاضر را اثبات نمی‌کند. [1]

صفحهٔ رسمی UAS FAA، کاربرانی از جمله remote pilot تجاری، public-safety، education، عملیات پیشرفته، research و testing را به‌عنوان گروه‌های عملیاتی تفکیک می‌کند. برای محصول فعلی، این نکته از فرضیهٔ تمرکز اولیه بر تیم‌های کوچک طراحی و آموزش/UAS پشتیبانی می‌کند؛ با این حال، willingness-to-pay هر گروه هنوز باید از طریق interview و pilot سنجیده شود. [2]

در اروپا، EASA اعلام می‌کند که بیش از ۱.۶ میلیون drone operator ثبت‌شده تحت یک مجموعه قواعد اتحادیه فعالیت می‌کنند. این یک شاخص از گستردگی اکوسیستم است، نه شمار مستقیم مشتریان بالقوهٔ نرم‌افزار airfoil. [3]

## یافته‌های رقابتی

| بازیگر / جایگزین | واقعیت مستند | دلالت راهبردی برای NACA Airfoil Kit Pro |
|---|---|---|
| QBlade / QFoil | QBlade تحلیل XFoil و QFoil را در workflow ایجاد polar قرار می‌دهد؛ پارامترهای Re، Mach، Ncrit و forced transition را عرضه می‌کند و batch analysis در بازهٔ Reynolds دارد. [4] | «چند-Re بودن» به‌تنهایی مزیت نیست. باید روی traceability، validation package، UX سریع‌تر و study/audit workflow تمرکز شود. |
| QFoil | QFoil نسبت به XFoil بر robustness و viscous/post-stall واقع‌گرایانه‌تر تمرکز دارد، اما خود مستندات تفاوت نتایج و نیاز به re-validation را هشدار می‌دهد. [5] | solver version، parameter set و dataset provenance باید برای هر polar ثبت شوند؛ جایگزینی solver بدون validation قابل‌قبول نیست. |
| XFLR5 / flow5 | XFLR5 تحلیل مستقیم/معکوس XFoil و تحلیل بال/هواپیما با lifting-line، VLM و 3D panel را اعلام می‌کند؛ صفحهٔ آن پایان پروژه در ژوئن ۲۰۲۶ را گزارش می‌کند و محصول را بدون تضمین حرفه‌ای معرفی می‌کند. [6] | فرصت white space در workflow مدرن، پشتیبانی، auditability و مسیر collaboration وجود دارد؛ system-level analysis نباید پیش از polar quality gates اضافه شود. |
| روش دستی و spreadsheet | در محصول‌های آموزش و تیم‌های کوچک، spreadsheet/فایل coordinate و ابزارهای open-source جایگزین اصلی‌اند. | conversion نیازمند time-to-first-study کوتاه، import/export باز و گزارش قابل‌ارسال است، نه lock-in زودهنگام. |

## محدودیت‌های رگولاتوری و اعتماد

Part 107 FAA، عملیات تجاری sUAS زیر ۵۵ پوند را پوشش می‌دهد و در کنار قواعد عملیاتی، ثبت، گواهی remote pilot، waiver و airspace authorization را تشریح می‌کند. این مقررات مستقیماً software airfoil را certify نمی‌کنند؛ اما نشان می‌دهند که طراحی UAV در زمینهٔ regulated operations استفاده می‌شود. بنابراین محصول نباید به‌صورت ضمنی یا صریح وعدهٔ compliance یا airworthiness بدهد. [7]

EASA در اروپا، دستهٔ open را مرجع عمدهٔ فعالیت‌های تفریحی و برخی فعالیت‌های تجاری low-risk معرفی می‌کند و برای دسته‌های C0 تا C4 محدودیت‌های متفاوتی درج می‌کند. این طبقه‌بندی به معنای آن نیست که airfoil tool حاضر برای طراحی compliant کافی است. [8]

EASA توضیح می‌دهد که DPIA طبق مادهٔ ۳۵ GDPR هنگامی لازم است که پردازش personal data احتمالاً ریسک بالا برای حقوق و آزادی‌های افراد داشته باشد. در مراحل فعلی، NACA Airfoil Kit Pro اساساً geometry و study data را پردازش می‌کند؛ با ورود cloud collaboration، کاربران سازمانی، telemetry یا attachmentهای mission، data map، DPA، retention policy، access control و احتمالاً DPIA باید به‌صورت مرحله‌ای اضافه شوند. [9]

## برداشت اولیهٔ قابل‌آزمون

**Beachhead پیشنهادی:** تیم‌های کوچک و مشاوران در طراحی اولیهٔ UAS/propeller/rotor و education/research که به workflow سریع، قابل‌آموزش و قابل‌تحویل نیاز دارند ولی برای solver enterprise یا pipeline دست‌ساز، هزینه/پیچیدگی بالایی دارند.

**علت انتخاب:** این بخش نسبت به aerospace certification حساسیت کمتری دارد، با قابلیت‌های موجود product fit بیشتری دارد، و می‌تواند pilotهای کوچک و قابل‌اندازه‌گیری فراهم کند. این انتخاب هنوز «فرضیه با اطمینان متوسط» است و باید با حداقل ۱۰ مصاحبهٔ ساخت‌یافته و ۳ تا ۵ pilot سنجیده شود.

**موضع‌گیری پیشنهادی:** «Engineering screening workspace with evidence and traceability»؛ نه «جایگزین CFD» و نه «airfoil generator عمومی». این positioning باید با landing-page/fake-door، interview و نرخ activation بررسی شود.

## شکاف‌های داده‌ای که قبل از TAM قطعی باید پر شوند

| دادهٔ لازم | دلیل | روش اعتبارسنجی |
|---|---|---|
| تعداد buyerهای هدف در هر geography | ساخت TAM/SAM/SOM bottom-up | logo universe از associations، directories و outbound list؛ deduplication دستی |
| willingness-to-pay و frequency استفاده | انتخاب tier و unit economics | مصاحبه، pricing survey، fake-door و paid pilot |
| جایگزین‌های واقعی workflow | ارزیابی switching cost | observe current toolchain در مصاحبه و نمونهٔ study واقعی |
| کانال acquisition و CAC | feasibility beachhead | آزمون محتوای technical، partnership دانشگاهی/مجتمع، outreach محدود |
| requirements privacy/security enterprise | مرز product architecture | discovery با design partner؛ DPA/security questionnaire |

## منابع

[1]: https://www.faa.gov/data_research/aviation/aerospace_forecasts "FAA Aerospace Forecasts"
[2]: https://www.faa.gov/uas "FAA — Drones / UAS"
[3]: https://www.easa.europa.eu/en/domains/civil-drones "EASA — Drones & Air Mobility"
[4]: https://docs.qblade.org/src/user/airfoil/airfoil_analysis.html "QBlade — Airfoil Analysis Overview"
[5]: https://docs.qblade.org/src/theory/aerodynamics/qfoil/qfoil.html "QBlade — QFoil Airfoil Analysis Code"
[6]: https://www.xflr5.tech/ "XFLR5 — General Description"
[7]: https://www.faa.gov/newsroom/small-unmanned-aircraft-systems-uas-regulations-part-107 "FAA — Small UAS Regulations (Part 107)"
[8]: https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/open-category-low-risk-civil-drones "EASA — Open Category"
[9]: https://www.easa.europa.eu/en/domains/civil-drones/privacy/data-protection-impact-assessment "EASA — Data Protection Impact Assessment"


## یافته‌های pricing و packaging رقبا

| بازیگر | بسته‌بندی/قیمت منتشرشده | تفسیر راهبردی |
|---|---|---|
| DesignFOIL | صفحهٔ رسمی، demo کامل و قیمت دانشجویی ۱۰ دلار را اعلام می‌کند؛ در کنار generation، virtual wind tunnel، CSV/CAD export، flap و wing layout را فهرست می‌کند. [10] | برای دانشجو و hobbyist، قیمت‌محور بودن بازار واقعی است؛ NACA Airfoil Kit نباید بدون متمایزسازیِ workflow/audit با یک paywall ساده رقابت کند. |
| AeroFoil | trial چهارده‌روزه، Lite پایدار و licence تک‌کاربره بین ۲۰ تا ۱۵۰ دلار را اعلام می‌کند؛ inverse design و comparison تا سه airfoil را عرضه می‌کند. [11] | یک tier entry/perpetual می‌تواند برای desktop مناسب باشد، اما ادعای دقت رقبا باید مستقل از marketing copy و با benchmark جداگانه ارزیابی شود. |
| AirShaper | pricing رسمی سالانه و credit-based برای CFD سه‌بعدی منتشر می‌کند: Discovery €990 شامل ۲۵ credit، Professional €2990 شامل ۱۰۰ credit و Enterprise سفارشی با API، batch و multiple seats. [12] | این محصول رقیب مستقیم ۲D airfoil نیست، اما سقف willingness-to-pay برای workflowهای حرفه‌ای aero و منطق tiering بر پایهٔ fidelity/credits/collaboration را نشان می‌دهد. |

**نتیجهٔ اولیه:** بهترین pricing architecture برای محصول فعلی به‌صورت hybrid است: یک مسیر free/education برای اثبات first value، desktop/individual با annual یا perpetual محدود برای workflow سریع، و tier حرفه‌ای/enterprise تنها پس از تکمیل private studies، collaboration، deployment و evidence packs. قیمت‌های پیشنهادی باید در pilot آزمایش شوند و فعلاً به‌عنوان fact بازار مطرح نشوند.

[10]: https://www.dreesecode.com/ "DreeseCODE — DesignFOIL"
[11]: https://aerofoilengineering.com/ "AeroFoil Engineering — AeroFoil"
[12]: https://airshaper.com/pricing "AirShaper — Pricing"
