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