from pydantic import BaseModel
from enum import Enum
from datetime import date

class add_fee_head_details(BaseModel):
    feeHeadName: str = None
    
class class_fee_head_details(BaseModel):
    feeHeadName: str = None
    amount: float = None


class fee_submission_details(BaseModel):
    studentNo: str = None
    courseName: str = None
    studentName: str = None
    totalDueAmount: float = None
    paymentMode: str = None
    receiptNo: str = None
    amountToSubmit: float = None    

