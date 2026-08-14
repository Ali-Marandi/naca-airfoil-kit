# ممیزی امنیتی و چک‌لیست سخت‌سازی XFOIL Worker

**تاریخ ممیزی:** 14 اوت 2026  
**دامنه:** `xfoil_worker_app.py`، `xfoil_adapter.py`، `Dockerfile.xfoil-worker`، `docker-compose.yml`، `.github/workflows/xfoil-worker.yml` و مسیر استقرار پیشنهادی.  
**روش:** بازبینی کد و پیکربندی، آزمون API درون‌پردازشی، آزمون static configuration و موفقیت build/smoke-test در CI. این گزارش **pen-test شبکه‌ای یا اسکن CVE زمان‌اجرا نیست**.

> **نتیجه اجرایی:** worker اکنون برای یک endpoint داخلیِ احرازهویت‌شده با محدودیت منابع، پایهٔ امنیتی مناسبی دارد؛ اما هنوز برای انتشار اینترنتی مستقیم یا محیط چندمستاجری بدون ingress، مدیریت secret، network policy و vulnerability scanning تکمیلی آماده نیست.

## وضعیت کنترل‌ها

| حوزه | کنترل مشاهده‌شده | ارزیابی |
|---|---|---|
| اجرای process | batch command allowlisted، `shell=False`، executable path deployment-controlled، timeout و tempdir per-run | **مؤثر** |
| ورودی | schema `extra=forbid`، حد 601 نقطه، دامنه عددی Re/Mach/alpha/transition، حد body 256 KiB | **مؤثر** |
| احراز هویت | API key از secret file یا env، fail-closed در نبود key، `compare_digest` | **مؤثر؛ تک‌کلیدی** |
| کنترل سوءاستفاده | semaphore یک‌تایی، timeout solver، rate limit per credential، CPU/memory/PID/ulimit | **مؤثر؛ quota محلی** |
| container | non-root UID 10001، read-only root، tmpfs محدود، `cap_drop: ALL` و `no-new-privileges` | **مؤثر** |
| شبکه | هیچ port عمومی Compose برای worker؛ health کم‌اطلاع | **جزئی؛ network policy ندارد** |
| supply chain | CI test-before-publish، SBOM و provenance attestation | **جزئی؛ scan/block gate ندارد** |
| observability | health check و log rotation محدود | **جزئی؛ audit event/alert عملیاتی ندارد** |

کنترل‌های non-root، حذف capability، جلوگیری از privilege escalation، filesystem read-only و limit منابع با توصیه‌های OWASP هم‌راستا هستند. OWASP همچنین بر scan image، secrets manager، شبکهٔ محدود و runtime policy تأکید دارد. [1] Docker توضیح می‌دهد که capability و cgroup به محدودسازی اختیار و کاهش اثر denial of service کمک می‌کنند، اما isolation container جایگزین hardening میزبان نیست. [2]

## یافته‌های اولویت‌دار

| شناسه | شدت | یافته | شواهد | اقدام لازم |
|---|---|---|---|---|
| XW-01 | بالا | ingress، TLS، mTLS/JWT و allowlist شبکه در repository تعریف نشده‌اند | Compose فقط `expose` دارد؛ ingress deploy نشده است | قبل از production، worker را private نگه دارید؛ فقط gateway/service مجاز را در network policy وارد کنید و TLS را در ingress terminate کنید |
| XW-02 | بالا | image و وابستگی‌ها به digest/lock hash کامل pin نشده‌اند و scan blocking ندارد | base image tag، `apt install xfoil` و rangeهای pip | digest base image، version pin + hash lock، Trivy/Grype و secret scan را به CI اضافه و high/critical policy را blocking کنید |
| XW-03 | بالا | API key یک shared static credential است؛ identity، rotation و revocation سراسری وجود ندارد | یک `XFOIL_WORKER_API_KEY_FILE` | secret manager، rotation، credential per caller و mTLS یا JWT در gateway را اضافه کنید؛ key را در log یا CI قرار ندهید |
| XW-04 | متوسط | rate limit فقط memory-local است و با replica/restart یا حمله connection-level کامل نیست | `defaultdict(deque)` در process | rate limit و connection/body deadline را در ingress/WAF اعمال کنید؛ برای scale-out از store مشترک استفاده کنید |
| XW-05 | متوسط | seccomp/AppArmor/SELinux، rootless daemon یا user namespace به deployment policy واگذار شده است | Compose تنها `no-new-privileges` دارد | Docker default seccomp را disable نکنید؛ AppArmor/SELinux یا policy معادل، rootless daemon/userns و host patch policy را اعمال کنید |
| XW-06 | متوسط | error/result message ممکن است tail stderr solver را به caller برگرداند | adapter structured message را پاسخ می‌دهد | پاسخ عمومی را به error code محدود کنید؛ stderr را redacted و فقط در log حفاظت‌شده با correlation ID نگه دارید |
| XW-07 | متوسط | API access audit و alert برای auth failure، 429، timeout و process error هنوز تعریف نشده است | health/log rotation فقط | structured audit event بدون secret، metrics، dashboard و alert threshold افزوده شود |
| XW-08 | کم | `/healthz` عمومی است | status کم‌اطلاع | فقط در internal network قابل دسترس باشد؛ ingress آن را از اینترنت route نکند |
| XW-09 | کم | `--proxy-headers` در command فعال است اما peer allowlist صریح ندارد | Dockerfile command | اگر proxy لازم نیست حذف شود؛ در غیر این‌صورت trusted proxy CIDR صریح پیکربندی شود |

## hardening اعمال‌شده در این بازبینی

در جریان ممیزی، worker به‌صورت fail-closed تغییر یافت: نبود key اکنون `503` می‌دهد مگر override توسعه‌ای صریح فعال باشد. API key از مسیر secret file خوانده می‌شود، مقایسه key constant-time است، rate limit per-credential و حد body افزوده شد و `/healthz` دیگر وضعیت دقیق executable را افشا نمی‌کند. responseهای worker نیز `Cache-Control: no-store` و `X-Content-Type-Options: nosniff` می‌گیرند.

Compose اکنون secret را از `XFOIL_WORKER_SECRET_FILE` به `/run/secrets/xfoil_worker_api_key` mount می‌کند؛ key در environment فایل Compose قرار نمی‌گیرد. UID runtime صریح است و علاوه بر limit پیشین، `nofile`، `nproc` و rotation log تنظیم شد. تست‌های worker این کنترل‌ها را می‌سنجند.

## چک‌لیست پیش از production

| مرحله | کنترل قابل‌تأیید | مالک پیشنهادی | وضعیت repository |
|---|---|---|---|
| P0 — بلوکه‌کننده | private network؛ ingress TLS؛ تنها client allowlisted؛ هیچ port/public route مستقیم | Platform | باز |
| P0 — بلوکه‌کننده | secret manager و rotation؛ key منحصر‌به‌سرویس؛ `XFOIL_ALLOW_INSECURE_NO_AUTH=false` | Platform/Security | باز |
| P0 — بلوکه‌کننده | scan CVE، secret scan و policy failure برای finding بحرانی/بالا | DevSecOps | باز |
| P1 | image digest و dependency lock hash؛ SBOM/provenance retained | DevSecOps | SBOM/provenance موجود؛ pin/scan باز |
| P1 | ingress rate/connection limit، body timeout و request ID | Platform | quota محلی موجود؛ ingress باز |
| P1 | seccomp/LSM، host patch cadence، rootless/user namespace | Platform | باز |
| P1 | redact stderr، structured audit event، metrics و alert | Engineering/SRE | باز |
| P2 | policy retention برای raw polar/artifact، backup و incident runbook | Engineering/SRE | باز |
| P2 | independent pen-test و load/abuse test در محیط staging | Security/QA | باز |

## معماری استقرار پیشنهادی

worker باید یک service **private** پشت gateway باشد. gateway TLS و authentication کاربر را برقرار می‌کند و فقط credential/service identity محدود را به worker منتقل می‌کند. worker نباید Docker socket، bind mount میزبان، shell interactive، network egress غیرضروری یا secret در source/image داشته باشد. API key header برای machine-to-machine داخلی مناسب است؛ FastAPI از API key header به‌عنوان security primitive پشتیبانی می‌کند، ولی repository باید تصمیم identity و rotation را به لایهٔ gateway/secrets manager بسپارد. [3]

برای cluster، context امنیتی باید non-root، privilege escalation ممنوع، capability drop، read-only root filesystem و seccomp profile را enforce کند. Kubernetes security context دقیقاً برای تعیین UID، capability و permission container طراحی شده است. [4]

## آزمون‌های اجراشده

کنترل‌های fail-closed auth، key صحیح/غلط، schema، quota 429، body-limit 413، header امنیتی، command allowlist، tempdir isolation و static Compose/CI اجرا و موفق شدند. موفقیت CI قبلی نیز build محدودشده container، smoke test و publication image را تأیید کرده است. Docker daemon محلی این جلسه در دسترس نبود؛ بنابراین ارزیابی runtime محلی با test suite و CI جایگزین شد.

## منابع

[1]: https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html "OWASP Docker Security Cheat Sheet"
[2]: https://docs.docker.com/engine/security/ "Docker Engine Security"
[3]: https://fastapi.tiangolo.com/reference/security/ "FastAPI Security Tools"
[4]: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ "Kubernetes: Configure a Security Context"
