""" 
Base forecasting interfaces.

This module defines the core abstractions used by all forecasting models.

Every forecasting model in the repository should inherit from BaseForecaster 
and return ForecastResult from predict(). 
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import pandas as pd 
from pydantic import BaseModel, Field


class ForecastResult(BaseModel):
    """ 
        Standard output returned by every Forecasting model.
    """
    
    predictions: pd.DataFrame = Field(
        ...,
        description="Forecasted values in tabular format.",
    )
    
    horizon: int = Field(
        ...,
        gt=0,
        description="Number of future periods forecasted.",
    )
    
    model_name: str = Field(
        ...,
        description="Name of the model that generated the forecast."
    )
    
    frequency: str | None = Field(
        default=None,
        description="Time series frequency, such as D, W, M, or H."
    )
    
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the forecast.",
    )
    
    class Config:
        arbitrary_types_allowed = True
        
    
class BaseForecaster(ABC):
    """ 
    Abstract base class for all forecasting models.
    
    Concrete forecasting models must implement this interface.
    """
    
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.is_fitted = False
        
    @abstractmethod
    def fit(self, data: pd.DataFrame, **kwargs: Any) -> "BaseForecaster":
        """ 
        Fit the forecasting model on historical data.
        """
        
    @abstractmethod
    def predict(self, horizon: int, **kwargs: Any) -> ForecastResult:
        """ 
        Generate forecasts for future time periods.
        """
        
    @abstractmethod
    def save(self, path: Path) -> None:
        """ 
        Save the fitted model to disk.
        """
        
    @classmethod
    @abstractmethod
    def load(cls, path: Path) -> "BaseForecaster":
        """ 
        Load a fitted model from disk.
        """
        
    def get_model_info(self) -> dict[str, Any]:
        """ 
        Return basic model metadata
        """
        
        return {
            "model_name": self.model_name,
            "is_fitted": self.is_fitted,
            "class_name": self.__class__.__name__,
        }
        
    def _check_is_fitted(self) -> None:
        """ 
        Raise an error if the model has not been fitted.
        """
        
        if not self.is_fitted:
            raise RuntimeError(
                f"Model '{self.model_name}' must be fitted before prediction. "
            )

