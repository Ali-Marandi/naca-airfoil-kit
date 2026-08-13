# یافته‌های استقرار XFOIL Worker

## بسته Solver

بسته رسمی Debian برای `xfoil` نسخه 6.99.dfsg+1-3 را منتشر می‌کند و آن را یک برنامه تحلیل/طراحی interactive برای airfoilهای زیرصوت معرفی می‌کند. قابلیت‌های فهرست‌شده شامل تحلیل viscous/inviscid، محاسبه drag polar با Reynolds/Mach متغیر، و تحلیل airfoil موجود است. Ubuntu 24.04 نیز source package xfoil 6.99.dfsg+1-3 را دارد. [1] [2]

**تصمیم طراحی:** worker image از یک base سازگار با apt package استفاده می‌کند، نصب `xfoil` را در build انجام می‌دهد و مسیر executable را ثابت روی `/usr/bin/xfoil` نگه می‌دارد. نسخه package در label image و endpoint health ثبت می‌شود. هیچ binary دانلودشده از source غیرقابل‌تأیید در build اجرا نمی‌شود.

## ساخت و انتشار Image

مستندات Docker توصیه می‌کند build/push image در GitHub Actions با official actions (Buildx، metadata، login و build-push) انجام شود و قابلیت‌هایی مانند provenance/SBOM attestation قابل استفاده‌اند. [3]

**تصمیم طراحی:** workflow در pull request صرفاً test و build می‌کند؛ push فقط در branch `main` و tag `v*` و فقط در صورت حضور مجوز registry انجام می‌شود. workflow از `GITHUB_TOKEN` با کمترین permission لازم استفاده می‌کند و image tag را از SHA/tag ایجاد می‌کند.

## محدودیت سرویس

worker یک FastAPI تک‌فرایندی با API key اختیاری، strict request size/schema، concurrency semaphore، timeout solver و tempdir per-run خواهد بود. HTTPS باید توسط ingress یا cloud provider خاتمه یابد؛ container کلید TLS یا user secret را نگهداری نمی‌کند. FastAPI برای container deployment، COPY ترتیبی requirements، exec-form command و یک process/container را توصیه می‌کند. [4]

## منابع

[1]: https://packages.debian.org/stable/science/xfoil "Debian xfoil package"
[2]: https://packages.ubuntu.com/source/noble/xfoil "Ubuntu Noble xfoil source package"
[3]: https://docs.docker.com/build/ci/github-actions/ "Docker Build GitHub Actions"
[4]: https://fastapi.tiangolo.com/deployment/docker/ "FastAPI in Containers — Docker"
