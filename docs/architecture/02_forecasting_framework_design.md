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

Forecast models should not return arbitrary objects.

Instead, every forecasting model should return a common ForecastResult object.

The ForecastResult object should contain:

- Forecast values
- Forecast horizon
- Forecast timestamps
- Model name
- Frequency
- Prediction intervals (optional)
- Additional metadata


This allows downstream components such as:

- evaluation
- plotting
- reporting 
- monitoring 

to consume forecast without depending on the underlying forecasting model.


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

The framework should support multiple forecasting paradigms without changing the external interface.

## Univariate Forecasting

Single target variable.

Example:

Electricity Demand.

---

## Multivariate Forecasting

Multiple related variables.

Example:

Demand, price, promotions, and holidays.

---

## Local Forecasting


One forecasting model per individual time series.

Example:

One ARIMA model per retail store.

---

## Global Forecasting 


A single forecasting model trained across many related time series.

Example:

One TFT trained on all retail stores. 

---

## Probabilistic Forecasting 

Forecasts represented as probability distributions or prediction intervals.

---

## Deep Learning Forecasting 

Examples include:

- LSTM
- GRU
- N-BEATS
- N-HiTS

---

## Transformer-based Forecasting

Examples include:

- Informer
- Autoformer
- PatchIST
- Temporal Fusion Transformer

---

## Foundation Models

Examples include:

- Chronos
- TimesFM
- Moirai

These models may have different internal architectures but should expose the same forecasting interface.
---


# 9. Dataset Representation 

To maximize compatibility across forecasting models, datasets should eventually be represented using a common tabular format.

Example:

| unique_id |  ds |  y  | covariates...|
|-----------|-----|-----|--------------|
| store_001 | ... | ... | ... |

where:

- unique_id identifies the time series
- ds represents the timestamp
- y represents the target variable

Additional columns may represent known covariates.

This format naturally supports:

- local forecasting
- global forecasting
- multivariate forecasting
- transformer models

--- 

# 10. Keeping the Interface Stable

The framework should distinguish between:

"Core Forecasting Behaviour" & "Advanced Forecasting Capabilities". 

The core interface should remain stable.

```
fit()

predict()
```

Advanced functionality should be added through optional extensions rather than modifying the base interface.

Examples include:

- Probabilistic Forecasting
- Explainability
- Feature Importance
- Serialization 

This design allows increasingly sophisticated forecasting models to integrate without breaking existing code. 

--- 

# 11. Architectural Principles

The framework follows the following software engineering principles:

## Single Responsibility Principle

Each component should perform one responsibility.

Examples:

- reader.py reads configuration.
- schema.py validates configuration.
- evaluation computes metrics.
- plotting generates figures.

## Open/Closed Principle

The framework should be open for extension but closed for modification.

Adding a new forecasting model should not require changing existing forecasting models.

---

## Dependency Inversion 

The forecasting pipeline should depend on the abstract forecasting interface rather than concrete forecasting implementations.

---

## Separation of Concerns

Data loading, forecasting, evaluation, visualization, and deployment should remain separate. 

---

# 12. Long-Term Vision

The rpository aims to evolve into a production-quality forecast framework supporting: 

- Statistical Forecasting
- Machine Learning
- Deep Learning 
- Foundation Models
- Model Comparison
- Backtesting 
- Hyperparameter Optimisation
- Experiment Tracking
- REST APIs
- Docker deployment 
- Monitoring 
- Drift detection 
- Explainability 

The objective is not merely to demonstrate forecasting algorithms but to demonstrate the software engineering required to build forecasting systems used in production.

--- 

# 13. Future Work

Future architecture documents will describe:

- Base Forecaster
- Model Registry 
- Feature Engineering Framework
- Dataset Abstraction
- Backtesting Engine
- Logging 
- Experiment Tracking 
- Deployment Architecture
- Monitoring Architecture

--- 

# 14. Summary 

The central design philosophy of this repository is:

> Build a reusable forecasting framework first.

> Add forecasting model as interchangeable components.

This allows the repository to scale from simple statistical forecasting models to the state-of-the-art foundation models without changing the overall architecture. 