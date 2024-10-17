from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from core.config import XpertsTax_config
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from models import *
from utils.dropdowns import perm
from anyio import Path
import base64

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


# To create JWT Token
def create_access_token(data: dict, EXPIRY=None):
    to_encode = data.copy()
    if EXPIRY:  
        expire = datetime.utcnow() + timedelta(minutes=EXPIRY)
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# To verify JWT Token and retrive user information


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_token(token)


def prepare_auth_data(db, id):
    user = db.query(User).filter(User.id == id).first()
    subscription_end = db.query(User).filter(User.id == user.headOfficeID).first()
    user_basic = db.query(BasicDetails).filter(
        BasicDetails.branchID == user.branchID).first()
    user_permission = db.query(UserPermission).filter(
        UserPermission.user_id == user.id).first()
    return {
        "id": user.id,
        "association": {k: getattr(user, k) for k in ["headOfficeID", "masterID", "branchID", "level"]},
        "permission": {k: getattr(user_permission, k) for k in perm},
        "gstin" : user_basic.gstin,
        "companyName": user_basic.companyName,
        "subscription_end":subscription_end.subscription_end.strftime("%Y-%m-%d") if subscription_end.subscription_end != None else '',
        "email": user.email,
        "mobile": user.mobile,
        "verified": user.verified,
        "created" : user.created.strftime("%Y-%m-%d"),
    }


class Authentication:
    def __init__(self, db, current_user):
        self.db = db
        self.current_user = current_user
        self.branchID = current_user.get('association').get('branchID')

    def convert_image(self,filepath):
        if(filepath != ''):
            binary_fc = open(filepath, 'rb').read()
            base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')

            ext = filepath.split('.')[-1]
            return f'data:image/{ext};base64,{base64_utf8_str}'
        return ''

    async def sendEmail(self, sender, to, client_name, template):
        row = self.db.query(
            EmailSettings.port,
            EmailSettings.domain,
            EmailSettings.settingEmail,
            EmailSettings.settingPassword,
        ).filter(EmailSettings.branchID == self.branchID
        ).first()
        if row and row.settingEmail and row.settingPassword:
            conf = ConnectionConfig(
                MAIL_USERNAME = row.settingEmail or XpertsTax_config.MAIL_USERNAME,
                MAIL_PASSWORD = row.settingPassword or XpertsTax_config.MAIL_PASSWORD,
                MAIL_FROM = row.settingEmail or XpertsTax_config.MAIL_FROM,
                MAIL_PORT = int(row.port) or XpertsTax_config.MAIL_PORT,
                MAIL_SERVER = row.domain or XpertsTax_config.MAIL_SERVER,
                MAIL_FROM_NAME = sender or XpertsTax_config.MAIL_FROM_NAME,
                TEMPLATE_FOLDER=Path(__file__).parent.parent/'templates',
                USE_CREDENTIALS=True,
                VALIDATE_CERTS=True
            )
        else:
            conf = ConnectionConfig(
                MAIL_USERNAME = XpertsTax_config.MAIL_USERNAME,
                MAIL_PASSWORD =  XpertsTax_config.MAIL_PASSWORD,
                MAIL_FROM = XpertsTax_config.MAIL_FROM,
                MAIL_PORT = XpertsTax_config.MAIL_PORT,
                MAIL_SERVER = XpertsTax_config.MAIL_SERVER,
                MAIL_FROM_NAME = XpertsTax_config.MAIL_FROM_NAME,
                TEMPLATE_FOLDER= Path(__file__).parent.parent/'templates',
                USE_CREDENTIALS= True,
                VALIDATE_CERTS= True
            )

        message = MessageSchema(
            subject="Welcome to startup khata",
            recipients=[to],
            template_body={
                "client_name": client_name, "logo": self.convert_image("templates/mailTemplates/images/v2_3.png")
            },
            subtype="html"
        )

        fm = FastMail(conf)
        response = await fm.send_message(message, template_name=template)
        
        return response

    def sendWelcomeMail(self):
        template = "mailTemplates/welcome.html"
        pass

    def sendFeaturesMail(self):
        pass

    def sendEducationMail(self):
        pass

    def sendSocialProofMail(self):
        pass

    def sendTestimonialMail(self):
        pass

    def sendCoundownMail(self):
        pass

    def sendThankyouMail(self):
        pass