# 01. Purpose

Define reproducible identification, recording, persistence, comparison and audit of forecasting experiments. Tracking stores evidence; it does **not** fit models. generate backtesting folds, calculate evaluation metrics and serve predictions.

**Initial deliverable:** local, filesystem-backed experiment manifests and artifacts for single-series point forecasts. Do not require MLflow, databases, cloud services or model serialization in teh first implementation. 

---

# 02. Relationship to Existing Architecture

| Document/component | Owns | Tracking responsibility |
|---|---|---|
| 01 Configuration | Validated settings | Persist sanitized resolved configuration |
| 03 Model Interfaces | `BaseForecaster`, `ForecastResult` | Record model ID, parameters and version |
| 04 Dataset | `ForecastDataset` validation | Record source, identity, frequency and checksum | 
| 06 Model registry | Model discovery | Reference model identity; avoid duplicate registry |
| 07 Backtesting | Splits, fitting and long-form predictions | Persist protocol and original records |
| 08 Evaluation | Metrics, aggregation, comparison | Persist computed outputs; never recompute |
| 09 Pipeline | Workflow orchestration | Establish run context and invoke tracker |
| 10 Logging | Operational events | Correlate logs with `run_id` | 
| 11 Serving | Approved artifact inference | Provide traceable approved model references | 
| 13 Plugins | Extensibility | Optional tracking backend later |
| 14 Testing | Test strategy | Verify tracking integrity and recovery |
| 15 Deployment | Infrastructure | Configure storage, access and retention | 

Reuse existing repository paths and placeholders after inspecting the actual code. 

---

# 03. Principles



---

# 04. Vocabulary and Hierarchy 



---

# 05. Architecture



---

# 06. Run Lifecycle



---

# 07. Manifest Contract 



---

# 08. Required Provenance



---

# 09. Prediction and Evaluation Artifacts



---

# 10. Local Artifact Layout 



---

# 11. Comparison and Scientific Validity 



---

# 12. Model Artifact Lineage and Approval



---

# 13. Storage Backend Choices



---

# 14. Logging and Monitoring Boundary 



---

# 15. Security, Retention and Reliability



---

# 16. Testing Matrix



---

# 17. First-Release Acceptance Criteria



--- 

# 18. Incremental Delivery Plan



---

# 19. Open Decisions



--- 

# 20. Suggested Copilot Prompt 



---
