# ☁ Cloud Sync & Sharing Guide

The Ultimate Enterprise Edition (v2.9.0) introduces seamless cloud integration for professional collaboration.

## 1. Saving to Cloud
When you complete an airfoil analysis, click the **Save to Cloud** button in the sidebar.
- **What is saved?**: Your NACA code/UIUC profile name, all analysis parameters (Alpha, Re, Roughness), and the computed results (Cl, Cd, Cp).
- **Security**: Data is encrypted and stored in our secure enterprise database.

## 2. Sharing Projects
Click the **Share Project** button to generate a unique collaboration link.
- **Link Format**: `https://manus.im/share/airfoil/[PROJECT_NAME]`
- **Usage**: The link is automatically copied to your clipboard. Anyone with the link can view your geometry and analysis results in their own instance of the software or the Web UI.

## 3. Collaborative Workflow
1. Designer creates an optimized airfoil and saves to cloud.
2. Designer shares the link with the manufacturing team.
3. Manufacturing team opens the link, reviews the STL export, and proceeds to 3D printing.

---
*Note: In the current version, cloud saving is simulated for demonstration. Full API integration requires an Enterprise API Key.*
