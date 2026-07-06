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