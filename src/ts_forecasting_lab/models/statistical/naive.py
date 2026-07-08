""" 
Naive forecasting models.

These models are simple baselines and are useful for validating 
the forecasting framework before adding more complex models.
"""


from pathlib import Path
from typing import Any

import joblib 
import pandas as pd 

from ts_forecasting_lab.models.base import BaseForecaster, ForecastResult

class SeasonalNaiveForecaster(BaseForecaster):
    """ 
    Seasonal naive forecaster.
    
    Forecasts future values by repeating the most recent seasonal cycle.
    """
    
    def __init__(self, season_length: int) -> None:
        super().__init__(model_name="seasonal_naive")
        
        if season_length <= 0:
            raise ValueError("Season length must be greater than zero.")
        
        self.season_length = season_length
        self.history_: pd.DataFrame | None = None
        
        
    def fit(self, data: pd.DataFrame, **kwargs: Any) -> BaseForecaster:
        """ 
        Store historical data for future seasonal repetition.
        """
        
        if "y" not in data.columns:
            raise ValueError("Input data must contain a 'y' column.")
        
        if len(data) < self.season_length:
            raise ValueError(
                "Input data length must be at least as large as season_length."
            )
            
        self.history_ = data.copy()
        self.is_fitted = True
        
        return self 
    
    def predict(self, horizon: int, **kwargs: Any) -> ForecastResult:
        """ 
        Forecast future values by repeating the last seasonal cycle.
        """
        
        self._check_is_fitted()
        
        if horizon <= 0:
            raise ValueError("Horizon must be greeater than zero.")
        
        assert self.history_ is not None 
        
        last_season = self.history_["y"].tail(self.season_length).to_list()
        
        repeated_values = [
            last_season[i % self.season_length]
            for i in range(horizon)
        ]
        
        predictions = pd.DataFrame(
            {
                "step": range(1, horizon + 1),
                "yhat": repeated_values,
            }
        )
     