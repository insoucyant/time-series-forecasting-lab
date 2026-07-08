from pathlib import Path
from typing import Any

import pandas as import pd 
import pytest 

from ts_forecasting_lab.models.base import BaseForecaster, ForecastResult

class DummyForecaster(BaseForecaster):
    """ Tiny concrete forecaster used only for testing BaseForecaster."""
    
    def __init__(self) -> None:
        super().__init__(model_name="dummy_forecaster")
        
    def fit(self, data: pd.DataFrame, **kwargs: Any) -> BaseForecaster:
        self.is_fitted = True 
        return self 
    
    def predict(self, horizon: int, **kwargs: Any) -> ForecastResult:
        self._check_is_fitted()
        
        predictions = pd.DataFrame(
            {
                "ds": pd.date_range(start="2026-01-01", periods=horizon, freq="D")
                "yhat": [1.0] * horizon
            }
        )
        
        return ForecastResult(
            predictions=predictions,
            horizon=horizon,
            model_name=self.model_name,
            frequency="D",
            metadata={"source": "dummy"},
        )