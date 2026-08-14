# بازبینی hardening Kubernetes برای XFOIL Worker

**دامنه:** `k8s/xfoil-worker/` و ارتباط آن با `xfoil_worker_app.py`، image GHCR و checklist امنیتی موجود.  
**نتیجه:** manifestها یک baseline **Restricted، internal-only و least-privilege** برای staging/production فراهم می‌کنند، اما بدون CNI enforcing، secret manager، image digest و gateway دارای TLS/authentication نباید به‌تنهایی اینترنت‌پذیر شوند.

## اجزای manifest

| فایل | نقش | ارزیابی |
|---|---|---|
| `namespace.yaml` | namespace `naca-xfoil` با Pod Security Admission در سطح `restricted` | مناسب؛ profile سخت‌گیرانه فعال است |
| `serviceaccount.yaml` | ServiceAccount بدون token خودکار | مناسب؛ worker به API Kubernetes نیاز ندارد |
| `deployment.yaml` | Pod، context امنیتی، secret mount، resource limit و probeها | مناسب برای یک worker تک‌پردازشی |
| `service.yaml` | ClusterIP داخلی روی TCP/8080 | مناسب؛ بدون LoadBalancer یا Ingress عمومی |
| `networkpolicy.yaml` | allowlist ingress client و egress DNS | مناسب مشروط به CNI enforcing |
| `secret.example.yaml` | template آموزشی بدون secret واقعی | نباید apply یا commit با secret واقعی شود |
| `kustomization.yaml` | اعمال همه اجزا به‌جز secret مثال | مناسب |

## کنترل‌های runtime

| کنترل | محل پیاده‌سازی | دلیل |
|---|---|---|
| non-root UID/GID 10001 | `podSecurityContext` و image | مانع اجرای solver به‌عنوان root می‌شود |
| privilege escalation ممنوع | `allowPrivilegeEscalation: false` | جلوگیری از افزایش privilege داخل container |
| حذف capability | `capabilities.drop: [ALL]` | حداقل‌سازی سطح اختیار process |
| seccomp | `RuntimeDefault` | محدودسازی syscall مطابق profile استاندارد runtime |
| root filesystem فقط‌خواندنی | `readOnlyRootFilesystem: true` | محدودکردن persistence و تغییر image filesystem |
| محل نوشتن موقت محدود | `emptyDir` حافظه‌ای، 64MiB، در `/tmp` | نیاز XFOIL را با size limit مهار می‌کند |
| secret file read-only | mount در `/run/secrets/xfoil-worker` | جلوگیری از secret در image/env source و کاهش exposure |
| request/limit | CPU، memory و ephemeral storage | کاهش خطر exhaustion و scheduling قابل پیش‌بینی |
| startup/liveness/readiness | `/healthz` و `/readyz` | readiness فقط وقتی key و executable درست هستند، traffic می‌پذیرد |

Restricted Pod Security Standard بر non-root، privilege escalation ممنوع، seccomp صریح و capability drop تأکید دارد؛ manifest این شرایط را اعلان می‌کند. [1]

## boundary شبکه

Service از نوع `ClusterIP` است و Ingress/LoadBalancer ندارد. NetworkPolicy فقط TCP/8080 را از namespace و Pod دارای label `naca-airfoil-kit/xfoil-client=true` قبول می‌کند و egress را به DNS kube-system محدود می‌کند. Kubernetes تصریح می‌کند که NetworkPolicy به plugin شبکه‌ای نیاز دارد که enforcement آن را پشتیبانی کند. [2]

> label client باید فقط به gateway یا backend trusted داده شود، نه به همه workloadها. پیش از rollout باید health probe و Node-to-Pod traffic در CNI واقعی staging آزموده شود. اگر node CIDR نیاز به allow داشته باشد، فقط آن CIDR و فقط TCP/8080 را اضافه کنید.

## کنترل‌های حل‌نشده یا وابسته به platform

| اولویت | کنترل | وضعیت |
|---:|---|---|
| P0 | image GHCR با SHA-256 digest به‌جای tag `main` | در manifest کامنت شده؛ قبل apply جایگزین شود |
| P0 | TLS و mTLS/JWT در gateway | خارج از worker؛ لازم قبل از exposure |
| P0 | secret manager و rotation | secret نمونه تنها template است |
| P0 | CNI با NetworkPolicy enforcement | باید توسط platform owner تأیید شود |
| P1 | CVE/secret scan blocking و policy admission | در CI/cluster باید فعال گردد |
| P1 | log redaction، metrics و alert | در gateway/SIEM باید تکمیل شود |
| P1 | profile AppArmor/SELinux یا runtime class sandbox | platform-specific؛ ارزیابی شود |
| P2 | PDB/HPA/queue external برای scale-out | پس از تعریف SLO و workload واقعی |

## عملیات پیشنهادی

اول secret runtime را از secret manager یا `kubectl create secret generic` بسازید، سپس digest image تأییدشده را جایگزین کنید و `kubectl apply -k k8s/xfoil-worker` را در staging اجرا کنید. بعد از `rollout status`، اتصال از یک Pod دارای label مجاز، responseهای 401/429/503، readiness و timeout XFOIL را تست کنید. برای production، ingress و gateway باید TLS، identity، rate limit سراسری و audit correlation ID را به worker اضافه کنند.

Kubernetes از request برای scheduling و limit برای enforcement resource استفاده می‌کند؛ emptyDir حافظه‌ای نیز باید size limit داشته باشد تا به مصرف بی‌کران حافظه منجر نشود. [3] Liveness، readiness و startup probeها برای چرخه سلامت Pod تعریف شده‌اند، اما readiness به‌تنهایی جایگزین SLO/monitoring نیست. [4]

## منابع

[1]: https://kubernetes.io/docs/concepts/security/pod-security-standards/ "Kubernetes Pod Security Standards"
[2]: https://kubernetes.io/docs/concepts/services-networking/network-policies/ "Kubernetes Network Policies"
[3]: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ "Kubernetes Resource Management"
[4]: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ "Kubernetes Probes"
