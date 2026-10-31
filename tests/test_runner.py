"""
    Tests for single-series backtesting execution and alignment.
"""

import pandas as pd
import pytest

from ts_forecasting_lab.backtesting.runner import run_backtest, RESULT_COLUMNS
from ts_forecasting_lab.backtesting.splitter import BacktestConfig
from ts_forecasting_lab.data.dataset import ForecastDataset
from ts_forecasting_lab.models.statistical.naive import SeasonalNaiveForecaster

