# Kubernetes: XFOIL Worker محدودشده

این manifestها worker را به‌صورت **داخلی** در namespace `naca-xfoil` اجرا می‌کنند. هیچ Ingress یا LoadBalancer در این پوشه وجود ندارد. worker باید فقط از یک gateway یا service داخلی دارای TLS، authentication و rate limit صدا زده شود.

## پیش‌نیازها

خوشه باید Kubernetes Pod Security Admission و یک CNI دارای NetworkPolicy enforcement داشته باشد. NetworkPolicy فقط زمانی ترافیک را محدود می‌کند که CNI آن را اعمال کند. [1] پیش از production، image tag در `deployment.yaml` را با digest تأییدشدهٔ GHCR جایگزین کنید؛ tag شناور `main` فقط برای staging است.

namespace با profile `restricted` برچسب‌گذاری شده است. این profile نیازمند non-root، `allowPrivilegeEscalation: false`، seccomp صریح و capability drop است. [2]

## ایجاد secret در runtime

Secret نمونه را commit یا apply نکنید. با secret manager سازمانی یا این دستور secret واقعی را بسازید:

```bash
kubectl create namespace naca-xfoil
kubectl -n naca-xfoil create secret generic xfoil-worker-api-key \
  --from-literal=api-key="$(openssl rand -base64 48)"
```

سپس manifestها را apply کنید:

```bash
kubectl apply -k k8s/xfoil-worker
kubectl -n naca-xfoil rollout status deployment/xfoil-worker
kubectl -n naca-xfoil get pods,service,networkpolicy
```

## hardening موجود

| کنترل | پیاده‌سازی |
|---|---|
| سطح دسترسی Pod | ServiceAccount بدون token و بدون RBAC؛ non-root UID/GID 10001 |
| process isolation | `readOnlyRootFilesystem`، `allowPrivilegeEscalation: false`، `capabilities.drop: [ALL]` و `RuntimeDefault` seccomp |
| فایل و secret | secret mount فقط‌خواندنی، tmpfs `emptyDir` با سقف 64MiB و عدم استفاده از hostPath |
| استفاده از منابع | request/limit برای CPU، memory و ephemeral storage |
| سلامت | startup/liveness با `/healthz` و readiness با `/readyz` |
| شبکه | Service از نوع ClusterIP؛ ingress فقط از namespace و pod دارای label client؛ egress فقط DNS |

Kubernetes برای request و limit منابع از scheduler و cgroup/runtime استفاده می‌کند؛ memory-backed `emptyDir` نیز باید size limit داشته باشد، زیرا مصرف آن بخشی از حافظه Pod است. [3]

## آماده‌سازی client مجاز

فقط namespace و Podهایی که هر دو label زیر را دارند می‌توانند به TCP/8080 worker وصل شوند:

```bash
kubectl label namespace YOUR_CLIENT_NAMESPACE naca-airfoil-kit/xfoil-client=true
kubectl -n YOUR_CLIENT_NAMESPACE label deployment/YOUR_GATEWAY naca-airfoil-kit/xfoil-client=true
```

پیش از rollout، enforcement واقعی CNI و رفتار health probe را در staging بررسی کنید. اگر CNI ترافیک probe از node را block کند، فقط node CIDR و فقط port 8080 را با policy platform-specific اضافه کنید؛ آن allowlist را بدون مشاهده رفتار CNI به‌صورت گسترده باز نکنید.

## کنترل عملیاتی باقی‌مانده

این manifestها جایگزین gateway، mTLS/JWT، WAF، scan CVE، secret rotation یا SIEM نیستند. checklist کامل در [`../../SECURITY_AUDIT_XFOIL_WORKER.md`](../../SECURITY_AUDIT_XFOIL_WORKER.md) قرار دارد. `readinessProbe` فقط وقتی HTTP 200 می‌گیرد که API key پیکربندی و executable XFOIL موجود باشد؛ Kubernetes برای لiveness/readiness/startup probes ابزار استاندارد ارائه می‌کند. [4]

## منابع

[1]: https://kubernetes.io/docs/concepts/services-networking/network-policies/ "Kubernetes Network Policies"
[2]: https://kubernetes.io/docs/concepts/security/pod-security-standards/ "Kubernetes Pod Security Standards"
[3]: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ "Kubernetes Resource Management"
[4]: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ "Kubernetes Probes"
