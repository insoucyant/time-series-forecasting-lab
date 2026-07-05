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
    

def test_load_yaml_config_missing_file(tmp_path: Path) -> None:
    missing_config_path = tmp_path / "missing_config.yaml"
    
    with pytest.raises(FileNotFoundError):
        load_yaml_config(missing_config_path)
        
def test_load_yaml_config_empty_file(tmp_path: Path) -> None: 
    config_path  = tmp_path / "empty_config.yaml"
    config_path.write_text("", encoding="utf-8")
    
    with pytest.raises(ValueError, match="Configuration file is empty"):
        load_yaml_config(config_path)
    
    
def test_load_yaml_config_non_mapping_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "list_config.yaml"
    config_path.write_text(
        "- item1\n- item2\n",
        encoding="utf-8",
    )
    
    with pytest.raises(ValueError, match="must contain a YAML mapping"):
        load_yaml_config(config_path)
        
        
# Run in Bash:
# -- pytest tests/test_reader.py

# Expected Output
# -- 4 passed

# We have verified that reader.py behaves correctly in 4 scenarios:
# 1. Valid YAML: Correctly reads a valid YAML file.
# 2. Missing file: Raises ==FileNotFoundError==
# 3. Empty File: Raises ==ValueError+ for an empty configuration
# 4. Invalid top-level YAML: Rejects a YAML list instead of a mapping/dictionary 
# We did not just test the happy path. We also tested failure modes.