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

---

## 6.


---

## 7.


---

## 8.


---

## 9.


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

## 16.


---

## 17.


---

## 18.


---

## 19.


---

## 20.


---

## 21.


---

## 22. Current Status and Next Action



--- 

**Maintenance rule:** Update this design when the backtesting contract changes. Do not modify the wider architecture merely to accommodate speculative extensions.
 



