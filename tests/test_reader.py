from pathlib import Path 

import pytest
import yaml 

from ts_forecasting_lab.config.reader import load_yaml_config 


def test_load_yaml_config_valid_file(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    
    config_data = {
        "project": {
            "name": "time-series-forecasting-lab",
            "version": "0.1.0",
        },
        "forecast": {
            "horizon": 30, 
            "seasonal_period": 7,
        },
    }
    
    config_path.write_text(
        yaml.safe_dump(config_data),
        encoding="utf-8",
    )
    
    loaded_config = load_yaml_config(config_path)
    
    assert loaded_config == config_data
    assert loaded_config["project"]["name"] == "time-series-forecasting-lab"
    assert loaded_config["forecast"]["horizon"] == 30