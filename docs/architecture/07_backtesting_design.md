# Backtesting Design

**Project:** Time Series Forecasting Lab  
**Document:** `docs/architecture/07_backtesting_design.md`  
**Status:** Architecture design — planned functionality  
**Scope:** Forecasting Engine, evaluation integration, and experiment reproducibility

---

## 1. Purpose

Backtesting estimates how a forecasting method would have performed when predictions were made using only information available at the historical forecast origins. It provides an auditable basis for model selection, comparison, and eventual decision-oriented evaluation.

This document defines the design and contracts of backtesting capability. **It does not claim that a backtesting engine is already implemented.**

---

## 2. Relationship to Existing Architecture

the backtesting design fits within the existing Forecasting Engine and works with the established project components:

- `ForecastDataset`: validated time-series data and metadata.
- `BaseForecaster`: common `fit` and `predict` interface for forecasting models.
- `ForecastResult`: the forecasting output contract, subject to the existing schema.
- `Configuration system: vaidated experiment settings and model parameters.
- Model registry design: model discovery and reproducible model identification.
- Evaluation framework (`08_evaluation_framework.md`): metrics, comparisons, and statistical analysis; designed separately.
- Pipeline architecture (`09_pipeline_architecture.md`): orchestration of the full workflow; designed separately.

The backtester should **orchestrate** data splits, model fitting, prediction, and result collection. It should not redefine model APIs, evaluation metrics, or dataset semantics. 

---

## 3. Design Principles

1. **Chronological integrity:** Training observations must precede the corresponding forecast origin.
2. **No look-ahead:** Inputs, transformations, and covariates must be available at prediction time.
3. **Reproducibility:** Identical data, settings, code, and seeds should produce equivqlent runs where the estimator is deterministic. 
4. **Model agnosticism:** Statistical, machien learning, deep learning, and future foundation models use the same *orchestration contract* where their capabilities permit. 
5. **Traceability:** Every forecast is associeated with a model, series, fold, origin, target timestamp, and horizon.
6. **Explicit failures:** Invalid splits, unsupported horizons, and model errors should be reported, not silently ignored.
7. **Incremental scope:** Begin with a reliable single-series workflow, then extend to panel and advanced forecast types. 


---

## 4. Core Terminology

| Term | Meaning |
|---|---|
| *Forecast origin (cutoff)* | last timestamp whose observed target is available to the model |
| *Horizon* (`h`) | Number of periods ahead of the forecast origin |
| *Initial training window* | Historical observations available for the first fit |
| *step/stride* | Number of periods between consecutive forecast origin |
| *Expanding window* | Training start is fixed; training end advances |
| *Sliding window* | Training start and end both advance; window length is fixed |
| *Fold* | One origin with its associated training and test oservations |
| *Gap* | Optional excluded periods between the training end and teh evaluated targets |
| *Refit* | Training a new model instance on each fold or at a configured interval |

All period counts must be interpreted against the dataset's declared frequency, not as arbitrary row offsets when timestamps are irregular. 

---

## 5. Backtesting Strategies

### 5.1 Expanding-window backtesting

The training window starts at the earliest permitted observation and grows as the forecast origin advances. 

```text
Time  ------------------------------------------------------------>
Fold 1: [ TRAIN             ] [ TEST ]
Fold 2: [ TRAIN                   ] [ TEST ]
Fold 3: [ TRAIN                         ] [ TEST ]
```

Suitable for models intended to learn from all available historical data.

### 5.2 Sliding-window backtesting

The training window has a fixed length and moves forward.

```text
Fold 1: [ TRAIN             ] [ TEST ]
Fold 2:       [ TRAIN             ] [ TEST ]
Fold 3:             [ TRAIN             ] [ TEST ]
```

Suitable when recent observations may be more representative than distant history.

## 5.3 Holdout evaluation

A single chronological train/test split can be used as a basic *smoke test* or baseline, but it does not provide the same robustness as multiple forecast origins. 

## 5.4 Future Strategies

Blocked or nested temporal validation, irregularly spaced series, panel-specific calendars, and event-driven evaluation may be introduced when justified. they are not prerequisites for the first implementation.

---

## 6. Fold Generation and Temporal Boundaries

For a serie with ordered timestamps, `t_1, ..., t_T`, define a forecast origin `o` nad horizons `h = 1, ..., H`.

For the standard no-gap case:

- Training observability satisfy `timestamp <= o`.
- Evaluated target timestamps are the next `H` valid periods after `o`. 
- A fold is eligible only if its minimum training size and full required evaluation horizon are available.
- The origin advances by the configured `step`. 

With an optional gap `g`, the evaluated horizons start after the gap. The design must explicitly record whether reported horizons are measured from the origin or form the first evaluated timestamp; **the recommended convention is to measure horizons from the origin**.

Partial final folds should be disallowed by default and supported only through an explicit option with clear output metadata. 


---

## 7. Proposed Backtest Congfiguration Contract

The following is a **conceptual confguration schema**, not an assertion that these keys already exist in `config/config.yaml` or its Pydantic models. 

| Field | Type | Meaning |
|---|---|
| `startegy` | enum | `expanding` or `sliding` |
| `initial_train_size` | positive integer | Minimum obervations in the first training fold |
| `window_size` | positive integer / optional | Required for sliding-window mode |
| `horizon` | positive integer | Maximum forecast horizon |
| `step` | positive integer | Origin advance in periods |
| `gap` | nonnegative integer | Excluded periods after training cutoff |
| `refit` | boolean | Whether the estimator is retained for each fold |
| `allow_partial_folds` | boolean | Whether incomplete final horizons are permitted; default `false` | 
| `random_seed` | integer/optional | Reproducibility control where applicable |

Example (illustrative only):

```yaml
backtesting:
    startegy: expanding
    initial_train_size: 48
    horizon: 6
    step: 1
    gap: 0
    refit: true
    allow_partial_golds: false
    random_seed: 42
```

The exact configuration fields must be reconciled with the existing configuration schema before implementation. Do not introduce an independent, conflicting configuration loader.

---

## 8. Backtesting Execution Flow

```mermaid
flowchartTD
    A[Validated ForecastDataset] --> B[Validated backtest configuration]
    B --> C[Generate Chronological Folds]
    C --> D[Create isolated model instance for fold]
    D --> E[Fit using training observations only]
    E --> F[Predict requested horizon]
    F --> G[Align predictions with actual timestamps]
    G --> H[Validate and collect fold results]
    H --> I{More folds?}
    I -- Yes --> D
    I -- No --> J[Backtest result dataset]
    J --> K[Evaluation framework]
```

The diagram is a proposed execution design; it is not a description of an already deployed pipeline. 

---

## 9. Integration with `ForecastDataset`

The backtester must consume the existing validated dataset interface rather than introducing a parallel dataset abstraction.

Requirements:

- Preserve the original input dataset without mutation
- Respect timestamp, target, frequency, and optional series identifier metadata.
- Slice folds by choronological boundaries and series identifiers.
- Preserve the exact timestamp-to-target association.
- Reject or explicitly handle missing periods in accordance with the dataset's validation rules.
- Avoid reusing information from held-out periods during transformations.

If a subset must be represented as a `ForecastDataset`, use its existing constructor and validated public interface. Do not add methods to `ForecastDataset` unless implementation reveals a concrete necessity.


---

## 10. Integration with `BaseForecaster`

The engine should use the established `fit` and `predict` methods and honor the exiting `ForecastResult` contract.

Model-specific behavior, including the meaning of `predict` arguments, must be checked against the current `BaseForecaster` implementation before coding. The backtesting design does **not** authorize silently changing that interface. 

Each fold should ordinarily receive an independent model instance to prevent fitted state leaking across folds. If `refit=false` is supported, its semantics must be defined and validated for each model type; otherwise reject the option rather than pretending it works. 

### 10.1 Model construction

A model factory or registry-backed constructor may be used when available. For the first implementation, a simple explicitly supplied constructor is sufficient if it preseves configuration and instance isolation.

### 10.2 Forecast alignment 

Predictions must be matched to evaluation timestamps using the declared frequency and forecast origin. Never assume that row order alone guarantees correct alignment.

---

## 11. Multi-Series Backtesting

The long-term backtester should support datasets containing multiple series identifiers.

Important design choices include:

- **Shared-origin mode:** All series use the same calendar cutoffs, with explicit eligibility rles for shorter histories.
- **Per-series-origin mode:** Each series has its own valid cutoffs.
- **Local models:** One fitted model per series and fold.
- **Global models:** One model trained on multiple series, subject to its supported interface.

The initial implementation may focus on a single series. Multi-series execution should be introduced after the single-series contract and results have been tested.

A global model must not train on future observations from one series while forecasting an earlier cutoff for another series unless the experiment design explicitly permits that information and documents its availability.

---

## 12. Backtesting Output Contract

A long-format, one-row-per-forecast-target result is recommended for interoperability with evaluation and experiment tracking.

| Field | Description |
|---|---|
| `run_id` | Identifier of the backtesting run |
| `model_id` | Stable model identifier |
| `series_id` | Series identifier, nullable for single-series data |
| `fold_id` | Fold identifier |
| `forecast_origin` | Historical cutoff at which the forecast was issued |
| `target_timestamp` | Timestamp being forecast |
| `horizon` | Periods ahead of forecast origin |
| `y_true` | Observed target |
| `y_pred` | Point forecast |
| `fit_status` | Fold fit outcome |
| `predict_status` | Fold prediction outcome | 


Additional optional metadata may include model version, configuration hash, data version, runtime, seed, and error code. Future probabilistic outputs may be represented in a separate, clearly specified extension rather than overloading `y_pred`. 

**Uniqueness invariant:** For a given run and model, the combination `(series_id, fold_id, forecast_origin, target_timestamp, horizon)` must identify at most one forecast record. 

---

## 13. Separation from Evaluation 

The backtesting engine produces out-of-sample forecasts and actuals. The evaluation framework consumes these records and computes metrics.

This separation enables:

- Reuse of one backtest for multiple series.
- Model comparisons on identical folds and horizons.
- Diagnostics by series, time period, and horizon.
- Statistical significance testing without retraining models unnecessarily.


Detailed metrics definitions belong to `08_evaluation_framework.md`, not in this document.


---

## 14. Data Leakage Prevention

The following must be enforced or explicitly validated:

1. **Temporal leakage:** No future target observations in the training fold.
2. **Feature leakage:** Lagged, rolling, and aggregated features are calculated only from information available at the origin.
3. **Transformation leakage:** Scalers, imputers, and encoders are fitted on training data only, then applied to evaluation data.
4. **Covariate leakage:** Future covariates are used only when genuinely known at forecast issuance time.  
5. **Selection leakage:** Hyperparameters tuning and model selection must not optimize directly against the final untouched test period. 
6. **Cross-series leakage:** For global models, time-based restrictions apply across all participating series.

The first implementation should prioritize strict target separation and fold isolation; feature-pipeline safeguards become mandatory as feature engineering in integrated.

---

## 15. Error Handling and Fold Policies

Distinguish configuration errors, data errors, model fit errors, prediction errors, and output alignment errors.

Recommended initial policy: **fail fast** on invalid configuration, invalid data, or violated temporal invariants. A future configurable `continue_on_fold_error` mode may record failures while continuing other folds, but must never misrepresent missing forecasts as successful predictions. 

When an error occurs, record sufficient context: run, model, series, fold, origin-stage, exception type, and message. Avoid logging raw sensitive dataset contents.

---

## 16. Reproducibility and Provenance

A reproducible backtest should record, where available:

- Source data identifier and version or content hash.
- Timestamp range, series selection, and frequency.
- Model identifier, parameters, and software version.
- Backtest strategy and complete configuration.
- Fold cutoffs and training/test ranges.
- Random seed and relevant libraray versions.
- Run timestamp and execution status.

Persisting these records is a later pipeline/experiment-tracking concern; the output contract should be designed to carry or refernce them.

---

## 17. Computational Efficiency

The initial design should favor correctness and traceability over premature optimization.

Potential later improvements.

- Cache immutable, validated fold definitions.
- Parallelize independent folds or series where safe.
- Reuse fitted state only when the model explicitly supports valid incremental training.
- Bound memory use for large panel datasets.
- Support checkpointing and restart for long-running backtests.

Parallelization must not compromise determinism, ordering, or model isolation.

---

## 18. Testing Startegy

### 18.1 Unit tests

- Expanding-window fold boundaries.
- Sliding-window fold boundaries.
- Step, gap, and horizon calculations.
- Too-short datasets and invalid settings.
- No overlap between training observations and evaluated future targets.
- Correct alignment of timestamps, horizons, predictions, and actuals.
- Input dataset immutability.
- Deterministic fold ordering and identifiers.

### 18.2 Integration tests

- Run backtesting using the existing `SeasonalNaiveForecaster` and `ForecastDataset`.
- Verify the engine uses the established `BaseForecaster` interface.
- Check fold isolation and model refitting behavior.
- Verify downstream compatibility with the evaluation result contract.

### 18.3 Golden tests

Construct small synthetic series for which every fold, prediction, and expected error can be calculated manually. Store expected values in tests and compare them with pipeline output. 

### 18.4 Property and edge-case tests

- No forecast origin is later than its target timestamp.
- Horizons remain positive and consistent with the declared frequency.
- Duplicate timestamps and missing periods follow dataset calidation policy.
- Multi-series histories with dufferent start/end dates are handle explicitly.
- Missing or invalid predictions are not silently accepted.

---

## 19. Acceptance Criteria for Initial Implementation

- [ ] Existing dataset and forecaster interfaces are reused without unnecessary changes.
- [ ] Expanding-window backtesting works for a valid single series.
- [ ] Sliding-window backtesting works for a valid single series.
- [ ] Fold generation has deterministic, documented behavior.
- [ ] Forecasts are aligned to the correct timestamps and horizons.
- [ ] No held-out target observations enter model fitting.
- [ ] Results contain model, fold, origin, horizon, actual, and prediction fields.
- [ ] Invalid configuration and model failures produce clear errors.
- [ ] Unit tests and a Seasonal Naive integration test pass.
- [ ] Golden test results match hand-calculated expectations.
- [ ] Existing repository tests continue to pass.
- [ ] Documentation describes teh actual implemented behavior.


---

## 20. Incremental Implementation Plan

| Stage | Deliverable | Exit condition |
|---|---|---|
| 1 | Backtest configuration validation and chronological fold generator | All fold-boundary unit tests pass |
| 2 | Single-series execution with `BaseForecaster` | Seasonal Naive integration test passes |
| 3 | Stnadardized result collection and validation | Golden outputs and alignment tests pass |
| 4 | Evaluation framework integration | Metrics consume backtest results without custom reshaping |
| 5 | Multi-series execution | Series-specific and shared-cutoff tests pass |
| 6 | Advanced features | Introduced only with documented need and tests |

The stages describe logical deliverables, **not new mandated folders or files**. Their implememntation locations must follow the existing repository structure. 


---

## 21.


---

## 22. Current Status and Next Action



--- 

**Maintenance rule:** Update this design when the backtesting contract changes. Do not modify the wider architecture merely to accommodate speculative extensions.
 



