# Forecaster Interface

**Status:** Accepted

**Date:** 2026-07-08

# 1. Overview

This document defines the core forecasting interface for the Time Series Forecasting Lab.

The goal is to ensure that every forecasting model in the repository follows a common contract, regardless of whether the model is:

- Naive
- Seasonal Naive
- ARIMA
- ETS
- Prophet
- XGboost
- LightGBM
- LSTM
- N-BEATS
- Temporal Fusion Transformer
- Chronos
- TimesFM
- Moirai

The central idea is:

> Every model should behave like a Forecaster.

---

# 2. Why do we need a Common Interface?

Without a common interface, each forecasting model tends to develop its own structure.

For example:

```python
arima_model.train(...)
arima_model.forecast(...)

xgboost_model.fit_model(...)
xgboost_model.predict_future(...)

tft_model.train_network(...)
tft_model.infer(...)
```

This creates several problems:

- Models become difficult to compare.
- Pipelines need model-specific logic.
- Evaluation code becomes duplicated.
- Backtesting becomes harder.
- New models are harder to add.
- Collaborators cannot easily understand the framework. 

A common interface solves this by making all models look the same from the outside.

---

# 3. What is a Forecaster?

A **Forecaster** is an object that learns from historical time series data and produces future forecasts.

In this framework, a forecaster should answer two basic questions:

1. How do I learn from historical data?
2. How do I generate forecasts for future periods?

The simplest interaction should look like:

```python
model.fit(train_data)

forecast = mode.predict(horizon=30)
```

This should remain true whether the model is ARIMA, XGBosst, LSTM, TFT, or a foundation model.

---

# 4. Responsibilities of a Forecaster

A forecaster is responsible for:

- Fitting or training on historical time series data.
- Producing future forecasts.
- Returning forecast in a standard format.
- Saving itself to disk.
- Loading itself from disk.
- Exposing basic model metadata.

Therefore, every forecaster should implement:

```python
fit(...)
predict(...)
save(...)
load(...)
get_model_info(...)
```

---

# 5. Responsibilities not owned by a Forecaster


---

# 6. Core Interface


---

# 7. ForeacastResult


---

# 8. What should ForecastResult contain?


---

# 9. Supporting different Forecasting Types


---

# 10. Optional Capabilities


---

# 11. Interface Stabilities


---

# 12. Design Principles



---

# 13. Example Usage


---

# 14. Implementation Plan




---

# 15. Summary 




---
