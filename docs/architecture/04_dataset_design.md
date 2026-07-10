# Dataset Design 

**Status:** Accepted

**Date:** 2026-07-09

--- 

# 1. Overview

This document how time series data should be represented inside the Time Series Forecasting Lab.

The goal is to create one standard dataset structure that can support:

- univariate forecasting 
- multivariate forecasting 
- local models
- global models
- statistical models
- machine learning models
- deep learning models
- transformer models
- foundation models

The central idea is:

> Standardize the data format early so the models, features, backtesting, and pipelines can all depend on the same structure. 


---

# 2. Why Dataset Design Matters?

Forecasting models often expect different input formats.

For example:
- ARIMA usually needs a single ordered target series
- Prophet expects column names `ds` and `y`.
- XGBoost needs lag and rolling features.
- TFT needs historical targets, knows future covariates, static covariates, encoder windows, and decoder windows.
- Foundation models may need context windows.

Without a common dataset abstraction, every model will need custom data handling. 

That creates duplication and makes the framework harder to maintain.

---

# 3. Standard Forecasting Table

The core internal format should be:

| Column | Meaning |
|---|---|
| `unique_id` | Identifier of the Time Series |
| `ds` | Timestamp column |
| `y` | Target value |
| covariates | Optional additional variables |

Example:

| unique_id | ds | y | price | promo | holiday |
|---|---|---:|---:|---:|---:|
| store_001 | 2026-01-01 | 120 | 10.5 | 0 | 1 |
| store_001 | 2026-01-02 | 135 | 10.5 | 1 | 0 |
| store_002 | 2026-01-01 | 88 | 8.0 | 0 | 1 |

This format is inspired by common forecasting libraries and is simple enough to support both beginner and advanced models. 

Example:

| unique_id | ds | y | price | promo | holiday |
|---|---|---:|---:|---:|---:|
| store_001 | 2026-01-01 | 120 | 10.5 | 0 | 1 |
| store_001 | 2026-01-02 | 135 | 10.5 | 1 | 0 |
| store_002 | 2026-01-01 | 88 | 8.0 | 0 | 1 |

This format is inspired by common forecasting libraries and is simple enough to support both beginner and advanced models.

--- 

# 4. Required Columns 

Every forecasting dataset should contain:
```text
unique_id
ds
y
```

--- 

# 5. Optional Columns

Optional columns may include:
```text
price
promotion
holiday
temperature
inventory
marketing_spend
event_flag
```

These are covariates.

They may be used by:

- machine learning models
- deep learning models
- transformer models
- causal feature analysis
- scenario forecasting 


--- 



