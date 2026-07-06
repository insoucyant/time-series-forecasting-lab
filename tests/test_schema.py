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
            "dataset_name": "sample_retail_demand",
            "target_column": "y",
            "time_column": "ds",
            "id_column": "unique_id",
            "frequency": "D",
        },
        "forecast":{
            "horizon": 30,
            "validation_size": 30,
            "test_size": 30,
            "seasonal_period": 7
        },
        "backtesting":{
            "n_splits": 3,
            "initial_train_size": 180,
            "step_size": 30,
            "expanding_window": True,
        },
        "model":{
            "name": "seasonal_naive",
            "category": "baseline",
            "params": {
                "seasonal_length": 7,
            },
        },
        "evaluation":{
            "metrics": ["mae", "rmse", "mape", "smape", "mase"]
        },
        "tracking":{
            "enabled": False,
            "experiment_name": "ts_forecasting_lab",
            "tracking_uri": "mlruns"
        },
    }