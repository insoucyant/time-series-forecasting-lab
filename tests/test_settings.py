from pathlib import Path

from ts_forecasting_lab.config.schema import Settings
from ts_forecasting_lab.config.settings import get_settings

def test_get_settings_loads_valid_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    
    config_path.write_text(
        """ 
project: 
    name: time-series-forecasting-lab
    version: 0.1.0
    description: Production time series forecasting lab
    
paths:
    data_dir: data
    raw_data_dir: data/raw
    processed_data_dir: data/processed
    reports_dir: reports
    plots_dir: reports/figures
    models_dir: artifacts/models
    logs_dir: logs
    
runtime:
    environment: local
    random_seed: 42
    log_level: "INFO"
    
data:
    dataset_name: sample_retail_demand
    target_column: y
    time_column: ds
    id_column: unique_id
    frequency: D
    
forecast: 
    horizon: 30
    validation_size: 30
    test_size: 30
    seasonal_period: 7
    
backtesting:
    n_splits: 3
    initial_train_size: 180
    step_size: 30
    expanding_window: true
    
model:
    name: seasonal_naive
    category: baseline
    params:
        seasonal_length: 7
        
evaluation:
    metrics:
        - mae
        - rmse
        - mape
        - smape
        - mase
        
tracking:
    enabled: false
    experiment_name: ts_forecasting_lab
    tracking_uri: mlruns
    """,
            encoding="utf-8",
    )
    
    settings = get_settings(config_path)

    assert isinstance(settings, Settings)
    assert settings.project.name == "time-series-forecasting-lab"
    assert settings.forecast.horizon == 30
    assert settings.model.name == "seasonal_naive"
    assert settings.model.params.seasonal_length == 7
    assert settings.tracking.enabled is False
    
    
    
    
# </> Bash
# pytest tests/test_settings.py
# Expected
# 1 passed