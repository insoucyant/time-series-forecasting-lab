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

A forecaster should **not** be responsible for everything.

The following responsibilities belong elsewhere:

| Responsibility | Owner |
|---|---|
| Reading raw data | Data layer |
| Cleaning data | Preprocessing layer |
| Feature Engineering | Feature Layer |
| Train/test splitting | Data splitting layer |
| Backtesting | Backtesting engine |
| Metric calculation | Evaluation layer |
| Plotting | Visualization layer |
| Experiment tracking | Tracking layer |
| API serving | Serving layer |

This separation keeps forecasting models focused and easy to test.

A forecaster should forecast.
It should not become a  pipeline, evaluator, plotter, or data cleaner. 

---

# 6. Core Interface

The first version of the base forecaster should define the following methods.

## `fit`

```python
fit(data, **kwargs)
```

Fits the model on historical data.

Expected behaviour:

- Accept training data.
- Learn model parameters.
- Store fitted state inside the object.
- Return the fitted model object.

Example:
```python
model = SeasonalNaiveForecaster(season_length=7)

model.fit(train_data)
``` 
---

## `predict`

```python
predict(horizon: int, **kwargs) -> ForecastResult
```

Generate forecasts for future periods.

Expected behaviour:

- Requires the model to be fitted first
- Produce forecasts for the requested horizon.
- Return a `ForecastResult`

Example:

```python
forecast = model.predict(horizon=30)
```

---

## `save`

```python
save(path)
```

Persists the trained model to disk.

Expected behaviour:

- Save the model state.
- Save enough metadata to reload the model safely.
-  Avoid mixing model serialization with evaluation or reporting

---

## `load`

```python
load(path)
```

Loads a trained model from disk.

Expected behaviour:

- Restore the model state.
- Restore model metadata.
- Return a usable forecaster object.


---

## `get_model_info`

```python
get_model_info() -> dict
```

Returns basic model metadata.

Examples metadata may include:

```python
{
    "model_name": "seasonal_naive",
    "model_type": "baseline",
    "supports_probabilistic_forecast": False,
    "supports_exogenous_variables": False,
}
```

---

# 7. ForeacastResult

A model should not return arbitrary outputs.

Every model should return a standard `ForecastResult`.

The purpose of `ForecastResult` is to decouple forecasting modesl from downstream consumers. 

The model returns:

```text
ForecastResult
```

The other components consume it:

```text
ForecastResult
    ├── Evaluation
    ├── Plotting
    ├── Reporting
    ├── Monitoring
    ├── API Response
```


---

# 8. What should ForecastResult contain?

A `ForecastResult` should contain:

| Field | Purpose |
| --- | --- \
| `predictions` | Forecasted values |
| `horizon` | Forecast horizon |
| `model_name` | Name of the model that generated the forecast |
| `frequency` | Time series frequency |
| `timestamps` | Forecast timestamps, if available |
| `series_id` | Time series identifier, if applicable |
| `prediction_intervals` | Optional lower/upper bounds |
| `quantiles` | Optional quantile forecasts |
| `metadata` | Additional information |

In simple cases, `ForecastResult` may only contain point forecasts.

In advanced cases, it may contain prediction intervals, quantiles, or multiple series.

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
