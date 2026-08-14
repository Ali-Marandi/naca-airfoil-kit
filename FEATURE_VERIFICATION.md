## Web UI verification — 2026-08-12

Core tests passed after the commercial-workbench refactor. The public Streamlit endpoint initially continued to render a stale `ImportError` for `EngineeringStudy` even after the local Streamlit process was restarted. Direct Python import from `/home/ubuntu/naca-airfoil-kit/airfoil_pro.py` confirmed that `EngineeringStudy` exists in the current module. A cache-bypass session test is required before treating the web UI verification as complete.

A cache-bypass Streamlit session loaded successfully at 22:36 UTC. The web UI rendered the new tabs: Geometry, Pressure, Flow Field, Polar & Envelope, Design Study, and QA & Export. The default NACA 2412 operating point displayed Cl 0.1021, Cd 0.01120, L/D 9.12, and maximum thickness 12.00%.

The Polar & Envelope tab rendered successfully for NACA 2412 over alpha −6° to 14°. It displayed estimated best L/D 14.75 at 14°, maximum Cl 0.165, three polar plots, and a Polar CSV download control. The Design Study tab also opened successfully and showed the default candidate list and alpha controls.

The Design Study executed successfully for NACA 0012, 2412, 4412 and 6409 over alpha −4° to 12°. The UI displayed a ranking table, comparative L/D chart, and ranking CSV download. The displayed screening order was NACA 4412, 2412, 0012, then 6409. Results remain explicitly labelled as preliminary screening estimates.

The QA & Export tab rendered successfully for NACA 2412. It displayed maximum-thickness location 0.304 c, maximum camber 2.00% at 0.398 c, trailing-edge gap 0.253% c, normalized area ratio 0.08226, and two CSV download controls for QA metrics and normalized coordinates.

Final code quality check: `python3 -m py_compile airfoil_pro.py app.py`, `python3 -m unittest discover -p 'test*.py'`, and `git diff --check` all completed successfully. The test suite reported 8 passing tests.

## Validation, Robustness and Flap update — 2026-08-13

The core now includes a CSV experimental-polar parser, point-aligned model-versus-measurement residuals with Cl/Cd MAE, RMSE, bias and MAPE, a deterministic multi-condition Reynolds/roughness sensitivity envelope, and rigid hinged trailing-edge flap geometry for preliminary studies. The Streamlit interface exposes the capabilities through **Validation**, **Robustness** and **Flap Lab** tabs; the PyQt desktop interface exposes experimental CSV loading/residual summary and hinged-flap controls for the Windows build.

A local end-to-end Streamlit verification confirmed that the Validation tab accepted a CSV in the documented format, calculated all residual metrics, rendered the model-versus-measurement overlay, showed the residual table and enabled CSV download. A separate Robustness run over three Reynolds values and two roughness values produced the L/D envelope, a min/mean/max table and an engineering CSV download. The Flap Lab tab rendered its controls and scope warnings. The CSV used for the browser smoke test was internal test data only and was not presented as wind-tunnel data.

Final quality checks completed successfully: `python3 -m py_compile gui.py airfoil_pro.py app.py` and `python3 -m unittest discover -v`. The suite reported **12 passing tests**, including dedicated coverage for flap geometry, experimental CSV parsing, validation metrics and multi-condition envelopes.

## XFOIL adapter, Airfoil 360 comparison and audit trail — 2026-08-14

A new `xfoil_adapter.py` implements a **draft** XFOIL batch adapter with an allowlisted command generator, finite/sweep guardrails, `shell=False` process execution, bounded logs, time limits, polar parsing and a disposable per-run temporary directory. It does not bundle or execute an unverified XFOIL binary in this release. Five dedicated unit tests verify command injection resistance, unsafe-sweep rejection, standard polar parsing, missing-binary handling, `shell=False`, and cleanup of the temporary work directory.

`scripts/compare_naca0012_airfoil360.py` was executed against the CC BY 4.0 Airfoil 360 workbook for NACA 0012 at Re = 50,000 and 100,000 over alpha 0°–8.1°. It produced a PNG overlay, residual CSV and metrics JSON. The current preliminary model yielded Cl RMSE of 0.27392 and Cd RMSE of 0.02228 at Re = 50,000, and Cl RMSE of 0.28998 and Cd RMSE of 0.02942 at Re = 100,000. These results are evidence of the model limitation at low Reynolds number, not a calibration or an experimental validation claim.

The new **Study Audit Trail** creates a JSON manifest with schema version, UUID, UTC creation time, geometry SHA-256, geometry metrics, operating conditions, solver provenance and scope notice. The control was added to the Streamlit QA & Export tab and the PyQt6 desktop sidebar. A browser smoke check showed the `Download audit manifest JSON` control in QA & Export after a cache-bypass reload. Unit tests verified stable geometry hashing and JSON serialization.

Final checks completed successfully: `python3 -m py_compile airfoil_pro.py xfoil_adapter.py app.py gui.py scripts/compare_naca0012_airfoil360.py` and `python3 -m unittest discover -v`. The suite reported **19 passing tests**.

## Pareto Explorer and XFOIL worker production draft — 2026-08-14

The Streamlit application was restarted and loaded successfully with the new **Pareto Explorer** tab visible alongside the existing analysis workspaces. The feature surfaces a preliminary two-objective L/D–Cl map, marks non-dominated candidates, exposes a ranking table and supports CSV export. A subsequent interaction test is recorded with the full regression check.
بازبینی رابط نشان داد فرم Pareto Explorer با candidates پیش‌فرض و کنترل‌های alpha/objective بارگذاری می‌شود. اجرای study آغاز شد و کنترل تکمیلی پس از اتمام پردازش برای تأیید نمودار و CSV انجام می‌شود.
A local web smoke test then executed Pareto Explorer for NACA 0012, 2412, 4412 and 6409 over alpha −4° to 12° at the default preliminary operating condition. The interface rendered the L/D–Cl map, a ranking table, the Pareto-front count and the `Download Pareto ranking CSV` control. In this model-only screening run, NACA 4412 was the sole non-dominated candidate; this is a result of the selected objectives and envelope, not a universal design recommendation.

The XFOIL production draft adds `xfoil_worker_app.py`, `Dockerfile.xfoil-worker`, an optional restricted Compose service, and an Actions workflow that performs worker tests, constrained container smoke test, GHCR publication, SBOM and provenance. Local Docker was unavailable in the current environment, so the image was not built locally; static configuration tests verify non-root execution, internal-only Compose exposure, read-only runtime constraints, test-before-publish ordering and supply-chain metadata settings. GitHub Actions is the authoritative environment for the container build/smoke test.

## Pareto catalog integration and XFOIL worker hardening — 2026-08-14

`test_pareto_integration_catalog.py` successfully executed a 120-candidate deterministic NACA 4-digit matrix and verified complete ranking, polar completeness and the non-domination property for every reported Pareto-front member. The reusable `screen_geometries()` path also passed on a named geometry fixture catalog using the design-alpha Cl objective.

`scripts/run_pareto_uiuc_catalog.py` loaded 24 of 24 curated NACA coordinate profiles from the UIUC index at Re=1,000,000, k/c=0 and alpha −4° to 12°. It emitted CSV, chart and source manifest artifacts. In this preliminary model run, UIUC NACA6412 was the only reported front member; this is not a validated design recommendation.

The XFOIL worker now fails closed when authentication is absent, supports a mounted secret file, uses constant-time key comparison, applies request-body and per-credential quota controls, and returns no-store/nosniff headers. Compose adds explicit UID, secret mount, file/process/log constraints. The full quality suite passed 34 tests after these changes.
