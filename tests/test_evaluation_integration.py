import pandas as pd
import pytest 

from ts_forecasting_lab.data.dataset import ForecastDataset
from ts_forecasting_models.statistical.naive import SeasonalNaiveForecaster
from ts_forecasting_lab.backtesting.splitter import BacktestConfig 
from ts_forecasting_lab.backtesting.runner import run_backtest 
from ts_forecasting_lab.evaluation.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    mean_bias
)