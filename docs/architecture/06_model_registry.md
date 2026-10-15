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

## 3. Responsibilities and Non-Responsibilities

### 3.1 Responsibilities

The registry should eventually:

1. Assign each supported forecasting implementation a stable, unique model identifier.
2. Map identifiers to importable implementations or explicitly registered factories. 
3. Validate registry entries and reject duplicates or invalid references.
4. Expose model metadata and supported capabilities.
5. Instantiate models using validated parameters.
6. Provide clear errors for unknown, disabled, or incompatible models.
7. Support reproducible records of the model implementation and configuration used in an experiment.
8. Support future references to trained model versions and stored artifacts.

### 3.2 Non-responsibilities

The registry should not:

- Perfrom model training or backtesting.
- Select the best model automatically.
- Calculate forecasting metrics.
- Own datasets or future pipelines.
- Replace the `BaseForecaster` contract.
- Store large trained-model binaries inside YAML configuration.
- Implicitly deploy or serve a model when it is registered.

These activities belong to their respective platform components.