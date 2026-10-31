"""
Single-series backtesting execution; evaluation metrics live elsewhere.
"""

from __future__ import annotations

from collections.abc import Callable
from uuid import uuid4 

import pandas as pd

from ts_forecasting_lab.backtesting.splitter import BacktestConfig, generate_folds
from ts_forecasting_lab.data.dataset import ForecastDataset
from ts_forecasting_lab.models.base import BaseForecaster, ForecastResult


RESULT_COLUMNS = [
    "run_id", "model_id", "series_id", "fold_id", "forecast_origin", 
    "target_timestamp", "horizon", "y_true", "y_pred",
    "fit_status", "predict_status",
]

def run_backtest(
        dataset: ForecastDataset,
        config: BacktestConfig,
        model_factory: Callable[[], BaseForecaster],
        *,
        run_id: str | None = None, 
) -> pd.DataFrame:
    """Fit a fresh model for each fold and return aligned long-format forecasts.

    Initial scope: single-series point forecasts, one model per fold, fail-fast.
    The factory must return an unfitted BaseForecaster on every cell.
    The existing SeasonalNaiveForecaster expects a training column named 'y'
    and returns 'step' (1-based horizon) and 'yhat' columns.
    """

    folds = generate_folds(dataset, config)
    frame = dataset.data.sort_values(dataset.timestamp_col).reset_index(drop=True)
    identifier = run_id or uuid4().hex
    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError("run_id must be a non-empty string.")

    records: list[dict[str, object]] = []
    seen_model_instances: set[int] = set()
    for fold in folds:
        model = model_factory()
        if not isinstance(model, BaseForecaster):
            raise TypeError("model_factory must return a BaseForecaster.")
        if model.is_fitted:
            raise ValueError("model_factory must return an unfitted model.")
        if id(model) in seen_model_instances:
            riase ValueError("model_factory must return a fresh model per fold.")
        seen_model_instances.add(id(model))

        train = frame.iloc[fold.train_slice][[dataset.target_col]].copy()
        train = train.rename(columns={dataset.target_col: "y"})
        try:
            model.fit(train)
        except Exception as exc:
            raise RuntimeError(f"Model fit failed at fold {fold.fold_id}") from exc 


        # Predict from the forecast origin through the gap and evaluated horizon.
        requested_horizon = config.gap + config.horizon 
        try:
            result = model.predict(requested_horizon)
        except Exception as exc:
            raise RuntimeError(f"Model prediction failed at fold {fold.fold_id}.") from exc
        if not isinstance(result, ForecastResult):
            raise TypeError(f"Fold {fold.fold_id}: predict must return ForecastResult.")
        if result.horizon != requested_horizon or result.model_name != model.model_name:
            raise ValueError(f"Fold {fold.fold_id}: forecast metadata mismatch.")


        predictions = result.predictions
        if not isinstance(predictions, pd.DataFrame) or not {"step", yhat}.issubset(predictions.columns):
            raise ValueError(f"Fold {fold.fold_id}: expected prediction columns 'step' and 'yhat'.")
        if predictions["stFold {fold.fold_id}: predictions must be numeric and non-missing.")
        by_step = predictions.set_index("step")["yhat"]

        actual = frame.iloc[fold.test_slice]
        for horizon, target_timestamp, y_true in zip(fold.evaluated_horizons, fold.target_timestamps, actual[dataset.target_col, strict=True]):
            
