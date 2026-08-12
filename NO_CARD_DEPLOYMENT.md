# مسیر بدون کارت برای NACA Airfoil Kit Pro – نسخه وب

**راهکار توصیه‌شده: Streamlit Community Cloud**

برای اجرای عمومی نسخه Streamlit این پروژه بدون نیاز به کارت، از Streamlit Community Cloud استفاده کنید. این سرویس به مخزن GitHub متصل می‌شود، فایل `app.py` را اجرا می‌کند و از `requirements.txt` برای نصب وابستگی‌ها بهره می‌برد. مراحل دقیق در [راهنمای کامل استقرار](HOSTING_DEPLOYMENT_PLAYBOOK.md) آمده است.

| فیلد استقرار | مقدار |
|---|---|
| Repository | `Ali-Marandi/naca-airfoil-kit` |
| Branch | `main` |
| Main file path | `app.py` |
| URL پیشنهادی | `naca-airfoil-kit-pro` در صورت آزادبودن |

> برای deploy باید حساب GitHub شما به Community Cloud متصل باشد و روی مخزن مجوز **admin** داشته باشید. [1]

## وضعیت Hugging Face Spaces

Hugging Face Spaces به‌عنوان مسیر فنی پشتیبان بررسی شده است، اما طبق مستندات فعلی، ساخت Spaceهای محاسباتی Gradio و Docker به پلن پولی نیاز دارد؛ بنابراین آن را راهکار بدون‌کارت تأییدشده در نظر نگیرید. برای حساب‌هایی که دسترسی Docker Space دارند، راهنمای Docker-based deployment در `HOSTING_DEPLOYMENT_PLAYBOOK.md` آورده شده است. [2] [3]

## منابع

[1]: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy "Deploy your app on Community Cloud"
[2]: https://huggingface.co/docs/hub/en/spaces-overview "Hugging Face Spaces Overview"
[3]: https://huggingface.co/docs/hub/en/spaces-sdks-docker "Hugging Face Docker Spaces"
