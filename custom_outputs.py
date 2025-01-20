from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class ColumnInfo(BaseModel):
    column_name: str
    data_type: str
    is_numeric: bool
    is_boolean: bool
    is_datetime: bool
    min_value: Optional[Union[float, str, datetime]] = None
    max_value: Optional[Union[float, str, datetime]] = None 