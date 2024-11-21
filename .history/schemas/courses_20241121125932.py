from pydantic import BaseModel
from enum import Enum
from datetime import date

class courses_details(BaseModel):
    courseName: str = None
    duration : str = None
    description: str = None
