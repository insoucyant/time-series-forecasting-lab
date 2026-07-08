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
        
    def save(self, path: Path) -> None:
        path.write_text("dummy_model", encoding="utf-8")
        
    
    @classmethod 
    def load(cls, path: Path) -> BaseForecaster:
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        
        model = cls()
        model.is_fitted = True
        return model
    
    
def test_forecast_result_accepts_valid_predictions() -> None:
    predictions = pd.DataFrame(
        {
            "ds": pd.date_range(start="2026-01-01", periods=3, freq="D")
            "yhat": [10.0, 11.0, 12.0],
        }
    )
    
    result = ForecastResult(
        predictions=predictions,
        horizon=3,
        model_name="dummy_forecaster",
        frequency="D",
    )
    
    assert result.horizon == 3
    assert resault.model_name == "dummy_forecaster"
    assert len(result.predictions) == 3
    assert result.frequency == "D"
    

def test_forecast_result_rejects_invalid_horizon() -> None:
    predictions = pd.DataFrame({"yhat": [1.0, 2.0]})
    
    with pytest.raises(ValueError):
        ForecastResult(
            predictions=predictions,
            horizon=0,
            model_name="dummy_forecaster",
        )
        
def test_base_forecaster_initial_state() -> None:
    model = DummyForecaster()
    
    assert model.model_nae == "dummy_forecaster"
    assert model.is_fitted is False 
    
    
def test_base_forecaster_fit_sets_fitted_state() -> None:
    model = DummyForecaster()
    data = pd.DataFrame({"y": [1,2,3]})
    
    fitted_model = model.fit(data)
    
    assert fitted_model is model
    assert model.is_fitted is True 
    

def test_base_forecaster_predict_requires_fit() -> None:
    model = DummyForecaster()
    
    with pytest.raises(RuntimeError, match="must be fitted before prediction"):
        model.predict(horizon=3)
        
def test_base_forecaster_predict_returns_forecast_result() -> None:
    model = DummyForecaster()
    data = pd.DataFrame({"y": [1, 2, 3]})
    
    model.fit(data)
    result = model.predict(horizon=5)
    
    assert isinstance(result, ForecastResult)
    assert result.horizon == 5
    assert result.model_name == "dummy_forecaster"
    assert len(result.predictions) == 5 
    

    