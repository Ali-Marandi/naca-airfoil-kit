# اعتبارسنجی خودکار شبکه و NetworkPolicy برای XFOIL Worker

**دامنه:** worker XFOIL، readiness، manifestهای Kubernetes و مسیر آزمون allow/deny شبکه.  
**هدف:** اثبات این‌که worker فقط از caller برچسب‌دار ترافیک دریافت می‌کند، DNS مجاز خود را از دست نداده است و endpoint تنها وقتی برای traffic آماده می‌شود که credential و executable solver صحیح باشند.

## معماری آزمون

اعتبارسنجی در دو لایه انجام می‌شود. لایه اول در CI و بدون نیاز به خوشه اجرا می‌شود؛ syntax runner، contract labelها، رفتار `/healthz` و `/readyz`، secret boundary و قیدهای static manifest را بررسی می‌کند. لایه دوم در staging Kubernetes اجرا می‌شود؛ این لایه تنها راه اثبات enforcement واقعی توسط CNI است، زیرا Kubernetes NetworkPolicy بدون network plugin دارای enforcement مؤثر نیست. [1]

| لایه | artifact | چه چیزی ثابت می‌شود | محدودیت |
|---|---|---|---|
| unit/static | `test_xfoil_network_validation.py` و testهای worker/manifests | runner معتبر است؛ allowlist labelها و DNS-only egress در source حفظ شده‌اند | عبور واقعی packet در CNI را اثبات نمی‌کند |
| in-cluster | `scripts/validate_xfoil_worker_networkpolicy.sh` و fixtureها | allowlisted caller موفق است؛ blocked caller به worker وصل نمی‌شود؛ readiness و DNS egress کار می‌کنند | نیازمند staging cluster و CNI enforcing است |
| smoke / CI image | workflow worker | image و API در container ساخته‌شده رفتار پایه قابل‌اجرا دارند | جایگزین test policy واقعی در cluster نیست |

## رفتار endpointها

`/healthz` فقط وضعیت سطح بالای process را بازمی‌گرداند و برای liveness مناسب است. `/readyz` در نبود API key معتبرِ پیکربندی‌شده یا نبود executable XFOIL با HTTP 503 پاسخ می‌دهد؛ پس readiness Kubernetes اجازه نمی‌دهد Pod معیوب traffic بگیرد. در Deployment، `startupProbe` و `livenessProbe` از `/healthz` و `readinessProbe` از `/readyz` استفاده می‌کنند. Kubernetes برای همین جداسازی lifecycle، liveness و readiness probe را ارائه می‌کند. [2]

## اجرای تست واقعی در staging

ابتدا secret runtime، image digest و worker را با `kubectl apply -k k8s/xfoil-worker` در خوشه staging آماده کنید. سپس اجرا کنید:

```bash
scripts/validate_xfoil_worker_networkpolicy.sh \
  --worker-namespace naca-xfoil \
  --test-namespace naca-xfoil-network-test
```

runner در یک namespace موقت دو Pod می‌سازد. Pod اول هم namespace label و هم Pod label `naca-airfoil-kit/xfoil-client=true` دارد؛ Pod دوم در همان namespace قرار دارد اما Pod label را ندارد. این تمایز بررسی می‌کند که policy صرفاً بر اساس namespace وسیع باز نشده است.

| گام | انتظار موفقیت | fail condition |
|---:|---|---|
| 1 | Deployment available و `/readyz` از caller مجاز، HTTP 200 | worker misconfigured، executable مفقود یا secret نادرست |
| 2 | lookup `kubernetes.default.svc.cluster.local` از worker | DNS egress policy، CNI یا DNS نامناسب |
| 3 | پنج درخواست health پیاپی از caller مجاز، همگی HTTP 200 | اختلال service routing، DNS یا شبکه درون‌خوشه‌ای |
| 4 | caller بدون Pod label در max 8 ثانیه نتواند به `/healthz` وصل شود | NetworkPolicy enforce نشده یا selector بیش‌ازحد باز است |
| 5 | namespace test به‌طور پیش‌فرض حذف شود | نیاز عملیاتی به diagnosis؛ `--keep-fixtures` برای نگه‌داری موقت |

> این runner هیچ port عمومی باز نمی‌کند، هیچ secret چاپ نمی‌کند و برای تست failure شبکه از privilege، `NET_ADMIN` یا chaos injection استفاده نمی‌کند؛ چنین ابزارهایی با Restricted Pod Security baseline و هدف least-privilege worker ناسازگارند.

## معنای «پایداری شبکه» در این نسخه

پنج درخواست متوالی برای تشخیص failureهای کوتاه DNS/service-routing و readiness اجرا می‌شود؛ این یک **smoke-resilience check** است، نه benchmark latency، load test یا آزمایش قطع شبکه. برای SLO واقعی، باید در staging با gateway واقعی، چند replica، metrics و fault-injection کنترل‌شده توسط platform team، آزمون‌های latency، connection exhaustion، DNS failure و rollout disruption جداگانه اجرا شوند.

## چک‌لیست قبل از فعال‌سازی production

| اولویت | کنترل | مالک |
|---:|---|---|
| P0 | اجرای runner در staging با CNI enforcing و ذخیره log نتیجه | Platform / QA |
| P0 | pin کردن image به digest، secret manager و rotation | Platform / Security |
| P0 | TLS/mTLS یا JWT، rate limit connection-level و identity در gateway | Platform |
| P1 | alert برای 401/429/503، timeout و NetworkPolicy denial | SRE |
| P1 | scan CVE و admission policy blocking | DevSecOps |
| P2 | load/chaos test کنترل‌شده و SLO latency با چند replica | SRE / QA |

## منابع

[1]: https://kubernetes.io/docs/concepts/services-networking/network-policies/ "Kubernetes Network Policies"
[2]: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ "Kubernetes Liveness, Readiness and Startup Probes"
