# طرح تجاری و محصول جهانی — NACA Airfoil Kit Pro

**نسخه:** ۰.۱ — فرضیه‌محور و قابل‌آزمون
**تاریخ مرجع:** ۱۴ اوت ۲۰۲۶
**افق برنامه‌ریزی:** ۱۲ ماه عملیاتی و ۵ سال برای market-sizing بعدی
**مبنای داده:** قابلیت‌های واقعی مخزن، مستندات رسمی رقبا/رگولاتورها، و فرضیات صریح. این سند، ارزش‌گذاری یا توصیهٔ سرمایه‌گذاری شخصی نیست.

## Executive Summary

فرصت واقعی NACA Airfoil Kit Pro فروش «یک generator ایرفویل دیگر» نیست. بازار در این سطح با ابزارهای رایگان، نرم‌افزارهای desktop کم‌هزینه و solverهای تخصصی پوشش دارد. فرصت قابل‌دفاع، ساخت یک **workspace سبک و قابل‌ردیابی برای تصمیم طراحی مقدماتی** است: کاربر geometry را وارد یا تولید می‌کند، رفتار را در چند condition غربال می‌کند، shortlist مقاوم می‌سازد، فاصلهٔ مدل از evidence را می‌بیند و یک study package قابل‌بازبینی تحویل می‌دهد.

پیشنهاد beachhead، تیم‌های کوچک طراحی UAS/propeller/rotor، مشاوران مستقل و گروه‌های تحقیق/آموزش حرفه‌ای است که در مرحلهٔ concept-to-shortlist قرار دارند. این انتخاب بر product fit موجود، چرخهٔ فروش کوتاه‌تر و ریسک certification پایین‌تر از aerospace OEMهای اصلی استوار است؛ اما هنوز یک **فرضیه با اطمینان متوسط** است و قبل از توسعهٔ بزرگ باید با مصاحبه و pilot پولی یا مشروط آزموده شود.

> تصمیم راهبردی: در ۹۰ روز آینده، محصول باید بر **activation، validation evidence و pilot conversion** متمرکز شود؛ نه بر افزودن هم‌زمان wing solver، marketplace، community یا AI chatbot.

## Opportunity

FAA در forecast رسمی ۲۰۲۶–۲۰۴۶ خود، UAS، Advanced Air Mobility و remote pilot را به‌عنوان بخش‌های forecast‌شده می‌آورد؛ EASA نیز بیش از ۱.۶ میلیون drone operator ثبت‌شده در اروپا گزارش می‌کند. این دو داده، وجود یک اکوسیستم گسترده و در حال نهادینه‌شدن را نشان می‌دهند، اما نه TAM مستقیم یک نرم‌افزار airfoil. [1] [2]

فرصت نزدیک‌تر، پراکندگی workflow در سطح concept design است. ابزارهای موجود قابلیت‌های عمیق دارند، اما تجربهٔ کاربر غالباً میان فایل coordinate، spreadsheet، solver، plot و گزارش جداگانه تقسیم می‌شود. NACA Airfoil Kit می‌تواند با قرار دادن provenance، validation و robust ranking در همان مسیر تحلیل، تصمیم اولیه را قابل‌توضیح کند.

| عامل | شواهد / فرضیه | اثر راهبردی |
|---|---|---|
| رشد و نهادینه‌شدن UAS/AAM | forecast رسمی FAA و اکوسیستم مقرراتی اروپا [1] [2] | beachhead UAS ارزش آزمون دارد، اما نباید با TAM قطعی اشتباه گرفته شود. |
| نیاز به multi-condition workflow | QBlade به batch analysis در Re و پارامترهای transition تکیه دارد. [3] | robust Pareto و sensitivity موجود باید محور positioning باشند. |
| pricing reference در low-end | AeroFoil licence تک‌کاربره $20–$150 و DesignFOIL student price $10 را منتشر می‌کنند. [4] [5] | tier دانشجویی/individual باید ساده و کم‌اصطکاک باشد. |
| willingness-to-pay high-end | AirShaper annual credit plan از €990 آغاز می‌کند. [6] | قیمت حرفه‌ای فقط با evidence، service و workflow collaboration قابل توجیه است. |

## Problem

**برای چه کسی؟** مهندس یا طراح کوچک که باید چند گزینهٔ airfoil را در چند condition بررسی کند، تصمیم را برای reviewer توضیح دهد و از سوءبرداشت نتیجهٔ panel/empirical model جلوگیری کند.

**درد اصلی:** سرعت تحلیل اولیه معمولاً با قابلیت اعتماد و ردگیری trade-off دارد. ابزار ساده، evidence و provenance ناکافی دارد؛ ابزار دقیق، onboarding و هزینهٔ زیاد دارد؛ و workflow دستی، دانش سازمانی را در فایل‌ها پخش می‌کند.

**راهکارهای فعلی و نقص آن‌ها:** XFLR5 و XFoil ابزارهای مهمی هستند، اما XFLR5 خود را رایگان، بدون تضمین حرفه‌ای و عمدتاً برای model aircraft معرفی می‌کند. [7] QBlade قابلیت batch و solverهای ۲D را فراهم می‌کند اما در حوزهٔ wind/rotor workflow تخصصی‌تر قرار دارد. [3] ابزارهای CFD سه‌بعدی مانند AirShaper به مسئله‌ای با fidelity و قیمت متفاوت پاسخ می‌دهند. [6]

## Target Customer

| رتبه | segment | job-to-be-done | درد قابل‌سنجش | پیشنهاد اولیه |
|---|---|---|---|---|
| ۱ | تیم ۲ تا ۱۰ نفره UAS/propeller/rotor در concept phase | تبدیل سریع geometry به shortlist و گزارش برای review | زمان، پراکندگی ابزار، uncertainty | Team Pilot: robust study + validation package + support محدود |
| ۲ | مشاور aero / design bureau | تحویل study قابل‌تکرار به مشتری | credibility، provenance، report cycle | Pro: audit package، branded report و project archive |
| ۳ | آزمایشگاه/دانشگاه و تیم مهندسی دانشجویی | آموزش workflow درست و experiment comparison | بودجه محدود، onboarding | Education: رایگان/تخفیف‌دار، محدودیت scope و بدون ادعای production |
| ۴ | OEM یا operator regulated | evidence package در کنار toolchain موجود | compliance، security، procurement | فقط پس از private deployment، SSO/RBAC و security review |

**عدم تمرکز در سال اول:** certification-heavy OEM، عملیات mission-critical، یا مشتریانی که از روز اول CFD سه‌بعدی/structural coupling/PLM کامل می‌خواهند. این‌ها ظرفیت فروش بالاتر دارند اما product gap، procurement cost و ریسک حقوقی بالاتری دارند.

## Value Proposition

**Core value proposition:** «از geometry تا study قابل‌ردیابی در چند دقیقه؛ با نشان‌دادن محدودیت مدل، نه پنهان‌کردن آن.»

**Unique selling proposition:** ترکیب single-click geometry workflow، multi-condition robust ranking، validation residual، audit manifest و solver-upgrade path در یک محصول با disclosure صریح preliminary screening.

**Killer feature که باید به محصول عرضه‌شده تبدیل شود:** `Evidence-Ready Study Package` شامل coordinate/condition، chart، ranking، validation metrics، manifest solver/model و quality flag. این package باید چیزی باشد که کاربر برای colleague یا customer ارسال می‌کند.

### Customer Journey

| نقطهٔ زمانی | تجربهٔ مطلوب | شاخص اندازه‌گیری |
|---|---|---|
| ۳۰ ثانیهٔ اول | کاربر می‌فهمد محصول برای screening است و می‌تواند NACA یا profile واقعی را باز کند. | landing-page → app start conversion |
| ۵ دقیقهٔ اول | کاربر یک polar/robust comparison و exportable study می‌سازد. | time-to-first-study، export rate |
| روز اول | کاربر یک dataset مرجع یا comparison دوم اضافه می‌کند. | validation/compare feature adoption |
| هفتهٔ اول | کاربر study جدیدی با condition متفاوت می‌سازد یا study را share می‌کند. | weekly retained activated users |
| ماه اول | تیم pilot report را در review واقعی به کار می‌برد. | pilot-to-paid conversion و qualitative evidence |

## Product Strategy

### محصول اکنون

محصول فعلی باید یک **screening workspace** باشد. موارد زیر در پیام فروش و UI حفظ می‌شوند: preliminary scope، عدم‌کفایت برای certification/safety-critical، نیاز به validation، و تفاوت solver/model provenance. موارد زیر نباید ادعا شوند: «validated» عمومی، post-stall دقیق، final drag prediction یا compliance design.

### Roadmap Now / Next / Later

| اولویت | اقدام | مسئله‌ای که حل می‌کند | معیار خروج |
|---|---|---|---|
| **Now** | guided first-study onboarding + starter workflows | کاهش time-to-first-value | ≥60% کاربران جدید به study exportable برسند؛ baseline ابتدا ثبت شود. |
| **Now** | Evidence-Ready Study Package و quality flag | reviewability و جلوگیری از overclaim | هر export شامل condition/provenance/scope باشد. |
| **Now** | event instrumentation با privacy-by-design | سنجش activation و retention | event dictionary و opt-in/retention policy روشن. |
| **Now** | design-partner pilot toolkit | تبدیل hypothesis به evidence | ۳–۵ pilot با brief، success metric و review ثبت‌شده. |
| **Next** | constraint-aware optimizer و solver provenance برای XFOIL | کاهش خروجی غیرقابل‌ساخت و افزایش fidelity قابل‌ردیابی | constraints و solver version در manifest. |
| **Next** | private studies، RBAC سبک و project archive | خرید تیمی و switching cost | security review و data retention policy. |
| **Later** | wing/rotor performance | پیوند section به mission performance | فقط با polar quality gate و validation. |
| **Later** | API/versioned integrations | ارزش enterprise و automation | rate limit، auth، versioning و audit log. |
| **Maybe** | AI copilot برای quality checks | کاهش خطای workflow | اثبات KPI: زمان study یا خطای metadata را کاهش دهد. |
| **Do Not Do** | generic chatbot، marketplace، certification claim، social feed | feature sprawl / legal exposure | تا زمانی که product-market evidence نداریم، انجام نشود. |

## Competitive Advantage and White Space

| حوزه | بازار موجود | White space قابل‌دفاع |
|---|---|---|
| geometry / basic analysis | free/open-source و desktop tools بسیارند. [4] [5] [7] | اینجا moat نیست؛ باید free/low-friction entry باشد. |
| viscous solver | QBlade/XFoil/QFoil workflowهای بالغ دارند. [3] | provenance، failure handling، policy-controlled worker و validation integration. |
| inverse design | AeroFoil و برخی ابزارها inverse design عرضه می‌کنند. [4] | تا قبل از constraint/evidence، رقابت مستقیم روی inverse design اشتباه است. |
| 3D CFD | AirShaper workflow credit-based و 3D ارائه می‌کند. [6] | position به‌عنوان سریع‌ترین مرحلهٔ قبل از CFD، نه جایگزین آن. |
| team decision | ابزارهای کوچک عموماً فایل‌محور هستند. | study archive، manifests، review-ready exports و private collaboration. |

**Moat واقع‌بینانه:** دادهٔ مطالعهٔ معتبر + metadata + history تصمیم + workflow integration. «الگوریتم panel» یا «یک chart» به‌تنهایی moat نیست.

## Business Model and Monetization

مدل پیشنهادی از سه خط درآمدی منطقی تشکیل می‌شود، نه ده مدل هم‌زمان.

| جریان درآمد | مشتری | premise | وضعیت |
|---|---|---|---|
| Free / Education | learner و evaluator | ایجاد first value و pipeline آموزشی؛ محدودیت export/private storage | hypothesis برای آزمایش |
| Individual / Pro subscription یا desktop licence | مشاور و مهندس مستقل | full screening workspace، report templates و study archive محلی | hypothesis برای آزمایش قیمت |
| Team / Enterprise pilot | تیم کوچک و design partner | private studies، review workflow، support و deployment configuration | اولویت درآمدی؛ نیازمند pilot |

### قیمت‌گذاری آزمایشی، نه price list نهایی

| tier | فرض قیمت آزمایشی | offer | سؤال اعتبارسنجی |
|---|---:|---|---|
| Education | $0 تا $10 ماهانه یا licence دانشجویی محدود | learning workflow و export آموزشی | آیا دانشجو/دانشگاه activation و referral ایجاد می‌کند؟ |
| Individual | $19 تا $29 ماهانه | study, robust compare, report/audit exports | آیا user مستقل ماهانه ≥۲ study تکرارشونده می‌سازد؟ |
| Team | $79 تا $99 به‌ازای workspace در ماه | shared/private study، review workflow و support محدود | آیا تیم برای time savings و auditability پرداخت می‌کند؟ |
| Pilot | $1,500 تا $7,500 برای scope محدود | onboarding، data import، validation review و success report | آیا outcome مشخص باعث conversion می‌شود؟ |
| Enterprise | quote-based | private deployment، SSO/RBAC، security review، API | فقط پس از readiness فنی و procurement discovery |

قیمت‌ها **فرضیات عملیاتی** هستند، نه دادهٔ بازار یا تعهد فروش. محدودهٔ low-end با قیمت‌های منتشرشدهٔ DesignFOIL و AeroFoil و سطح high-end با AirShaper triangulate شده، ولی selection واقعی فقط از interview، fake-door و pilot می‌آید. [4] [5] [6]

## Financial Model

### پایه و مفروضات

مدل زیر forecast حسابداری یا valuation نیست. یک operating model سال اول است تا حجم لازم برای آزمایش price/segment را شفاف کند. همهٔ مشتریان، قیمت‌ها و ۸۵٪ gross margin **فرضیات برنامه‌ریزی** هستند. margin صرفاً یک هدف قبل از هزینه‌های تیم، فروش، حقوقی و جذب مشتری است؛ نه واقعیت ثبت‌شده.

| سناریو | Individual | Team | Pilot | Usage add-on | ARR / revenue سال اول | gross profit فرضی با ۸۵٪ |
|---|---:|---:|---:|---:|---:|---:|
| محتاطانه | 20 × $19/mo | 3 × $79/mo | 1 × $1,500 | — | $8,904 | $7,568.40 |
| پایه | 50 × $29/mo | 10 × $99/mo | 3 × $5,000 | — | $44,280 | $37,638.00 |
| جسورانه | 100 × $29/mo | 25 × $99/mo | 8 × $7,500 | 5 × $100/mo | $130,500 | $110,925.00 |

فرمول‌ها به‌ترتیب عبارت‌اند از: `Individual customers × monthly price × 12 + Team workspaces × monthly price × 12 + Pilot fees + Usage accounts × monthly price × 12`. سناریوی پایه شامل $17,400 درآمد individual، $11,880 درآمد team و $15,000 درآمد pilot است. این ساختار نشان می‌دهد که در سال اول، pilotهای محدود می‌توانند سهم مهمی از cash learning داشته باشند؛ اما business نباید وابستگی بلندمدت به خدمات داشته باشد.

**Gate مالی:** تا وقتی که حداقل سه design partner یک outcome قابل‌اندازه‌گیری و willingness-to-pay واقعی ارائه نکرده‌اند، سرمایه‌گذاری بزرگ در paid acquisition، build-out enterprise یا تیم فروش پیشنهاد نمی‌شود.

## Go-to-Market and Growth Strategy

| موتور رشد | اقدام ۹۰ روزه | KPI اولیه | ریسک |
|---|---|---|---|
| Product-led | landing page با مسیر «اولین study در ۵ دقیقه» و templateهای sample | signup→first-study و first-study→export | بازدید آموزشی بدون intent خرید |
| Technical content | ۳ case study روش‌شناسی: NACA 0012 validation، multi-Re shortlist، report provenance | qualified leads و completion rate | content بدون distribution |
| Partnership | ۲ دانشگاه/آزمایشگاه و ۳ مشاور/تیم UAS برای pilot | pilot acceptance و feedback quality | partner به customer تبدیل نشود |
| Outbound focused | ۵۰ prospect دقیق در یک beachhead، نه تبلیغ وسیع | interview booked، paid-pilot rate | پیام اشتباه یا ICP مبهم |
| Referral | shareable evidence package با attribution کنترل‌شده | share-to-signup | leakage دادهٔ study؛ نیازمند permission |

North Star Metric پیشنهادی: **تعداد studyهای evidence-ready که توسط کاربران فعال ایجاد و export می‌شوند.** این metric باید با conversion ترکیب شود تا صرفاً تولید نمودار را به‌اشتباه رشد تلقی نکنیم.

### AARRR

| مرحله | گلوگاه محتمل | اقدام |
|---|---|---|
| Acquisition | پیام بیش‌ازحد عمومی «airfoil tool» | landing page بر اساس job-to-be-done و use case beachhead |
| Activation | کاربر با Re/alpha/roughness سردرگم است | guided study و template واقعی |
| Retention | product فقط یک‌بار برای آموزش استفاده می‌شود | project history، repeat conditions و alert برای provenance ناقص |
| Revenue | offer مبهم و نداشتن outcome | pilot outcome + tier boundaries روشن |
| Referral | export بدون هویت/اثبات ارزش share می‌شود | evidence package، permissioned share link و case-study attribution |

## Global Strategy

معیار پیشنهادی Global Expansion Score شامل demand، product fit، payment/procurement، regulation clarity، cost of localization، partner availability و support complexity است. تا زمانی که دادهٔ logo universe و conversion واقعی نداریم، این امتیاز یک framework کیفی است نه ranking بازار قطعی.

| بازار | ارزیابی کارکردی | اولویت پیشنهادی | سطح اطمینان |
|---|---|---|---|
| ایالات متحده | اکوسیستم UAS رسمی، کانال technical-content/education قابل‌دسترسی و beachhead انگلیسی‌زبان [1] | ۱ — اولین pilot و content | متوسط |
| اتحادیه اروپا/انگلیسی‌زبان EMEA | قواعد نسبتاً هماهنگ EASA و ecosystem گسترده، ولی privacy/procurement حساس‌تر [2] [8] | ۲ — بعد از data/privacy baseline | متوسط |
| کانادا/استرالیا/نیوزیلند | زبان مشترک و market entry ساده‌تر به‌صورت فرضی | ۳ — بعد از evidence US/EU | پایین؛ نیازمند research مستقل |
| MENA/APAC/LATAM | فرصت بالقوه، اما تفاوت payments، language و regulation بالاتر | Later | پایین؛ فعلاً research-only |

### Localization Without Rebuilding

1. تمام copyها به resource file منتقل شوند؛ calculations و engineering terms از زبان جدا باشند.
2. template report، تاریخ، decimals، units و currency configurable باشند.
3. region-specific privacy/retention و storage policy از product settings جدا شوند.
4. pricing page و entitlement layer چندارزی و tax-aware طراحی شوند؛ payment و tax integration فقط پس از انتخاب jurisdiction و provider.

## Technology and AI Strategy

### فناوری

معماری فنی باید lean باقی بماند: Streamlit برای self-serve evaluation و desktop برای local workflow ادامه یابد؛ solver worker در boundary داخلی و policy-controlled قرار گیرد. با افزایش team use، backend باید ابتدا به authentication، study storage، audit log، RBAC و secret management ارتقا یابد، نه به microserviceهای متعدد.

### AI

**Safe:** rule-based metadata assistant که Re، alpha range، geometry source و validation condition ناقص را قبل از export flag کند. KPI: کاهش studyهای ناقص.

**Smart:** copilot محدود به context study که تفاوت بین model و experimental residual را خلاصه می‌کند و user را به validation guideline هدایت می‌کند. KPI: کاهش زمان review بدون خلق ادعای فنی جدید.

**Bold:** recommendation engine که از studyهای permissioned، anonymized و metadata-complete برای پیشنهاد candidate/design space استفاده می‌کند. پیش‌نیاز: consent، governance، model validation و evidence کافی.

**Moonshot Opportunity:** یک «evidence graph» از geometry، condition، solver/version، experimental data و review outcomes که به تیم‌ها کمک کند قابل‌اعتمادترین design space را برای mission خود بیابند. این کار، نه قبل از privacy، data quality و رضایت کاربر، بلکه در فاز platform مطرح می‌شود.

## Data, Security, Privacy and Trust

| سطح | اکنون | قبل از Team/Enterprise |
|---|---|---|
| Data | export/manifests محلی و provenance اولیه | data classification، retention، deletion و backup policy |
| Identity | session/local use | auth، verified email، RBAC، access reviews |
| Security | worker hardening و NetworkPolicy test suite | secret rotation، image digest pinning، monitoring، incident process |
| Privacy | حداقل‌سازی داده در study workflows | DPA، subprocessors register، region policy، DPIA trigger assessment |
| Trust | disclosure preliminary scope | status page، security questionnaire، audit logs و customer evidence policy |

EASA توضیح می‌دهد که DPIA در شرایط پردازش personal data با احتمال high risk طبق Article 35 GDPR لازم است. [9] برای محصول فعلی، این یک محرک معماری آینده است، نه اینکه هر study airfoil ذاتاً DPIA می‌خواهد. ادغام cloud collaboration نباید پیش از مالکیت data flow و retention انجام شود.

## Risks and Failure Scenarios

| ریسک/فرض شکست | احتمال | اثر | mitigation |
|---|---|---|---|
| مشتری tool رایگان را کافی بداند | بالا | بالا | focus روی evidence package/pilot outcome و نه generator؛ WTP interview پیش از build. |
| دقت مدل بیش‌ازحد برداشت شود | متوسط | بسیار بالا | UI/export disclosure، validation gate و منع claims certification. |
| feature sprawl هزینه را بالا ببرد | بالا | بالا | Now/Next/Later gate و توقف هر feature بدون KPI. |
| solver worker production-ready فرض شود | متوسط | بالا | staged deployment، external penetration/security review و CNI enforcement validation. |
| pilotها بدون پرداخت یا repeat use باشند | متوسط | بالا | success criteria، fee/LOI و stop/go checkpoint. |
| privacy/security enterprise مانع فروش شود | متوسط | بالا | private deployment path، DPA/RBAC/retention roadmap؛ عدم وعدهٔ SLA زودهنگام. |
| competitor بزرگ bundling کند | متوسط | متوسط | workflow layer، domain evidence و open import/export؛ نه lock-in مصنوعی. |

## 90-Day Operating Plan

| بازه | deliverable | KPI / تصمیم |
|---|---|---|
| روز ۰–۳۰ | ۱۰ مصاحبهٔ problem discovery، landing page، guided first-study، event dictionary | انتخاب یک ICP، نه چند ICP؛ baseline activation. |
| روز ۳۱–۶۰ | ۳–۵ design partner، evidence-ready study package، pricing fake-door و proposal pilot | paid/committed pilot یا اصلاح positioning. |
| روز ۶۱–۹۰ | validation case studies، pilot reviews، retention cohort اولیه و price test | Go/No-go برای team storage و collaboration. |

## Immediate Next Actions

1. پیام public README و web onboarding را از «feature list» به «first evidence-ready study» تغییر دهید.
2. در app، starter workflow و quality checklist قبل از export اضافه کنید.
3. برای ۱۰ prospect مصاحبهٔ ساخت‌یافته تنظیم کنید؛ سوال اصلی «آخرین تصمیم airfoil شما چگونه گرفته شد و چه چیزی سخت بود؟» باشد، نه «آیا محصول ما را دوست دارید؟»
4. یک pilot brief استاندارد ایجاد کنید: scope، supplied data، success criteria، deliverables، legal disclaimer و fee/LOI.
5. هیچ feature بزرگ دیگری را پیش از ثبت activation/retention و evidence پرداختی اضافه نکنید.

## References

[1]: https://www.faa.gov/data_research/aviation/aerospace_forecasts "FAA Aerospace Forecasts"
[2]: https://www.easa.europa.eu/en/domains/civil-drones "EASA — Drones & Air Mobility"
[3]: https://docs.qblade.org/src/user/airfoil/airfoil_analysis.html "QBlade — Airfoil Analysis Overview"
[4]: https://aerofoilengineering.com/ "AeroFoil Engineering — AeroFoil"
[5]: https://www.dreesecode.com/ "DreeseCODE — DesignFOIL"
[6]: https://airshaper.com/pricing "AirShaper — Pricing"
[7]: https://www.xflr5.tech/ "XFLR5 — General Description"
[8]: https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/open-category-low-risk-civil-drones "EASA — Open Category"
[9]: https://www.easa.europa.eu/en/domains/civil-drones/privacy/data-protection-impact-assessment "EASA — Data Protection Impact Assessment"
