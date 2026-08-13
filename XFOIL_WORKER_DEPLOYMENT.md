# استقرار production برای XFOIL Worker

**وضعیت:** Dockerfile، API worker و GitHub Actions در مخزن پیاده‌سازی شده‌اند. این سرویس هنوز به رابط Streamlit عمومی متصل نشده است؛ اتصال UI فقط پس از provision کردن endpoint داخلی، API key و کنترل دسترسی محیط production انجام می‌شود.

> Worker خروجی XFOIL را به‌عنوان یک **پیش‌بینی عددی viscous** برمی‌گرداند، نه داده آزمایشگاهی و نه نتیجه مناسب برای تصمیم ایمنی‌محور بدون validation مستقل.

## معماری

| جزء | مسئولیت | سطح دسترسی |
|---|---|---|
| Streamlit UI | جمع‌آوری پارامتر و نمایش نتایج | نباید command یا مسیر executable دریافت کند |
| XFOIL worker | اعتبارسنجی request، queue محدود و اجرای adapter | فقط شبکه داخلی یا ingress دارای authentication |
| `xfoil_adapter.py` | batch allowlisted، tempdir per-run، timeout و polar parser | هیچ فرمان آزاد کاربر را اجرا نمی‌کند |
| ingress/TLS | HTTPS و identity در محیط production | خارج از container worker |
| GHCR | نگهداری image دارای tag/SBOM/provenance | write فقط از CI main/tag |

## شروع محلی با Compose

یک فایل `.env` در ریشه پروژه ایجاد کنید و مقدار بلند و تصادفی برای `XFOIL_WORKER_API_KEY` قرار دهید. این فایل نباید commit شود.

```dotenv
XFOIL_WORKER_API_KEY=replace-with-a-long-random-secret
```

سپس worker اختیاری را همراه اپ اصلی فعال کنید:

```bash
docker compose --profile xfoil up --build
```

Compose worker را **بدون port عمومی** اجرا می‌کند. image با `read_only: true`، tmpfs محدود برای `/tmp`، `cap_drop: ALL`، `no-new-privileges`، سقف PID/CPU/memory و یک concurrency پیش‌فرض ساخته شده است. اگر به ingress مستقل نیاز باشد، فقط همان ingress باید به port 8080 داخلی وصل شود و باید API key را به شکل `X-API-Key` منتقل کند.

## API contract

| مسیر | روش | authentication | کاربرد |
|---|---|---|---|
| `/healthz` | `GET` | ندارد | وضعیت سرویس و وجود executable |
| `/v1/polar` | `POST` | `X-API-Key` در صورت تنظیم secret | polar محدودشده XFOIL |

بدنه `POST /v1/polar` فقط fields مشخص‌شدهٔ geometry، Re، Mach، Ncrit، transition، alpha range و iteration/timeout را می‌پذیرد. field اضافه رد می‌شود. geometry حداکثر 601 نقطه دارد و alpha/re/timeout با schema و adapter کنترل می‌شوند.

```json
{
  "airfoil_name": "NACA 0012",
  "coordinates": [[1.0, 0.0], [0.95, 0.01], [0.0, 0.0], [0.95, -0.01], [1.0, 0.0]],
  "reynolds": 1000000,
  "alpha_start": -4,
  "alpha_end": 12,
  "alpha_step": 1,
  "mach": 0,
  "ncrit": 9,
  "xtr_top": 1,
  "xtr_bottom": 1,
  "iteration_limit": 100,
  "timeout_seconds": 30
}
```

نمونه بالا تنها shape API را نمایش می‌دهد؛ برای اجرا باید contour معتبر با حداقل هشت نقطه ارسال شود.

## CI/CD

workflow `.github/workflows/xfoil-worker.yml` در pull request ابتدا unit testهای worker/adapter و سپس build + smoke-test container محدودشده را اجرا می‌کند. فقط پس از موفقیت آن‌ها، push به `main` یا tag `v*` image را در GitHub Container Registry با tag branch/tag/SHA منتشر می‌کند. SBOM و provenance attestation نیز تولید می‌شوند. این workflow به `packages: write` محدود شده و برای registry از `GITHUB_TOKEN` کوتاه‌عمر استفاده می‌کند؛ secret runtime worker هرگز در CI قرار نمی‌گیرد. [1]

## حد استقرار و عملیات

XFOIL یک CLI/system package است؛ بنابراین برای worker باید محیطی با container runtime یا کنترل OS فراهم باشد. Streamlit Community Cloud برای خود UI مناسب است، اما worker solver باید در یک سرویس container داخلی و دارای TLS/authentication جدا اجرا شود. پیش از production، ownership GHCR package، policy retention، log redaction، rate limit ingress و مانیتور کردن `timed_out`/`process_error`ها باید توسط تیم پروژه تأیید شود.

## منابع

[1]: https://docs.docker.com/build/ci/github-actions/ "Docker Build GitHub Actions"
[2]: https://packages.debian.org/stable/science/xfoil "Debian XFOIL package"
[3]: https://fastapi.tiangolo.com/deployment/docker/ "FastAPI in Containers — Docker"
