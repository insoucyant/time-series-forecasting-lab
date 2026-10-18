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

---

## 2. Scope and Implementation Status

The repository already contains:

- `config/model_registry.yaml` - an existing registry configuration file.
- `src/ts_forecasting_lab/models/base.py` - the common forecaster interface, including `BaseForecaster` and `ForecastResult`.
- `src/ts_foreasting_lab/models/statistical/naive.py` - the seasonal naive forecaster.
- `src/ts_forecasting_lab/config/` - configuration loading and validation components.

The existing elements form the starting point. **A fully implemented runtime registry, persisitent registry service, artifact vision store, and lifecycle management workflow are not assumed to exist.**

This documents specifies the intended contract and incremenetal implementation plan. It does not change the existing repository layout or prescribe a new directory.

---

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

---

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

---

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

---

## 6. Relationship to Existing Configuration

The existing `config/model_registry.yaml` is the natural source for **declarative model definitions** at the current stage.

Before extending it, inspect its current keys and the existing configuration schema. Changes must remain compatible with the configuration reader and settings design documented in `01_configuration_system.md`.

The registry configuration should describe models and their capabailities; environment-specific credentials, deployment endpoints, and runtime secrets must not be embedded in it. 

### 6.1 Illustrative configuration shape

The following is a **proposed example**, not a statement of the current YAML schema:


```yaml
models:
  seasonal_naive:
    family: statistical
    implementation: ts_forecasting_lab.models.statistical.naive.SeasonalNaiveForecaster
    enabled: True
    capabilities:
      probabibilistic: false
      requires_training: true
    default_parameters: {}
```

The final field names and capability values must be reconciled with the existing code and actual `SeasonalNaiveForecaster` constructor before implementation. 

---

### 6.2 Configuration validation

At minimum, validation should ensure:

- The top-level registry structure is valid.
- Each model identifier is unique and nonempty.
- Each enabled model has a resolvable implementation.
- The implementation conforms to the established forecasting interface.
- Parameter defaults match the implementation's accepted initialization contract.
- Capabilities fields use consistent types and documented meanings.

Validation should fail with actionable error messages rather than silently skipping malformed entries. 

---

## 7. Model Identifier Policy

Model identifiers should be:

- Stable across ordinary refactoring.
- Unique within the registry.
- Human-readable and suitable for logs, experiments, and configuration.
- Independent of a particular training run or artifact version.

Use lowercase snake_case names when practical, such as `seasonal_naive`.

Renaming an identifier is a compatibility change because saved experiment metadata and downstream configurations may refer to it. Prefer aliases or an explicit migration policy if renaming becomes necessary.

---

## 8. Runtime refistry Interface

A future runtime registry should expose a small, explicit interface. The following signatures are **illustrative design targets**, not currently implemented APIs:

```python
registry.list_models()  # model identifiers and metadata
registry.get_model_info(model_id) # metadata for one implementation
regitsry.create(model_id, **params) # a new forecaster instance
```

A registry factory must return a fresh model instance rather than a shared mutable trained object. 

The runtime registry should delegate forecasting behavior to `BaseForecaster` implementations. It should not create alternative `fit`, `predict`, `save`, or `load` conventions.

---

## 9. Discovery and Instantiation Worflow

1. Load registry configuration using the existing configuration infrastructure.
2. Validate the registry schema and identifier uniqueness.
3. Resolve the requested model identifier.
4. Check whether the model is enabled and available.
5. Resolve the implementation safely from an approved reference. 
6. Validate or normalize initialization parameters.
7. Instantiate the model.
8. Return the instance to the calling workflow.
9. record model identity, implemenetation version, and effective parameters in run metadata when supported.

**Security requirement:** Do not evaluate arbitrary configuration strings as Python expressions. If import paths are used, resolve them through controlled imports and explicit validation; a stricter allowist may be appropriate for production environments.

---

## 10. Capability Metadata

Capability metadata helps consumers determine whether a model is suitable for a task without inferring behavior from its name.

Potential fields include:

| Capability | Question answered |
|---|---|
| Single-series support | Can it forecast one time series? |
| Multi-series support | Can it handle multiple series in one dataset or workflow? |
| Exogenous variables | Can it use known or observed covariates? |
| Probabilitic forecasts | Can it produce distributions or intervals? |
| Incremental updates | Can an existing fitted model be updated? |
| Serialization | Can it be saved and loaded reliably? |
| Minimum history | What amount of data is required? |
| Supported frequency | Are there frequency restrictions? |

  Do not mark a cpabaility as supported until its behaviour has been implemented and tested. 
  Distinguish **not supported**, **supported**, and **not yet assessed** where useful.

---

## 11. Model Definitions Versus Trained Artifacts

The initial registry may only need to manage implementation definitions. A future production workflow will also need to track fitted artifacts.  

For each trained artifact, useful metadata may include:

- Stable model identifier.
- Artifact version or immutable run identifier.
- Source-code revision or package version.
- Effective hyperparameters.
- Training dataset reference or fingerprint.
- Training and validation time window.
- Forecast horizon and target definition.
- Evaluation results and metric definitions.
- Serialization format and artifact URI.
- Artifact checksum.
- Creation timestamp and environment information.

---

## 12. Versioning Strategy

Maintain separate identities for:

1. **Implementation version:** The code and interface used to construct a model.
2. **Configuration version:** The parameters and settings applied to a run.
3. **Artifact version:** The immutable fitted-model output from that run.

A new fitted model does not necessarily imply a new implementation version. Likewise, a code change does not retroactively modify previously produced artifacts.

Version records should be immutable after publication, with new records created for retraining or material changes.

---

## 13. 



---

## 20.



---

## 21. Related Documents

- `docs/architecture/00_platform_architecture.md`
- `docs/architecture/01_configuration_system.md`
- `docs/architecture/02_forecasting_framework_design.md`
- `docs/architecture/03_forecaster_interface.md`
- `docs/architecture/04_dataset_design.md`
- `docs/architecture/07_backtesting_design.md` *(planned)*
- `docs/architecture/08_evaluation_framework.md` *(planned)*
- `docs/architecture/11_model_serving.md` *(planned)*
- `docs/architecture/12_experiment_tracking.md` *(planned)*
- `docs/engineering/01_engineering_standards.md`
- `docs/documentation/01_documentation_strategy.md`

---

**Guiding principle:** The registry makes forecasting implementations discoverable and reproducible without changing how forecasters behave. Model definitions, trained artifacts, experiments, and deployments are related—but distinct—entities.
