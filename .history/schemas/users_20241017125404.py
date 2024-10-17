from pydantic import BaseModel,EmailStr, validator

class OTP_Verification(BaseModel):
    email: EmailStr = None
    mobile: int = None
    reason: str = None

# properties required during user creation
class UserCreate(BaseModel):
    email : EmailStr
    mobile: int
    password : str
    otpVerify: bool
    username: str
    emailOtp: int
    mobileOtp: int = None

class pass_reset(BaseModel):
    email: EmailStr
    otp : int
    password: str
