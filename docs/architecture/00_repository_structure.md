# Repository Structure

**Status:** Accepted
**Date:** 2026-08-02

Why does this file exist? \\
As the repository grows to 250-400 files, this document becomes the map that explains where everything belongs and why it belongs there? \\


# 1. Overview

This document describes the organization of the **Time Series Forecasting Lab** repository.

The repository is designed as a long-term , production-grade, forecasting platform rather than a collection of forecasting algorithms or notebooks. 

The repository structure should promote:

- modularity 
- maintainability
- discoverability
- extensibility
- separation of concerns
- production readiness

Every directory should have a clearly defined responsibility. 

---

# 2. Design Principles

The repository organization follows several guiding principles. 

## Platform Before Algorithms

Infrastructure should be built before forecasting models. 

Examples include:

- configuration 
- datasets
- feature engineering 
- pipelines
- monitoring 

These platform components support every forecasting algorithm. 

---

## Separation of Concerns

Each directory should own one responsibility.

Directories should not contain unrelated functionality. 


---

## Open for Extension 

New forecasting models should integrate without modifying existing repository organization. 

---

## Discoverability 

Developers should easily locate:

- forecasting models
- pipelines
- datasets
- documentation 
- benchmarks
- examples

---

## Production First 

The repository should be organized as an industrial software project rather than an academic notebook collection. 

---


# 3. High-Level Repository Structure

```
TIME-SERIES-FORECASTING-LAB/

├── config/
├── data/
├── docs/
├── examples/
├── notebooks/
├── benchmarks/
├── reports/
├── tests/
├── scripts
├── src/
├── .github/
├── pyproject.toml
├── README.md
└── LICENSE 
```

---

# 4. Root-Level Directories

## config/

Contains platform configuration.

Examples include:

- config.yaml
- environment-specific configuration
- model registry configuration 

Responsibilities:

- application configuration 
- runtime configuration 
- deployment configuration 

Should not contain:

- business logic
- forecasting models

---

## data/

Contains datasets used during development.

Typical structure:

```
raw/

interim/

processed/

external/

sample/
```

Responsibilities:

- local datasets
- sample datasets
- benchmark datasets

Large production datasets should remain outside the repository.

--- 

## docs/

Contains architecture and project documentation.

Subdirectories may include:

```
vision/

architecture/

engineering/

research/

roadmap/

tutorials/

case_studies/
```

Documentation should explain why systems are designed in a particular way.

--- 

## examples/

Contains complete end-to-end examples.

Examples should demonstrate:

- model training
- forecasting
- evaluation 
- deployment

---

## notebooks/

Contains exploratory notebooks. 

These are intended for experimentation only.

Production code should not depend on notebooks.

--- 

## benchmarks/

Contains benchmark infrastructure.

Examples include:

- benchmark datasets
- benchmark configurations
- benchmark results

---

## reports/

Contains general artifacts.

Examples include:

- figures
- model cards
- evaluation reports

Reports should be reproducible.

--- 

## tests/

Contains automated tests.

Test categories include:

```
unit 

integration

end-to-end

performance
```

Every production module should include corresponding tests.

--- 

## scripts/

Contains executable utilities.

Examples include:

- training scripts
- benchmark runners
- deployment utilities

Scripts should orchestrate platform components rather than implement business logic. 

---

## src/

Contains production source code.

All platform implementation belongs here. 

--- 

# 5. Source Code Organization 

The production package is located under:

```
src/

└── ts_forecasting_lab/
```

This package contains all reusable forecasting components. 

---

# 6. Platform Foundation

The platform foundation provides reusable infrastructure.

Proposed structure:

```
config/

data/

features/

pipelines/

evaluation/

backtesting/

registry/

tracking/

monitoring/

serving/

deployment/

logging/

utils/
```

These modules should remain independent of forecasting algorithms. 

--- 

## config/

Responsibilities:

- settings
- schema
- readers
- environment management

---

## data/

Responsibilities:

- ForecastDataset
- validators
- splitters
- frequency handling
- hierarchy handling 

---

## features/

Responsibilities:

- lag features
- rolling statistics
- calendar features
- trend features
- seasonality features
- demand sensing features
- feature selection 
- feature validation 

---

## pipelines/

Responsibilities:

- training pipelines
- inference pipelines
- forecasting workflows

Pipelines coordinate components.

They should not contain forecasting logic. 

--- 

## evaluation/

Responsibilities:

- evaluation metrics
- calibration
- forecast value added
- business metrics

--- 

## backtesting/

Responsibilities:

- model registration
- metadata
- versioning

--- 

## tracking/

Responsibilities:

- experiment tracking
- run metadata
- artifacts

---

## monitoring/

Responsibilities:

- drift detection
- production monitoring 
- observability 

## serving/

Responsibilities:

- prediction APIs
- inference services

--- 

## deployment/

Responsibilities:

- Docker
- Kubernetes
- cloud deployment 

## logging/

Responsibilities:

- structure logging
- audit logging 

--- 

## utils/

Contains reusable utilities shared across multiple platform modules. 

--- 

# 7. Forecasting Engine

Forecasting models are organized by methodology.


 


