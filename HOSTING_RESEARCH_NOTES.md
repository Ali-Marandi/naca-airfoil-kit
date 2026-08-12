# Hosting research notes — 12 August 2026

## Streamlit Community Cloud

Official Streamlit documentation states that a Community Cloud account can connect to GitHub, deploy from repository files, and automatically update deployed applications after file changes. Public repositories are available after the initial GitHub connection; deployment requires repository admin permission. The documented flow is: workspace → Create app → confirm that an app exists → enter repository, branch, and entrypoint file → optionally choose subdomain and advanced Python/secrets settings → Deploy. Sources: <https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account> and <https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy>.

## Hugging Face Spaces

The current Spaces overview says that the currently offered SDKs are Gradio, Docker, and static HTML. It also states that static Spaces are free, while Gradio and Docker Spaces require a paid plan for creation, with the documented ZeroGPU exception limited to qualifying free personal accounts and Gradio. Therefore, Hugging Face is a technical fallback for this Python Streamlit application, but not a verified no-card fallback. A legacy Streamlit-specific page remains available and describes a Streamlit SDK with port 8501, but it conflicts with the current overview and should not be relied upon for a new no-card deployment. Sources: <https://huggingface.co/docs/hub/en/spaces-overview> and <https://huggingface.co/docs/hub/en/spaces-sdks-streamlit>.

## Commercial feature direction

QBlade documents alpha-range polar generation, Reynolds-number batch analysis, operating-point visualization, and polar export. XFOIL documents drag polar calculation, multiple stored polars, geometry modifications, inverse design, and airfoil blending. These capabilities support prioritizing polar sweeps, batch candidate screening, exportable design studies, and geometry quality metrics. Sources: <https://docs.qblade.org/src/user/airfoil/airfoil_analysis.html> and <https://web.mit.edu/aeroutil_v1.0/xfoil_doc.txt>.
