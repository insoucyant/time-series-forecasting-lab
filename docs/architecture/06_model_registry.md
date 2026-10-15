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

## 4. Registry Concepts

| Concept | Meaning | Example or intended use |
|---|---|---|
| Model identifier | Stable name for a model implementation | `seasonal naive` |
| Model family | Broad methodology category | `statistical`, `ml`, `deep_learning`, `foundation`|
| Implementation reference | Import path or explicit factory reference | A Python forecaster class |
| Capability metadata | Declared support behaviors | Single/multiple series, probabilistic output |
| Default parameters | Optional validated initialization defaults | Seasonal period | 
| Model configuration | Parameters for one run or experiment | Forecast horizon and hyperparameters |
| Trained model artifact | Serailized fitted model | A file or object-store object |
| Artifact version | Immutable identity or a fitted artifact | Versioned URI and checksum |
| Lifecycle status | Operational state of a trained version | Candidate, approved, retired |

**Important distinction:** A *modeldefinition* identifies an implementattion; a *trained model version* identifies a particular fitted artifact. They must not be conflated. 

## 5. Architectural Position

The regsitry sits between model consumers and forecasting implementations.

```text
Configuration/Experiment/Pipeline/Serving
                      |
                      v
            
          Model Registry Contract
             |       |       |
             v       v       v
       Statistical/ML/Deep Learning/Foundation
             \       |       /
              \      |      /
               
              Base Forecaster
                      |
                      v
              
              Forecast Result
```

The diagram represnts the intended integration pattern, not a claim that all shown model families or consumers have been implemented.


