from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from twilio.rest import Client
from random import randint
from core.config import XpertsTax_config
from datetime import date

def otp_generator():
    return(randint(100000,1000000))

conf = ConnectionConfig(
    MAIL_USERNAME = XpertsTax_config.MAIL_USERNAME,
    MAIL_PASSWORD = XpertsTax_config.MAIL_PASSWORD,
    MAIL_FROM = XpertsTax_config.MAIL_FROM,
    MAIL_PORT = 587,
    MAIL_SERVER = XpertsTax_config.MAIL_SERVER,
    MAIL_FROM_NAME=XpertsTax_config.MAIL_FROM_NAME,
    # MAIL_STARTTLS = False,
    # MAIL_SSL_TLS = True,
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

def sendOTPemail(otp,email_id,mess, background_tasks):
    # pass
    message = MessageSchema(
        subject="OTP for email verification",
        recipients=[email_id],  # List of recipients, as many as you can pass 
        body=f"Welcome to STARTUP KHATA.\nOTP for {mess} is {otp}"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message,message)

def sendConfirmInfo(password, email_id, mess, background_tasks):
    # pass
    message = MessageSchema(
        subject="Password changed",
        recipients=[email_id],
        body=f"Your password has been changed. \n{mess} {password}"
    )
    
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

def sendQuote(name, email, mobile, message, background_tasks):
    # pass
    message = MessageSchema(
        subject="New Quote",
        recipients = ["info@startupkhata.com"],
        body = f"You have new Quote.\n\n{message} \n\nCustomer Name: {name} \nEmail Address: {email}\nContact No.: {mobile}"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

def sendRegistrationMail(email, mobile, background_tasks):
    # pass
    message = MessageSchema(
        subject="New Registration",
        recipients = ["info@startupkhata.com"],
        body = f"You have new Registration.\n\nEmail Address: {email}\nContact No.: {mobile}"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

def sendPaymentSucess(email, mobile, background_tasks):
    # pass
    message = MessageSchema(
        subject="New Payment",
        recipients = ["info@startupkhata.com"],
        body = f"You have new Payment.\n\nEmail Address: {email}\nContact No.: {mobile}"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

def sendOTPmobile(otp,mobile, mess, background_tasks):
    # pass
    def send():
        client = Client(XpertsTax_config.TWIL_ACCOUNT_SID,XpertsTax_config.TWIL_AUTH_TOKEN)
        client.messages.create(
            body=f"Welcom to STARTUP KHATA.\nYour OTP for {mess} is {otp}",
            from_= XpertsTax_config.TWIL_PHONE,
            to = "+91"+str(mobile)
        )
    background_tasks.add_task(send)

async def sendTestEmail(email, mobile):
    message = MessageSchema(
        subject="New Registration",
        recipients = [email],
        body = f"You have new Registration.\n\nEmail Address: {email}\nContact No.: {mobile}"
    )
    fm = FastMail(conf)
    await fm.send_message(message)


def sendScheduleTestEmail(email):
    message = MessageSchema(
        subject="Greetings",
        recipients = [email],
        body = f"Good morning ajit. today date is {date.today()}"
    )
    fm = FastMail(conf)
    fm.send_message(message)