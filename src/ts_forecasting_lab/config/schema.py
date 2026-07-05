"""
Configuration schema definitions.

This module defines the typed configuration objects used throughout
the Time Series Forecasting Lab.

A schema should only describe the structure of the configuration.

It should NOT:
- read YAML
- know where the YAML file is
- contain business logic
- initialize models

Its only responsibility is to answer:

"If a valid config.yaml is loaded,
what Python objects should it become?"
"""


from pydantic import BaseModel, Field
from pathlib import Path 

class ProjectConfig(BaseModel):
    """
    Project metadata.
    """
    name: str = Field(..., description="Name of the project.")
    version: str = Field(default="0.1.0", description="Current version of the project")
    description: str = Field(default="", description="Short description of the project.")


class PathsConfig(BaseModel):
    """ 
    Directory paths used throughout the project.
    """
    
class RuntimeConfig(BaseModel):
    """
    

   
    """
    

class DataConfig(BaseModel):
    """
    
    """

class ForecastConfig(BaseModel):
    """ 
    
    """
# 6
class BacktestingConfig(BaseModel):
     """ 
    
    """

# 7
class ModelParametersConfig(BaseModel):
    """ 
    
    """
    

# 8
class ModelConfig(BaseModel):
    """
    
    """   

# 9
class EvaluationConfig(BaseModel):
    """ 
    
    """
    
# 10
class TrackingConfig(BaseModel):
    """ 
    
    """
    
# 11
class Settings(BaseModel):
    """ 
    
    """