from pydantic import BaseModel
from enum import Enum
from datetime import date

class student_detailss(BaseModel):
    studentNo: str = None
    year : str = None
    admissionDate : str = None
    course: str = None