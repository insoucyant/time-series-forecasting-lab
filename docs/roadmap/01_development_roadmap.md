# Development Roadmap

**Project:** Time Series Forecasting Lab
**Document:** `docs/roadmap/01_development_roadmpa.md`
**Status:** Working roadmap
**Last Reviewed:** 2026-10-18
**Scope:** Incremental development from forecasting foundations to forecast and decision intelligence

---


## 01. Purpose

The roadmap defines **what to build, in what order, and how to know when each milestone is complete**. It translates the project's vision into an incremental implementation plan without changing the agreed repository structure.

The platform's longterm progression is:

**Data → Understanding → Forecasting → Forecast Intelligence → Decision Intelligence → Business Value**

A forecast is not the end product; it is an input to better decisions.

This roadmap is a planning document, not a statement that all listed capabilities already exist. Completion dates are deiberately provisional. Technical designs and interface contracts remain authoratative in `docs/architecture/`; coding and quality requirements remain authoratative in `docs/engineering/01_engineering_standards.md`.

---

## 02. Guiding principles

1. **Architectural stability:** keep the existing repository structure and contracts unless a documented technical requirements justifies a change. 

2. **Vertical progress:** Prefer a working data-to-forecast-to-evaluation path over many disconnected modules. 

3. **One component at a time:** Implement, test, document, and integrate each component before expanding scope.

4. **Scientific validity:** Prevent tempora leakage; make benchmarks and experiments reproducible.

5. **Extensible but minimal:** Support future model families through stable interfaces, not speculative infrastructure. 

6. **Decision orientation:** Evaluate forecast quality first, then downstream utility where decision workflows exist.

7. **Honest status:** Distinguish implemented, designed, planned, and experimental features. 



---

## 03. Scope and Boundaries

The roadmap spans four layers:

| Layer | Objective | Representative Capabilities |
|---|---|---|
| Platform Foundation | Reliable data, configuration, interfaces, and engineering practices | Dataset contracts, configuration, testing, pipelines |
| Forecast engine | Generate and compare forecast | Statsitical, ML, DL, and foundation models |
| Forecast intelligence | Improve interpretation and use of forecasts | Uncertainity, hierarchy, reconciliation, scenarios, explainability |
| Decision Intelligence | Translate forecast into decisions | Optimization, resource allocation, inventory, pricing, energy, supply-chain use cases |

Advanced capabilities are long-term goals; their inclusion here does not authorize premature implementation of new folders.

---

## 04. Current Baseline

The following components have been implemented and exercised in the repository's initial test suite:

- YAML-based configuration loading and validation using the existing `config/` and `src/ts_forecasting_lab/config/` modules.
- `BaseForecaster` and `ForecastResult` contracts.
- `SeasonalNaiveForecaster`, including persistence behaviour.
- `ForecastDataset`, including single-series and multi-series valication, sorting, metadata, and copy isolation.
- Unit tests for the above components. The most recently reported full test run passed **67 tests with one warning**; this is a historical checkpoint, not a permanent quality claim.

Existing architecture documents through `docs/architecture/06_model_registry.md` and the documentation strategy establish design direction. A design document is not evidence that runtime capability has been implemented.

---

## 05. Milestone Overview

| Phase | Milestone | Primery deliverable | Exit evidence |
|---|---|---|---|
| 0 | Foundation baseline | Configuration, dataset, base forecaster, seasonal naive | Passing focused and repository tests | 
| 1 | End-to-end forecasting slice | Dataset → fit → predict → evaluate | Reproducible executable examples and tests |
| 2 | Evaluation and backtesting | Temporal splits, rolling evaluation, metric reports | Leakage-safe backtests and refernce checks |
| 3 | Statistical forecasting breadth | Additional classical baseline | Comparable results through one interface |
| 4 | Experiment and model lifecycle | Tracking, registration, artifact handling | Reproducible runs and loadabale artifacts |
| 5 | ML and DL forecasting | Feature-based and neural approaches | Consistent training and evaluation contracts |
| 6 | Forecast intelligence | Probabilistic and hierarchical capabilities | Validated uncertainty and reconciliation tests |
| 7 | Production-oriented v1.0 | Repeatable execution, CI/CD, packaging, observability | Release checklist and deployment rehearsal |
| 8 | Decision intelligence | Optimization and scenario-driven applications | Decision-quality benchmarks |
| 9 | Reseacrch and ecosystem maturity | Foundation models, plugins, educational benchmarks | Reproducible comparisons and contributor workflows | 


Phases may overlap selectively, but **dependencies and acceptance criteria** should determine sequencing rather than document numbering alone. 

---

## 06. Phase 0 - Foundation baseline

### Status

**Initial implementation complete; continued maintenance required.**

### Scope

- Project and environment configuration.
- Common forecaster interface and forecast-reult schema
- Seasonal naive forecasting baseline
- Dataset validation and data access
- Initial unit tests and engineering documentation

### Exit criteria

- [x] Configuration validation and tests exist.
- [x] Base forecaster and tests exist.
- [x] Seasonal naive implementation and tests exist.
- [x] Dataset implementation and tests exist.
- [x] Full test suite reported passing at the initial checkpoint.
- [ ] Investigate the outstanding warning and record whether action is required.

---

## 07. Phase 1 - First end-to-end forecasting workflow

### Objective

Demonstrate a complete, reproducible forecasting workflow using existing interfaces before expanding the model catalog. 

### Work items

1. Define the simplest supported workflow from a validated `ForecastDataset` to a trained forecaster.
2. Confirm forecast-horizon semantics and result alignment with actual timestamps.
3. Create a minimal evaluation path with one or two clearly defined error metrics. 
4. Run the workflow on a small, deterministic dataset.
5. Add integration tests that exercise multiple components together.
6. Document exact  commands and expected outputs.

### Exit criteria

- [ ] One command or example executes the workflow end to end.
- [ ] Forecasts have unambiguous timestamps, horizons, and series identifiers.
- [ ] No future observations are used to train a model for an earlier forecast origin.
- [ ] Repeated runs on deterministic inputs produce the expected results.
= [ ] Integration tests pass in the project environment.

---

## 08.



---

## 09.



---

## 10.



---

## 11.



---

## 12.



---

## 13.



---

## 14.



---

## 15.



---

## 16. Cross-cutting Engineering Requirements



---

## 17. Prioritization and Change Control



---

## 18. Milestone Tracking Template



---

## 19. Definition of Done



---

## 20. Near-term Execution Plan



---

## 21. Relationship to Existing Documents



---

## 22. Maintenance Rule



---

**Roadmap principle:** Build the smallest reliable forecasting capability, validate it rigorously, and extend it toward forecast intelligence and decision intelligence without sacrificing architectural consistency. 