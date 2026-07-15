# Feature Engineering Framework

**Status:** Accepted

**Date:** 2026-07-13 

# 1. Overview

Feature Engineering is one of the most important components of industrial forecasting platform. 

While forecasting models often receive the most attention, real-world forecasting accuracy frequently depends more on high-quality features than on the forecasting algorithm itself.

The objective of this subsystem is to design a reusable, production-grade feature engineering framework that can support:

- Statistical Forecasting
- Machine Leaning Forecasting 
- Deep Learning Forecasting 
- Foundation Models
- Demand Sensing
- Hierarchical Forecasting 
- Probabilistic Forecasting 
- Causal Forecasting 
- Scenario Planning 
- Decision Intelligence

Rather than manually creating features for each forecasting model, the platform should expose a common feature engineering pipeline.

--- 

# 2. Design Goals

The Feature Engineering Framework should satisfy the following goals:

## Consistency

Features should be generated consistently across all forecasting models.

---

## Reusability 

Features should be reusable across multiple forecasting models.

--- 

## Extensibility 

Adding new feature generators should not require modifying existing feature generators.

---

## Production Readiness

Feature generation should support:

- batch processing
- streaming pipelines
- online inference
- feature stores

---

## Leakage Prevention

The framework should prevent accidental use of future information.

--- 

## Explainability 

Generated features should be traceable and understandable.

---

# 3. Why Feature Engineering Matters?

Forecasting models rarely learn directly from raw observations. 

Instead, they learn from carefully constructed representations of historical behavior.

Example include:

- lag values
- rolling statistics
- seasonality 
- holidays
- weather
- promotions
- search trends
- hierarchical information

Well-designed features often improve forecasting performance more than changing forecasting algorithm.

--- 

# 4. Feature Engineering Pipeline

The feature engineering pipeline should follow the architecture below:

```
Raw Dataset

↓

Validation

↓

Missing Value Handling

↓

Outlier Handling

↓

Frequency Alignment

↓

Feature Generation

↓

Feature Selection

↓

Forecasting Model
```

Each stage should have a single responsibility.

--- 

# 5. Feature Categories

The framework should organize features into logical categories.

## Historical Features 

Information derived directly from historical observations.

Examples:

- previous demand
- previous sales
- previous temperature

--- 

## Lag Features

Lag features represent previous observations.

Examples:

```math
y_{t-1}, \\

y_{t-2}, \\

y_{t-7}, \\

y_{t-14}, \\

y_{t-28} 
```

Lag features are among the most important forecasting features.

--- 

## Rolling Window Features

Rolling statistics summarize recent history.

Examples:

```
Rolling Mean

Rolling Median

Rolling Maximum

Rolling Minimum

Rolling Standard Deviation

Rolling Variance
```

Different window sizes may be generated.

Examples:

```
3

7

14

28

56
```

---

## Expanding Window Features

Expanding windows summarize the complete history.

Examples:

```
Expanding Mean

Expanding Variance

Expanding Maximum
```

--- 

## Exponentially Weighted Features

Examples include:

- EWMA
- Exponential variance

These emphasize recent observations.

---

# 6. Calendar Features

Calendar variables capture repeating temporal patterns.

Examples include:

- Hour
- Day of Week
- Day of Month
- Week Number
- Month
- Quarter
- Year
- Weekend
- Holiday
- Fiscal Period

Calendar features are useful across nearly all forecasting domains. 

---

# 7. Trend Features

Trend features describe long-term movement.

Examples:

- Time Index
- Linear Trend
- Polynomial Trend
- Growth Rate

--- 

# 8. Seasonality Features

Seasonality may be represented using:

- Month
- Week
- Hour
- Fourier Features
- Cyclical Encoding 

Examples:

```
sin(month)

cos(month)
```

--- 

# 9. Frequency-Based Features

Different frequencies may require different feature sets.

Examples:

Hourly 

Daily 

Weekly

Monthly

Quarterly

Yearly

The framework should automatically adapt feature generation to dataset frequency.

--- 

# 10. Statistical Features 

Examples include:

- Mean
- Median
- Variance
- Kurtosis
- Skewness
- Percentiles

These are particularly useful for machine learning models.

--- 

# 11. External Covariates

External variables may strongly influence future demand.

Examples include:

- Weather
- Fuel Price
- Inflation
- Exchange Rate
- Population
- GDP
- Competitor Pricing

These variables should be managed separately from historical target variables.

--- 

# 12. Demand Sensing Features

Demand sensing uses real-time signals.

Examples include:

- POS Transactions
- Search Trends
- Website Traffic
- Mobile App Activity
- Promotions
- Inventory Levels
- Weather Forecasts
- Social Media
- Events

These features often arrive at higher frequencies than historical forecasting data.

--- 

# 13. Static Features

Static variables rarely change.

Examples include:

```
Store Size

Store Type

Region

Climate Zone

Product Category

Manufacturer
```

Static features are particularly valuable for global forecasting models.

--- 

# 14. Hierarchical Features

Future versions of the platform should support hierarchy-aware features.

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

These features enable:

- hierarchical forecasting
- reconciliation
- cross-level learning 

--- 

# 15. Causal Features

Future versions whould support variables related to interventions.

Examples:

- Promotions
- Pricing Changes
- Advertising Campaigns
- Government Policies

These variables become treatment variables in causal forecasting.

--- 

# 16. Scenario Features

Scenario planning introduces hypothetical feature values.

Examples:

```
Price Increase

Promotion

Economic Recession

Supply Disruption

Heat Wave
```

Scenario variables allow "what-if" forecasting.


--- 

# 17. Embedded Features

Future deep learning models may generate learned embeddings.

Examples include:

- Product Embeddings
- Store Embeddings
- Customer Embeddings
- Geographic Embeddings

They should integrate naturally into the feature engineering framework.

--- 

# 18. Feature Selection

Not every generated features should be used.

Possible selection techniques include:

- Correlation Filtering
- Mutual Information
- Recursive Feature Elimination
- SHAP Importance
- Permutation Importance
- Model-Based Selection

--- 

# 19. Feature Validation

Generated features should be validated.

Examples include:

- Missing Values
- Infinite Values
- Constant Features
- Duplicate Features
- Leakage Detection
- Datatype Validation

Invalid features should fail fast.

--- 

# 20. Data Leakage Prevention

The framework should actively prevent feature leakage.

Examples of leakage include:

- Future Target Values
- Future Rolling Statistics
- Future Inventory
- Future Weather Observations

Leakage prevention i mandatory for trustworthy forecasting. 

--- 

# 21. Feature Store

The long-term vision includes a production-grade Feature Store.

Responsibilities include:

- Feature Versioning 
- Feature Metadata
- Online Features
- Offline Features
- Feature Lineage
- Feature Discovery

The feature engineering framework should integrate seamlessly with the feature store. 

--- 

# 22. Explainability

Feature engineering should support explainability. 

Examples include:

- SHAP Values
- Feature Importance
- Partial Dependence
- Prediction Attribution 

Business users should understand which features influenced a forecast. 

--- 

# 23. Future Extensions

Future version may support:

- Streaming Features
- Kafka
- Spark
- Ray Data
- Delta Lake
- Iceberg
- DuckDB
- Arrow
- Vector Features
- LLM-generated Features

--- 

# 24. Design Principles

The Feature Engineering Framework follows:

- Single Responsibility Principle
- Open/Closed principle
- Separation of Concerns
- Extensibility
- Reproducibility
- Explainability
- Production Readiness

--- 

# 25. Implementation Roadmap

This documentation guides the implementation of:

```
src/
└── ts_forecasting_lab/
    └── features/
        ├── base.py
        ├── lag.py
        ├── rolling.py
        ├── calendar.py
        ├── trend.py
        ├── seasonality.py
        ├── statistical.py
        ├── external.py
        ├── hierarchy.py
        ├── causal.py
        ├── scenario.py
        ├── validation.py
        ├── selection.py
        ├── registry.py
        └── pipeline.py
```

---

# 26. Summary 

The Feature Engineering Framework is one of the core platform components of the Time Series Forecasting Lab.

Rather than generating the ad hoc features for individual forecasting models, the platform provides a standardized, extensible, and production-grade feature engineering subsystem. 

This enables forecasting models ranging from statistical approaches to modern foundation models to share a common feature generation pipeline while remaining compatible with demand sensing, causal forecasting, hierarchical forecasting, explainability, optimization, and decision intelligence. 

Feature engineering should be viewed as a reusable platform capability rather than a model specific preprocessing step. 

---

# 27. Another Future Recommendation

We should distinguish between **Platform Features** and **Model-Generated Features** as the repository evolves.

* **Platform Features:** lags, rolling statistics, calendar variables, weather, hierarchy fearures, demand sending signals. They are reusable across many models.
* **Model-generated features:** transformers embeddings, learned latent representations, attention weights, or foundation-model embeddings. These are specific to a model family. 