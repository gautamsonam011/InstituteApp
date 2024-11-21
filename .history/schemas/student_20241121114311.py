from pydantic import BaseModel
from enum import Enum
from datetime import date

class student_details(BaseModel):
    studentNo: str = None
    year : str = None
    admissionDate : date = None
    course: str = None
    firstName: str = None
    lastName: str = None
    gender: str = None
    date_of_birth: date = None
    email: str = None
    mobile: str = None
    address: str = None
