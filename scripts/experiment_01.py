import pandas as pd
from pathlib import Path 
import platform 

from dataclasses import asdict 
from datetime import datetime, timezone
from uuid import uuid4 

from ts_forecasting_lab.data.dataset import ForecastDataset
from ts_forecasting_lab.models.statistical.naive import SeasonalNaiveForecaster
from ts_forecasting_lab.backtesting.splitter import BacktestConfig 
from ts_forecasting_lab.backtesting.runner import run_backtest
from ts_forecasting_lab.evaluation.runner import evaluate_forecasts
from ts_forecasting_lab.evaluation.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    mean_bias
)
from ts_forecasting_lab.tracking.artifact_writer import (
    save_experiment_artifacts,
)

# 1. Create a small daily time series
data = pd.DataFrame({
    "date": pd.date_range("2026-01-01", periods=20, freq="D"),
    "sales": list(range(20)),
})

# 2. Create a ForecastDataset
dataset = ForecastDataset(
    data=data,
    timestamp_col="date",
    target_col="sales",
    frequency="D",
)

# 3. Define the hsitorical evaluation protocol
config = BacktestConfig(
    strategy="expanding",
    initial_train_size=10,
    horizon=3,
    step=3,
    gap=0,
)

# 4. Run the forecasting experiment
results = run_backtest(
    dataset=dataset,
    config=config,
    model_factory=lambda: SeasonalNaiveForecaster(season_length=1),
    run_id=uuid4().hex,
)

# 5. Inspect the results
print("\nForecasting results:")
print(
    results[
        [
            "fold_id",
            "forecast_origin",
            "target_timestamp",
            "horizon",
            "y_true",
            "y_pred",
        ]
    ].to_string(index=False)
)

print("\nTotal forecast observations:", len(results))

#Evaluate forecasting performance using the implemented metrics
actual = results["y_true"]
predicted = results["y_pred"]

mae = mean_absolute_error(actual, predicted)
mse = mean_squared_error(actual, predicted)
rmse = root_mean_squared_error(actual, predicted)
bias = mean_bias(actual, predicted)


print("\nEvaluation metrics:")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"Bias: {bias:.4f}")


print("\nEvaluation by forecast horizon:")
for horizon, group in results.groupby("horizon"):
    horizon_mae = mean_absolute_error(group["y_true"], group["y_pred"])
    horizon_mse = mean_squared_error(group["y_true"], group["y_pred"])
    horizon_rmse = root_mean_squared_error(group["y_true"], group["y_pred"])
    horizon_bias = mean_bias(group["y_true"], group["y_pred"])

    print(f"\nHorizon {horizon}:")
    print(f"  MAE: {horizon_mae:.4f}")
    print(f"  MSE: {horizon_mse:.4f}")
    print(f"  RMSE: {horizon_rmse:.4f}")
    print(f"  Bias: {horizon_bias:.4f}")


print("\nForecast identifiers:")
print(
    results[["run_id", "model_id", "series_id"]]
    .drop_duplicates()
    .to_string(index=False)
)
evaluation = evaluate_forecasts(results)
print("\nOverall evaluation metrics:")
print(evaluation.overall.to_string(index=False))

print("\nEvaluation metrics by fold:")
print(evaluation.by_fold.to_string(index=False))

print("\nEvaluation metrics by horizon:")
print(evaluation.by_horizon.to_string(index=False))


# ============================================================
#               Persist experiment metadata
# ============================================================

project_root = Path(__file__).resolve().parents[1]

run_id = str(results["run_id"].iloc[0])

metadata = {
    "experiment_name": "experiment_01",
    "run_id": run_id, 
    "recorded_at_utc": datetime.now(timezone.utc).isoformat(),

    "dataset": dataset.get_metadata(),

    "model": {
        "model_id": str(results["model_id"].iloc[0]),
        "parameters": {
            "season_length": 1,
        }, 
    },

    "backtesting": asdict(config), 

    "results": {
        "n_forecast_observations": len(results),
        "n_folds": int(results["fold_id"].nunique()),
        "n_series": int(results["series_id"].nunique()),
    },

    "environment": {
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "platform": platform.platform(),
    }, 
}



# ============================================================
#               Persist experiment artifacts
# ============================================================

output_dir = save_experiment_artifacts(
    artifact_root=project_root / "artifacts",
    experiment_name="experiment_01",
    run_id=run_id,
    forecasts=results,
    evaluation=evaluation,
    metadata=metadata,
)

print(f"\nExperiment artifacts saved to: {output_dir}")








# Run this script using the command: `python scripts/experiment_01.py`