"""
In code writing, I wrote first config.yaml, next schema.py. Now Iam writing reader.py and teh comments.
So, now I have config.yaml and schma.py. But nothing connects them.
Eventually, we want:
    settings = get_settings()
Internally that will be:
config.yaml --> reader.py --> dictionary --> schema.py --> Settings object --> Entire Application

What should reader.py do?
W=Exactly **one thing**: Given a Path, return Python Dictionary.
Nothing else. It should NOT:
1. know about forecasting
2. know about Pydantic
3. know about Models
4. Know about Paths
5. Know about Settings
Its job is simple: YAML --> dict.

The architecture after reader.py:
config.yaml --> load_yaml_config() --> Python dict --> Settings.model_validate(...) --> 
--> Settings Object --> Application
Notice how above each step has exactly one responsibility:
---------------------------------------------------------------------------------------------
|Stage1| config.yaml        | Store Configuration  | doesn't know Python/Pydantic/ |
|      |                    |                      | /application                  |
---------------------------------------------------------------------------------------------
|Stage2| load_yaml_config() | Read a YAML file and | does NOT validate/check miss- |
|      |                    | convert it into a    | -ing fileds/create Settings/  |
|      |                    | Python dictionary    | does NOT know forecast        |
---------------------------------------------------------------------------------------------
|Stage3| Python Dictionary  | YAML - Python        |                               |
---------------------------------------------------------------------------------------------
|Stage4| Settings.model_va- | Pydantic enters here |                               |
|      | lidate(...      )  | Converts untrusted d-|                               |
-ictionary into  a trusted Settings object. This is validation. It checks:
* Is horizon present?
* Is horizon and integer?
* Is iy positive?
* is paths.logs_dir actually a Path?
* Is model.name present?
* Are defaults applied?
If anything is wrong it immedaitely raises an error. Without Pydantic your application might fail 
30 minutes later. With Pydantic it fails immediately. 
This is one of the biggest reasons production systems use schemas.
---------------------------------------------------------------------------------------------
|Stage5| Settings object  |           |                               |
---------------------------------------------------------------------------------------------


---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------
|Component                |                          Responsibility                         |
---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------
|config.yaml              | Stores Configuration Values.                                    |
---------------------------------------------------------------------------------------------
|load_yaml_config()       | Reads yaml from disk and converts it into a Python dictionary.  |
---------------------------------------------------------------------------------------------
|Python dict              | Temporary, unvalidated representation of the configuration.     |
---------------------------------------------------------------------------------------------
|Settings.model_validate()| Validates the dictionary and converts it into typed configurat- |
|                         | ion object                                                      |
---------------------------------------------------------------------------------------------
|Settings object          | The final, trusted, strongly typed configuration used througho- |
|                         | -ut the application.                                            |
---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------|


After reader.py, we will write settings.py. Its responsbility will be:
locate config.yaml --> Call reader.py --> Call schema.py --> Return validated Settings object.    

That means the rest of the repository only writes:
from ts_forecasting_lab.config.settings import settings
print(settings.forecast.horizon)
and rest of the repository never worries about YAML or validation.
"""