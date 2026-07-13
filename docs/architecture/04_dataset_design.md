# Dataset Design 

**Status:** Accepted

**Date:** 2026-07-12

--- 

# 1. Overview

This document how time series data should be represented inside the Time Series Forecasting Lab.

The goal is to create one standard dataset structure that can support:

- Univariate forecasting 
- Multivariate forecasting 
- Local models/forecasting
- Global models/forecasting
- Statistical forecasting
- Machine learning forecasting
- Deep learning forecasting
- Transformer models 
- Foundation models
- Hierarchical forecasting
- Demand sensing
- Causal forecasting
- Scenraio planning
- Explainability
- Optimization
- Decision Intelligence

Rather than allowing every forecasting model to define its own data format, the platform standardizes on a single internal representation. 

This allows every component of the platform to communicate using a common language. 

The central idea is:

> Standardize the data format early so the models, features, backtesting, and pipelines can all depend on the same structure. 


---

# 2A. Why Dataset Design Matters?

Forecasting models often expect different input formats.

For example:
- ARIMA usually needs a single ordered target series
- Prophet expects column names `ds` and `y`.
- XGBoost needs lag and rolling features.
- TFT needs historical targets, knows future covariates, static covariates, encoder windows, and decoder windows.
- Foundation models may need context windows.

Without a common dataset abstraction, every model will need custom data handling. 

That creates duplication and makes the framework harder to maintain.

---

# 2B. Design Goals

The dataset layer should satisfy the following objectives:

## Consistency

Every forecasting model should consume a common dataset representation.

---

## Extensibility

The dataset should support future forecasting models without requireing structural changes. 

---

## Production Readiness 

The design should work for:

- batch forecasting 
- streamline forecasting 
- real-time demand forecasting 
- production deployment 

---

# Separation of Concern

The dataset object should represent data.

It should not:

- train forecasting models
- compute metrics
- generate plots
- perfrom optimization

---


## Reusability 

The same dataset should be reusable by:

- feature engineering
- forecasting 
- explainability
- benchmarking 
- optimization
- deployment 



# 3. Standard Forecasting Table

The core internal format should be:

| Column | Meaning |
|---|---|
| `unique_id` | Identifier of the Time Series |
| `ds` | Timestamp column |
| `y` | Target value |
| covariates | Optional additional variables |

Example:

| unique_id | ds | y | price | promo | holiday |
|---|---|---:|---:|---:|---:|
| store_001 | 2026-01-01 | 120 | 10.5 | 0 | 1 |
| store_001 | 2026-01-02 | 135 | 10.5 | 1 | 0 |
| store_002 | 2026-01-01 | 88 | 8.0 | 0 | 1 |

This format is inspired by common forecasting libraries and is simple enough to support both beginner and advanced models. 

Example:

| unique_id | ds | y | price | promo | holiday |
|---|---|---:|---:|---:|---:|
| store_001 | 2026-01-01 | 120 | 10.5 | 0 | 1 |
| store_001 | 2026-01-02 | 135 | 10.5 | 1 | 0 |
| store_002 | 2026-01-01 | 88 | 8.0 | 0 | 1 |

This format is inspired by common forecasting libraries and is simple enough to support both beginner and advanced models.

--- 

# 4. Required Columns 

Every forecasting dataset should contain:
```text
unique_id
ds
y
```

For a single univariate series, `unique_id` can be a constant value such as:

```text
series_001
```

This allows the same framework to handle both one series and many series.
--- 

# 5. Optional Columns

Optional columns may include:
```text
price
promotion
holiday
temperature
inventory
marketing_spend
event_flag
competitor_price
weather
fuel_price
search_trend
```

These are covariates. These variables become candidate predictors during feature engineering.

They may be used by:

- machine learning models
- deep learning models
- transformer models
- causal feature analysis
- scenario forecasting 


--- 


# 6. Local vs Global Models

The dataset should support both:

## Local Models

A local model trains one model per time series.

Example:

```text
one ARIMA model per store
```

## Global Models

A global model trains one model across many time series.

Example:

```text
one TFT model across all stores
```

The `unique_id` column makes both design possible. 

---

# 7. Dataset Categories

The platform should distinguish between different categories of variables.

## Target Variables

The value to forecast.

Example:

```
Demand
Sales
Electricity Load
Wind Generation
Stock Price
```


## Historical Covariates

Observed only in the past.

Examples:

- previous inventory 
- historical weather
- historical prices

## Known Future Covariates

Some variables are known in advance: Known future covariates. They are available before the forecast is generated.

Examples:

- holidays
- calendar features: day of week, month
- planned promotions
- scheduled/planned prices

This can be passed to models that support future covariates.

--- 

## Unknown Future Covariates

Some variables are not known in advance. They are not available at forecast time.

Examples:

- future demand
- future weather, unless forecasted separately
- future competitor behavior

These should be treated carefully. 

Using unknown future variables directly can create data leakage. These should never be used directly for future predictions unless separately forecast. 

--- 

## Static Covariates

Attributes that rarely change.

Examples:

```
Store Size
Region
Product Category
Plant Capacity 
```

Static variables are especially important for global forecasting models. 

---

# 9. Hierarchical Forecasting 

The dataset should eventually support hierarchical forecasting. 

Examples:

```
Country 

↓

Region

↓

State

↓

City 

↓

Store
```

or

```
Company 

↓

Business Unit

↓

Product Family 

↓

SKU
```

Future version should include hierarchy metadata that enables reconciliation algorithms. 
---


# 10. Temporal Hierarchies

The platform should also support multiple temporal resolutions.

Examples:

```
Hourly

↓

Daily

↓

Weekly

↓

Monthly 

↓

Quarterly

↓

Yearly 
```

This enables temporal reconciliation


---

# 11. Probabilistic Forecasting 

The dataset design should not assume point forecasts only. 

Future forecasting models may produce:

- quantiles
- prediction intervals
- probability distributions

The dataset should therefore remain compatible with probabilistic outputs.

---

# 12. Demand Sensing 

Future versions should support real-time demand sensing.

Examples include:

- weather
- POS transactions
- online traffic
- promotions
- social media
- search trends

These mau arrive at much higher frequencies than historical forecasting data.

The dataset layer should remain flexible enough to integrate them. 

---

# 13. Causal Forecasting

Future forecasting system may distinguish between:

```
Observed Variables

↓

Treatment Variables

↓

Outcome Variables
```

Examples include:

- pricing interventions
- promotions
- policy changes

The dataset abstraction should not prevent causal modeling. 

---

# 14. Scenario Planning 

Future scenarios may include hypothetical values.

Examples:

```
Promotion = 20%

Weather = Extreme Heat

Oil Price = +30%

Demand Shock = Pandemic
``` 

These scenario variables should be supported without changing the dataset structure.

---

# 15. Data Validation

The `dataset object` should validate :
- required columns
- duplicate timestamps
- duplicate IDs
- missing timestamps
- missing target values
- invalid frequencies
- incorrect datatypes

Invalid datasets should fail early. 

---

# 16. Data Leakage Principle

The dataset layer should help prevent leakage.

A model should not accidentally use information from the future during training or prediction.

Examples of leakage:

- using future target values as features
- computing rolling averages using future observations
- using test-period covariates that would not have been known at prediction time
- future weather observation
- future inventory

The framework should encourage leakage-free forecasting. 

--- 

# 17. ForecastDataset Object 

The future implementation should define:

```python
ForecastDataset(...)
```

Responsibilities include:

- store data
- validate schema
- infer frequency
- expose metadata
- sort data
- group by series
- filter series
- inspect missing values

It should **not**:

- forecast
- evaluate 
- optimize 

---

# 18. Dataset Flow

```
CSV

↓

Parquet

↓

Database

↓

API

↓

ForecastDataset

↓

Validation

↓

Feature Engineering

↓

Forecasting

↓

Evaluation

↓

Decision Intelligence
``` 

---

# 19. Future Extensions

The dataset abstraction should eventually support:

- streaming data
- Kafka
- Spark
- Ray Datasets
- Feature Stores
- Delta Lake
- Iceberg
- DuckDB
- Arrow
- cloud object storage


without changing the forecasting API

---

# 20. Design Principles

The dataset layer follows:

- Single Responsibility Principle
- Open/Closed Principle
- Separation of Concerns
- Extensibility 
- Type Safety
- Production Readiness


---

# 21. Implementation Roadmap

This document guides the implementation of:

src/
└── ts_forecasting_lab/
    └── data/
        ├── dataset.py
        ├── validators.py 
        ├── frequency.py
        ├── hierarchy.py
        ├── schema.py 
        ├── splitter.py    

--- 

# 22. Summary 

The dataset layer is the foundation of the forecasting platform. 

By standardizing on a single internal representation based on:

```
unique_id
ds
y
covariates
``` 

The platform can support forecasting models ranging from ARIMA to future foundation models, while remaining extensible enough for hierarchical forecasting, probabilistic forecasting, demand sensing, causal inference, scenario planning, optimization, and decision intelligence. 

The dataset should be viewed as a reusable platform component rather than merely a DataFrame wrapper. 



