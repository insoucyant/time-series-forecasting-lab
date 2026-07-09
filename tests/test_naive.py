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
    model = SeasonalNaiveForecaster(season_length=5)
    
    assert model.model_name == "seasonal_naive"
    assert model.season_length == 5
    assert model.is_fitted is False 
    
def test_seasonal_naive_rejects_invalid_season_length() -> None:
    with pytest.raises(ValueError, match="season_length must be greater than zero"):
        SeasonalNaiveForecaster(season_length=0)
        

def test_seasonal_naive_fit_sets_fitted_state() -> None:
    model = SeasonalNaiveForecaster(season_length=5)
    
    fitted_model = model.fit(sample_training_data())
    
    assert fitted_model is model 
    assert model.is_fitted is True 
    assert model.history_ is not None 
    
def test_seasonal_naive_fit_requires_y_column() -> None:
    model = SeasonalNaiveForecaster(season_length=5)
    data = pd.DataFrame({"value": [1,2,3,4,5]})
    
    with pytest.raises(ValueError, match="must contain a 'y' column"):
        model.fit(data)
        
def test_seasonal_naive_fit_requires_enough_history() -> None: 
    model = SeasonalNaiveForecaster(season_length=7)
    data = pd.DataFrame({"y": [1,2,3]})
    
    with pytest.raises(ValueError, match="at least as large as season_length"):
        model.fit(data)
        
        