from pathlib import Path 
import pandas as pd 
import pytest 

from ts_forecasting_lab.models.base import ForecastResult
from ts_forecasting_lab.models.statistical.naive import SeasonalNaiveForecaster

def sample_training_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ds" : pd.date_range(start="2026-01-01", periods=10, freq="D"),
            "y": [10, 11, 12, 13, 14, 20, 21, 22, 23, 24],
        }
    )
    
def test_seasonal_naive_initialization() -> None:
    