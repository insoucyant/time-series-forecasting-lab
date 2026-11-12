# Model Serving Architecture

# 01. Purpose

Define how a **previously trained and approved forecasting model** can produce predictions in a controlled, reproducible runtime. Servings is distinct from model development, historical backtesting, model evaluation, experiment tracking, and infrastructure development. 

The initial target is **local batch inference** for a validated, single-series, point forecast model. A synchronous HTTP API. multi-series workloads, model routing, asynchronous execution, and scalable infrastructure are alter increments. This document specifies their boundaries without asserting they already exist.

**Core rule:** A serving request must not silently fit, tune, select, or retrain a model. Training belongs to the pipeline; serving consumes a clearly identified trained artifact or explicitly documented fitted-model instance.

---

# 02. Relationship to Existing Architecture 

| Component/document | Owns | Serving responsibility |
|---|---|---|
| `03` model interface | `BaseForecaster`, `ForecastResult`, fit/predict semantics | Invoke supported prediction interface; do not replace its schema|
| `04` dataset | `ForecastDataset` and validation rules | Validate inference history through established rules |
| `06` model registry | Model identity and construction design | Resolve approved model/version once registry is implemented |
| `07` backtesting | Historical folds and out-of-sample forecasts| No backtest execution inside serving |
| `08` evaluation | Accuracy metrics and comparisons | No recomputation of evaluation metrics inside serving |
| `09` pipeline | Training, backtesting, orchestration | Supply trained artifacts and a stable handoff |
| `10` logging and monitoring | Events, telemetry, health signals | Emit serving lifecycle events and bounded metrics | 
| `12` experiment tracking | Run history, artifact provenance, lifecycle | Retrieve or reference approved artifacts when available |
| `14` testing startegy | Test levels and acceptance evidence | Implement serving-specific tests under established test structure |
| `15` deployment architecture | packaging, hosting, scaling, secrets | Choose infrastructure; serving defines runtime contract | 

**Repository rule:** Use the existing `src/ts_forecasting_lab/serving` package and `scripts/serve_api.py` placeholder when implementation is justified. Do not create a parallel serving framework or restructure the repository speculatively. 

---

# 03. Design Principles



---

# 04. Serving Modes and Delivery Order



---

# 05. High-Level Serving Architecture



---

# 06. Boundary Between Training and Serving 



---

# 07. Current Model Interface Compatibility 



---

# 08. Conceptual request Contract 



---

# 09. Conceptual Response Contract 



---

# 10. Worked Example: Forecast Origin and Horizon



---

# 11. Model Artifact and Manifest Design



---

# 12. Model Lifecycle and Version Resolution



---

# 13. Input Data Validation and Temporal Safety



---

# 14. Serving Adapter and Dependency Boundaries



---

# 15. Batch Inference Workflow



---

# 16. Future HTTP API Design



## 16.1 HTTP Status Principles



---

# 17. Runtime Model Loading, Caching and Concurrency



---

# 18. Errors, Retries and Idempotency



---

# 19. Logging, Monitoring and Observability Integration 



---

# 20. Security, Governance and Data Policy



---

# 21. Performance, Capacity and SLOs



---

# 22. Deployment Boundary and Infrastructure Readiness



---

# 23. Testing Startegy and Acceptance Evidence



---

# 24. Incremental Implementation Plan



---

# 25. Definition of Done: Initial Serving Architecture



---

# 26. Open Design Decisions



---

# 27. Relationship to the Next Documents
