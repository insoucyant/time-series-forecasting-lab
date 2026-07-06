import pytest 
from pydantic import ValidationError

from ts_forecasting_lab.config.schema import Settings

def valid_config() -> dict:
    return {
        "project": {
            "name": "time-series-forecasting-lab",
            "version": "0.1.0",
            "description": "Production kind generic time series forecasting lab",
        },
        "paths": {
            "data_dir": "data",
            "raw_data_dir": "data/raw",
            "processed_data_dir": "data/processed",
            "reports_dir": "reports",
            "plots_dir": "reports/figures",
            "models_dir": "artifacts/models",
            "logs_dir": "logs",
        },
        "runtime":{
            "environment": "local",
            "random_seed": 42,
            "log_level": "INFO"
        },
        "data":{
            
        },
        "forecast":{
            
        },
        "backtesting":{
            
        },
        "model":{
            
        },
        "evaluation":{
            
        },
        "tracking":{
            
        },
    }