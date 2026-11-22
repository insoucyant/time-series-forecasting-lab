import pandas as pd

from ts_forecasting_lab.data.dataset import ForecastDataset
from ts_forecasting_lab.models.statistical.naive import SeasonalNaiveForecaster
from ts_forecasting_lab.backtesting.splitter import BacktestConfig 
from ts_forecasting_lab.backtesting.runner import run_backtest
from ts_forecasting_lab.evaluation.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    mean_bias
)

# 1. Create a small daily time series
data = pd.DataFrame({
    "date": pd.date_range(start="2026-01-01", periods=20, freq="D"),
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
    run_id="experiment01",
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