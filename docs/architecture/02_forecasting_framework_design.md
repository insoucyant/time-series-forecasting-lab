# Forecasting Framework Design

**Status:** Accepted

**Date:** 2026-7-06

--- 

# 1. Overview:

The goal of this repository is to build a **production-quality forecasting framework** into which different forecasting models can plug seamlessly. The goal is **not** to implement a collection of independent forecasting models. 

The framework should support:

- Classical Statistical Forecasting
- Machine Learning Forecasting
- Deep Learning Forecasting
- Transformer-Based Forecasting
- Foundation Models
- Probabilistic Forecasting
- Local and Global Forecasting 
- Production Deployment 
- Experiment Tracking
- Monitoring 
- Explainability 

The guiding principle is:

> **Design the framework first. Plug models into it later.**

--- 

# 2.  Problem Statement 

Many forecasting repositories evolve into collections of unrelated scripts.

For example:

```
arima.py
prophet.py
lstm.py
tft.py
xgboost.py
```

Each script:

- accepts different inputs
- returns different outputs 
- has different APIs
- performs preprocessing differently 
- is difficult to compare
- is difficult to extend

Such repositories become difficult to maintain as more forecasting models are added. 
The objective of this repository is to avoid that problem by defining a common forecasting interface. 

---

# 3. Design Goals

The framework should satisfy the following goals:
## Consistency
Every forecasting model should expose the same interface.
## Extensibility
New forecasting models should be added with minimal changes.
## Maintainability 
Business Logic should be separated from infrastructure.
## Reusability 
Components should be reusable across projects.
## Testability 
Every component should be independently testable.
## Product Readiness

The framework should support deployment, monitoring and experiment tracking. 

---

# 4. What is a Forecaster?

A **Forecaster** is an object that learns patterns from historical time series data and produces forecasts for future time periods. 

Regardless of the underlying algorithm, every forecasting model should behave like a forecaster. 

Examples include:

- Seasonal Naive
- ARIMA
- ETS
- Prophet
- Random Forest
- XGBoost
- LightGBM
- CatBoost
- LSTM
- GRU
- N-Beats
- N-HiTS
- Temporal Fusion Transformer
- Chronos
- TimesFM
- Moirai

Although these models are mathematically different, the framework should interact with them uniformly. 

--- 

# 5. Required Interface

Every forecasting model should implement the following methods.

```python
fit(...)
```

Train or fit the forecasting model.

```python
predict(...)
```

Generate forecasts. 

Future versions may additionally support:

```python
save(...)
```

Persist a trained model.

```python
load(...)
```

Load a trained model.

Optional capabilities may include:

- predictions intervals
- quantile forecasts
- explainability 
- feature importance

These capabilities should not be mandatory for every forecasting model. 

---

# 6. ForecastResult

# 7. Data Flow

The forecasting pipeline should follow the architecture below:

```
Raw Data

↓

Data Validation

↓

Preprocessing

↓

Feature Engineering 

↓

Train / Validation / Test Split

↓

Forecaster.fit()

↓

Forecaster.predict()

↓

ForecastResult

↓

Evaluation

↓

Reporting 

↓

Visualization 

↓

Deployment 
```

Each should have a single responsibility. 

---

# 8. Supported Forecasting Paradigms