import pandas as pd

from ts_forecasting_lab.data.dataset import ForecastDataset
from ts_forecasting_lab.models.statistical.naive import SeasonalNaiveForecaster
from ts_forecasting_lab.backtesting.splitter import BacktestConfig 
from ts_forecasting_lab.backtesting.runner import run_backtest

# 1. Create a small daily time series
data = pd.DataFrame({
    "date": pd.date_range(start="2026-01-01", periods=20, freq="D"),
    "sales": list(range(20)),
})

# 2. Create a ForecastDataset
dataset = ForecastDataset(
    data=data,
    time_col="date",
    target_col="sales",
    frequency="D",
)