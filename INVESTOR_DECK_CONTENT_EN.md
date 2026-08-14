# Investor Deck Content — NACA Airfoil Kit Pro

**Audience:** Early-stage investors and design partners
**As of:** August 14, 2026
**Evidence rule:** Product capabilities and CI results are current facts. Market size, customer traction, willingness to pay, revenue, retention, and interview findings remain **unproven** until real customer evidence is supplied.

## Cover

**NACA Airfoil Kit Pro**
**From Geometry to Traceable Screening Decisions**
A disciplined path from early engineering workflow to evidence-ready studies

## Slide 1

### Concept-Stage Aero Decisions Are Still Fragmented

- At the concept stage, geometry, solvers, spreadsheets, charts, and reports frequently live in separate tools and files.
- Available alternatives range from free desktop utilities to professional CFD platforms, but their fidelity and workflow scope are not comparable. [1] [2] [3]
- The proposed opportunity is not “another calculation engine.” It is a reviewable study package for small design teams.

**Key message:** Discovery must validate the workflow and handoff pain—not generic interest in airfoil analysis.

## Slide 2

### A Screening Workspace That Produces Reviewable Evidence

- The web and desktop applications combine geometry generation/import, polar analysis, QA, validation residuals, robustness studies, and multi-Reynolds Pareto screening.
- Evidence readiness classifies results as screening-only, informational comparison, or metadata-complete review.
- The audit manifest records geometry, conditions, and solver provenance; the desktop PDF also displays scope and evidence status.

**Internal evidence:** The latest release passed 57 local tests and the Python 3.10–3.13 CI matrix. [4]

## Slide 3

### Multi-Condition Decisions, Not Single-Point L/D Selection

- Robust multi-Reynolds Pareto evaluates candidates across a defined set of operating conditions instead of ranking them at one Reynolds number.
- In a reproducible run over 24 UIUC profiles from Re=100k to 2.0M, NACA6412 was the only front member in the current model and candidate set. [5]
- Sensitivity envelopes and the validation workflow are designed to expose uncertainty and limitations rather than conceal them.

**Key message:** The method makes trade-offs and evidence gaps visible; it does not claim a final design recommendation.

## Slide 4

### A Guardrailed Path to Higher-Fidelity Solver Integration

- The XFOIL adapter uses an allowlisted protocol, temporary-directory isolation, timeouts, and shell-free execution.
- The FastAPI worker includes fail-closed authentication, request quotas, security headers, a non-root container, and CI supply-chain artifacts.
- Kubernetes manifests define an internal service, restricted runtime controls, and DNS-only NetworkPolicy. Production still requires an enforcing CNI, secret management, and image-digest pinning. [6]

**Key message:** The technical foundation for higher solver fidelity is in place; a production solver service remains a milestone, not a revenue claim.

## Slide 5

### Beachhead Hypothesis: UAS, Rotor Teams, and Consultants

- FAA aerospace forecasts cover UAS and Advanced Air Mobility across 2026–2046, while EASA reports more than 1.6 million registered drone operators under a harmonized European framework. [7] [8]
- These figures indicate a broad ecosystem; they do **not** establish direct TAM for this software.
- The initial ICP is teams that need a fast shortlist, handoff, and review before committing to CFD or experimental work.

**Key message:** This beachhead is a medium-confidence hypothesis that must be tested through structured discovery.

## Slide 6

### Pricing Is a Controlled Experiment, Not a Final Price List

| Offer | Bounded scope | Experimental fee |
|---|---|---:|
| Founding Design Partner | Up to 3 geometries, one review cycle, evidence package | $1,500 |
| Standard Evidence Pilot | Up to 5 geometries, robust study, two check-ins | $3,500 |
| Extended Workflow Pilot | Workflow mapping and handoff workshop | $5,000 |

- Each step in the price ladder includes a different scope and support level; no discount is granted without a measurable concession.
- DesignFOIL, AeroFoil, and AirShaper are used only as pricing-range context. They are not like-for-like products. [1] [2] [3]
- No paid conversion rate, ARR, or realized revenue has been recorded yet.

## Slide 7

### A Five-Partner Cohort Is the Fastest Route from Hypothesis to Evidence

- The proposed cohort includes two UAS/rotor teams, one aerodynamic consultant, one professional laboratory, and one reserve candidate to manage dropout risk.
- Each pilot runs for four weeks, uses a fixed scope, and includes no more than three synchronous sessions.
- Proposed gates are at least three paid commitments or LOIs, at least 70% activation, and at least three evidence packages used in a review context.

| Capacity scenario | Cohort composition | Illustrative gross pilot fees |
|---|---|---:|
| Minimum | 3 × Founding | $4,500 |
| Core | 2 × Founding + 2 × Standard | $10,000 |
| Full cohort | 2 × Founding + 2 × Standard + 1 × Extended | $15,000 |

**Note:** These are capacity scenarios, not forecasts or realized revenue. [9]

## Slide 8

### Discovery Status: The Plan Exists; Customer Evidence Must Be Collected

- The repository audit found no recorded transcript, CRM export, survey response, or completed discovery interview from the planned ten calls.
- Pain ranking, willingness to pay, churn risk, and conversion are therefore currently unknown.
- Discovery intake standards and stop/go gates are now prepared to turn real feedback into usable product evidence. [10]

**Key message:** Capital is not being requested for feature sprawl. It is being directed toward proving ICP, pricing, and repeatable use.

## Slide 9

### Investment Is Structured Around Stage-Gated Proof Points

| Stage | Proof point | Decision enabled |
|---|---|---|
| Discovery | 10 structured interviews and at least 7 complete records | Confirm or revise ICP |
| Pilot | 3–5 partners and at least 3 paid commitments or LOIs | Confirm value metric and price corridor |
| Product | At least 70% activation and 60% evidence-package use | Build private-study and team workflow |
| Scale | At least 50% repeat study use and referenceable outcomes | Prepare focused GTM |

- Larger financial or technical commitments follow only after the relevant proof point is met.
- This structure limits burn on enterprise integrations or low-demand features before customer evidence exists.

## Slide 10

### The Ask: Design Partners and Staged Validation Capital

- Introductions to 3–5 UAS/rotor teams or consultants with a real design decision in the next 90 days.
- Support for disciplined discovery execution, the pilot cohort, and measurement.
- Partnership in translating real evidence into a repeatable product roadmap and pricing model.

**Goal:** Build a reliable path from geometry to decision—first for preliminary screening, then, with sufficient evidence, for more professional team workflows.

## References

[1]: https://www.dreesecode.com/ "DreeseCODE — DesignFOIL"
[2]: https://aerofoilengineering.com/ "AeroFoil Engineering — AeroFoil"
[3]: https://airshaper.com/pricing "AirShaper — Pricing"
[4]: https://github.com/Ali-Marandi/naca-airfoil-kit/actions/runs/31762936115 "GitHub Actions — tests, commit 602730c"
[5]: ./PARETO_MULTI_RE_ANALYSIS.md "Robust multi-Re Pareto analysis"
[6]: ./SECURITY_AUDIT_XFOIL_WORKER.md "XFOIL Worker security audit"
[7]: https://www.faa.gov/data_research/aviation/aerospace_forecasts "FAA Aerospace Forecasts"
[8]: https://www.easa.europa.eu/en/domains/civil-drones "EASA — Drones & Air Mobility"
[9]: ./LIMITED_PILOT_EXECUTION_AND_PRICING_PLAN_FA.md "Limited Pilot Execution and Pricing Plan"
[10]: ./PROBLEM_DISCOVERY_EVIDENCE_AUDIT_FA.md "Problem-Discovery Evidence Audit"
