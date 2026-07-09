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
        
def test_seasonal_naive_predict_requires_fit() -> None:
    model = SeasonalNaiveForecaster(season_length=5)
    
    with pytest.raises(RuntimeError, match="must be fitted before prediction"):
        model.predict(horizon=3)
        
def test_seasonal_naive_predict_requires_fit() -> None:
    model = SeasonalNaiveForecaster(season_length=5)
    
    with pytest.raises(RuntimeError, match="must be fitted before prediction"):
        model.predict(horizon=3)
        
def test_seasonal_naive_predict_repeats_last_season() -> None:
    model = SeasonalNaiveForecaster(season_length=5)
    model.fit(sample_training_data())
    
    result = model.predict(horizon=7)
    
    assert isinstance(result, ForecastResult)
    assert result.horizon == 7
    assert result.model_name == "seasonal_naive"
    assert result.predictions["yhat"].tolist() == [20, 21, 22, 23, 24, 20, 21]
    
def test_seasonal_naive_predict_rejects_invalid_horizon() -> None:
    model = SeasonalNaiveForecaster(season_length=5)
    model.fit(sample_training_data())
    
    with pytest.raises(ValueError, match="horizon must be greater than zero"):
        model.predict(horizon=0)
        
def test_seasonal_naive_get_model_info() -> None:
    model = SeasonalNaiveForecaster(season_length=5)
    
    info = model.get_model_info() 
    
    assert info["model_name"] == "seasonal_naive"
    assert info["model_type"] == "baseline"
    assert info["season_length"] == 5
    assert info["supports_exogenous_variables"] is False
    assert info["supports_probabilistic_forecast"] is False 
    
def test_seasonal_naive_save_and_load(tmp_path: Path) -> None:
    model_path = tmp_path / "seasonal_naive.joblib"
    
    model = SeasonalNaiveForecaster(season_length=5)
    model.fit(sample_training_data())
    model.save(model_path)
    
    loaded_model = SeasonalNaiveForecaster.load(model_path)
    
    assert model_path.exists()
    assert isinstance(loaded_model, SeasonalNaiveForecaster)
    assert loaded_model.is_fitted is True 
    assert loaded_model.season_length == 5 
    
    result = loaded_model.predict(horizon=3)
    assert result.predictions["yhat"].tolist() == [20, 21, 22]