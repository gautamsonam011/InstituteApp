from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String, DateTime, Boolean, Float, Date, Text
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime, date
from sqlalchemy.orm import relationship
from core.session import Base as Basex

class Base(Basex):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

# Create DataTable for User details
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username= Column(String(500), default=None)
    email = Column(String(500), unique=True, default=None)
    mobile = Column(BigInteger, unique=True, default=None)
    password = Column(String(500), default=None)
    headOfficeID = Column(Integer, default=None)
    masterID = Column(Integer, default=None)
    branchID = Column(Integer, default=None)
    level = Column(Integer, default=None)
    status = Column(String(500), default=None)
    verified = Column(Boolean(), default=False)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())
    # otps = relationship("OTP", back_populates= "owner")
    permissions = relationship("UserPermission", back_populates="owner")
  
# Create DataTable for User Permission details
class UserPermission(Base):
    id = Column(Integer, primary_key=True, index=True)
    designation = Column(String(500), default=None)
    professionalManagement = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    updated = Column(DateTime, default=datetime.now())
    owner = relationship("User", back_populates="permissions")

# Create DataTable for OTPs
class OTP(Base):
    id = Column(Integer, primary_key=True, index=True)
    otp_email = Column(Integer, default=123456)
    email_verified = Column(Boolean(), default=False)
    otp_mobile = Column(Integer, default=123456)
    mobile_verified = Column(Boolean(), default=False)
    email_otp_created = Column(DateTime, default=datetime.now())
    mobile_otp_created = Column(DateTime, default=datetime.now())
    othersOTP = Column(String(500), default="")
    user_id = Column(Integer, ForeignKey("user.id"))
    # owner = relationship("User", back_populates= "otps")

# Create DataTable for password reset
class password_reset(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_email_id = Column(String(500), nullable=False, unique=True)
    othersPassReset = Column(String(500), default="")
    otp = Column(Integer)


if date.today().month > 3:
    yr = date.today().year
else:
    yr = date.today().year-1
dt = date(yr, 4, 1)
