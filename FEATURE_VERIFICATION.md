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
