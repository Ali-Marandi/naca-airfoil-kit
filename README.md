# NACA Airfoil Kit Pro

NACA Airfoil Kit Pro is an engineering application for the **preliminary generation, analysis, comparison and validation-oriented screening** of NACA and UIUC airfoil sections. It supplies a PyQt6 desktop application intended for Windows packaging and a Streamlit web interface for browser-based use.

> **Engineering scope.** The current aerodynamic engine combines a lightweight vortex-panel calculation with empirical drag and stall estimates. It is appropriate for education, concept screening and early design comparison. It is not a viscous CFD solver and must not be used alone for safety-critical, certification, structural-load or final production decisions.

## Commercial Feature Set

| Capability | Delivered behavior | Interface |
|---|---|---|
| NACA geometry generation | Generates NACA four- and five-digit sections with configurable point density | Desktop and web |
| UIUC profile library | Searches and loads indexed UIUC coordinate profiles | Desktop and web |
| Preliminary aerodynamic analysis | Computes estimated Cl, Cd, L/D, Cp distribution, streamlines, roughness response and empirical stall flags | Desktop and web |
| Polar and design workbench | Sweeps alpha, summarizes best L/D and Clmax, compares NACA candidates and exports engineering CSV files | Web |
| Geometry QA | Reports thickness, camber, trailing-edge gap and normalized-area checks | Web |
| Experimental validation | Imports experimental polar CSV files, compares at the measurement alpha values and reports residuals, MAE, RMSE and bias | Desktop and web |
| Multi-condition robustness | Sweeps selected Reynolds and roughness values and exports deterministic min/mean/max response envelopes | Web |
| Hinged-flap study | Applies a rigid trailing-edge flap geometry for preliminary comparative studies | Desktop and web |
| Reporting and export | Provides normalized coordinate, polar, QA and validation CSV exports; desktop reporting includes PDF workflow | Desktop and web |

## Start the Web Application

Create a virtual environment if desired, install the dependencies, then start Streamlit from the repository root.

```bash
pip install -r requirements.txt
streamlit run app.py
```

The web application presents the **Geometry**, **Pressure**, **Flow Field**, **Polar & Envelope**, **Design Study**, **QA & Export**, **Flap Lab**, **Validation** and **Robustness** workspaces. The free Streamlit Community Cloud deployment procedure is documented in [`HOSTING_DEPLOYMENT_PLAYBOOK.md`](HOSTING_DEPLOYMENT_PLAYBOOK.md), with an alternate no-card deployment overview in [`NO_CARD_DEPLOYMENT.md`](NO_CARD_DEPLOYMENT.md).

## Start the Desktop Application

```bash
pip install PyQt6 matplotlib numpy requests fpdf2
python gui.py
```

The desktop application supports geometry and flow visualization, its existing reference-data overlay, direct import of an experimental CSV for residual reporting, and the preliminary hinged-flap controls. The final EXE is built by the repository’s GitHub Actions workflow when a release version tag is pushed.

## Experimental Validation Workflow

The **Validation** workspace accepts a CSV with a header row containing `alpha_deg` (or `alpha`, `aoa`, or `angle_of_attack`) plus at least one of `cl` or `cd`. A minimal file is shown below.

```csv
alpha_deg,cl,cd
-2.0,0.031,0.0084
0.0,0.248,0.0072
2.0,0.463,0.0070
```

The software evaluates the model at the same alpha values and provides pointwise model-minus-experiment residuals. It reports Cl and Cd metrics separately, which avoids hiding drag errors behind lift agreement. A validation study should also record the exact geometry, chord, Reynolds number, Mach number, surface state or transition information, turbulence level, tunnel corrections, alpha convention and source identifier.

Use [`VALIDATION_GUIDE.md`](VALIDATION_GUIDE.md) for the full documented workflow, data-selection method, uncertainty boundaries and authoritative reference sources. The guide highlights NASA’s critical assessment of NACA 0012 datasets, a NASA NACA 2412 separation study and the openly licensed Airfoil 360 low-Re data. [1] [2] [3]

The **Robustness** workspace is a deterministic sensitivity study, not a statistical confidence interval. It maps how this model responds to the Reynolds and roughness conditions chosen by the user; it does not quantify wind-tunnel measurement uncertainty.

## Flap Study Scope

The flap controls rotate the geometry aft of a user-selected hinge. Positive deflection moves the trailing edge downward. This produces a convenient preliminary geometry comparison, but it does **not** model flap-gap flow, seals, structural deformation, hinge moments, transition behavior or separated viscous flap aerodynamics. Verify any flap decision with a suitable viscous solver and/or experiment.

## Development and Quality Checks

| Path | Purpose |
|---|---|
| `airfoil_pro.py` | Geometry, panel/empirical analysis, validation parser/metrics, robustness and flap transformations |
| `app.py` | Streamlit web interface |
| `gui.py` | PyQt6 desktop interface |
| `VALIDATION_GUIDE.md` | Repeatable wind-tunnel comparison protocol and reference sources |
| `COMMERCIAL_FEATURE_ROADMAP.md` | Product priorities and next-release rationale |
| `test_*.py` | Unit tests for geometry, solver, commercial workbench, validation and robustness |

Run the quality suite before creating a tag:

```bash
python -m py_compile gui.py airfoil_pro.py app.py
python -m unittest discover -v
git diff --check
```

## Windows EXE Build and Release

A version tag triggers the Windows packaging workflow.

```bash
git tag v3.1.0
git push origin v3.1.0
```

After the GitHub Actions job finishes successfully, review the generated release asset on the repository’s [Releases page](https://github.com/Ali-Marandi/naca-airfoil-kit/releases). The workflow must retain `contents: write` permission to attach artifacts to the release.

## Further Development

The next highest-priority commercial investment is an optional, traceable viscous-solver integration (for example, XFOIL/QFoil) with solver version logging, input/output retention and failure diagnostics. This should be followed by constraint-aware inverse design, multi-objective Pareto selection, wing/rotor integration, project collaboration and an auditable API. See [`COMMERCIAL_FEATURE_ROADMAP.md`](COMMERCIAL_FEATURE_ROADMAP.md) for the complete prioritization.

## References

[1]: https://ntrs.nasa.gov/citations/19880002254 "McCroskey, A Critical Assessment of Wind Tunnel Results for the NACA 0012 Airfoil"
[2]: https://ntrs.nasa.gov/citations/19950002355 "NASA CR-197497, Experimental Studies of Flow Separation of the NACA 2412 Airfoil at Low Speeds"
[3]: https://data.mendeley.com/datasets/dz4bv26ncd "Airfoil 360 v2022: Wind Tunnel Data"
