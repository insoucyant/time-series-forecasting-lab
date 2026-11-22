"""Evaluate forecasts produced by the backtesting runner using various metrics."""

from dataclasses import dataclass
import pandas as pd

from ts_forecasting_lab.evaluation.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    mean_bias,
)

@dataclass
class EvaluationResults:
    overall: pd.DataFrame
    by_fold: pd.DataFrame
    by_horizon: pd.DataFrame


def calculate_metrics(forecasts: pd.DataFrame) -> dict:
    """Calculate evaluation metrics for a set of forecast observations."""

    actual = forecasts["y_true"]
    predicted = forecasts["y_pred"]

    return {
        "mae": mean_absolute_error(actual, predicted),
        "mse": mean_squared_error(actual, predicted),
        "rmse": root_mean_squared_error(actual, predicted),
        "bias": mean_bias(actual, predicted),   
    }

def evaluate_forecasts(forecasts: pd.DataFrame) -> EvaluationResults:
    """Evaluate one model's successful backtest forecasts."""
    required_columns = {
        "fold_id",
        "horizon",
        "y_true",
        "y_pred",
        "fit_status",
        "predict_status",
    }

    missing = required_columns - set(forecasts.columns)

    if missing:
        raise ValueError(
            f"Forecasts DataFrame is missing required columns: {sorted(missing)}"
        )

    if forecasts.empty:
        raise ValueError("Forecasts DataFrame is empty. Cannot evaluate.")

    # Do not silently exclude failed forecasts; raise an error if any exist.
    if (
        not forecasts["fit_status"].eq("success").all()
        or not forecasts["predict_status"].eq("success").all()
    ):
        raise ValueError(
            "Forecasts contain unsuccessful fit or predict statuses. Cannot evaluate."
        )

    if forecasts[["y_true", "y_pred"]].isna().any().any():
        raise ValueError(
            "Forecasts contain missing actual or predicted values. Cannot evaluate."
        )

    # Overall Evaluation 
    overall = pd.DataFrame([calculate_metrics(forecasts)])

    # Evaluate by backtesing fold
    fold_rows = []

    for fold_id, group in forecasts.groupby("fold_id"):
        metrics = calculate_metrics(group)
        metrics["fold_id"] = fold_id
        fold_rows.append(metrics)

    by_fold = pd.DataFrame(fold_rows)

    # Evaluate by forecast horizon 
    horizon_rows = []

    for horizon, group in forecasts.groupby("horizon"):
        metrics = calculate_metrics(group)
        metrics["horizon"] = horizon
        horizon_rows.append(metrics)

    by_horizon = pd.DataFrame(horizon_rows)

    return EvaluationResult(
        overall=overall,
        by_fold=by_fold,
        by_horizon=by_horizon,
    )