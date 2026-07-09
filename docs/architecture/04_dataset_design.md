# Dataset Design 

**Status:** Accepted

**Date:** 2026-07-09

--- 

# 1. Overview

This 


---

# 2. Why Dataset Design Matters?


---

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

--- 

# 4. Required Columns 

Every forecasting dataset should contain:
```text
unique_id
ds
y
```

--- 
