from pydantic import BaseModel
from enum import Enum
from datetime import date

class add_fee_head_details(BaseModel):
    feeHeadName: str = None
    
