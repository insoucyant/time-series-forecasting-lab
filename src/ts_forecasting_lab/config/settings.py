"""
Application Settings.

This module loads the **application configuration** from config.yaml.
Validates it using the Pydantic Schema, and exposes a single validated Settings object for 
use throughout the application.
"""

from pathlib import Path
from ts_forecasting_lab.config.reader import load_yaml_config
from ts_forecasting_lab.config.schema import Settings

def get_settings(config_path: Path | None = None) -> Settings:
    """ 
    Load and Validate Application Settings.
    This becomes the **single entry point** for configuration.
    
    Parameters
    -----------
    config_path
        Optional path to a configuration file.
        If omitted, the default config/config.yaml is used.
        
    Returns
    ---------
    Settings
        A validated Settings object.
    """
    
    if config_path is None:
        config_path = Path("config/config.yaml")
        
    raw_config = load_yaml_config(config_path)
    
    settings = Settings.model_validate(raw_config)
    
    return settings

settings = get_settings() # Global Singleton # Creates one validated -
# - **configuration object** when the module is imported.