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

## 3.


---

## 4.


---

## 5.


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
 



