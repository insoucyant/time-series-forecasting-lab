# Model Registry Design

**Project:** Time Series Forecasting Lab
**Document:** `docs/acrchitecture/06_model_registry.md`
**Status:** Architecture specification — implementation status noted below
**Scope:** Forecast model definitions, registration, discovery, versioning, and artifact metadata

---

## 1. Purpose

The model registry provides a consistent mechanism to identify, configure, instantiate, and eventually manage forecasting models across the Time Series Forecasting Lab.

It supports the platform's progression from statistical forecasting to machine learning, deep learning, and foundation-model approaches without requiring callers to depend on individual model implementation modules.

The registry is **not** itself a training pipeline, experiment tracker, model artifact store, or serving system. It supplies model identity and discovery contracts that those components may consume. 

## 2. Scope and Implementation Status

The repository already contains:

- `config/model_registry.yaml` - an existing registry configuration file.
- `src/ts_forecasting_lab/models/base.py` - the common forecaster interface, including `BaseForecaster` and `ForecastResult`.
- `src/ts_foreasting_lab/models/statistical/naive.py` - the seasonal naive forecaster.
- `src/ts_forecasting_lab/config/` - configuration loading and validation components.

The existing elements form the starting point. **A fully implemented runtime registry, persisitent registry service, artifact vision store, and lifecycle management workflow are not assumed to exist.**

This documents specifies the intended contract and incremenetal implementation plan. It does not change the existing repository layout or prescribe a new directory.

