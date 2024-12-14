# To configure database
import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

class project_config:
    # To name the project
    PROJECT_NAME: str = "Institute"
    PROJECT_VERSION: str = "1.0.0"
    BASE_URL: str = os.getenv("BASE_URL")
    
    # To configure database
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
    POSTGRES_DB : str = os.getenv("POSTGRES_DB","tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    MAIL_USERNAME: str = os.getenv("MAILGUN_USERNAME")
    MAIL_PASSWORD = os.getenv("MAILGUN_PASSWORD")
    MAIL_FROM: str = os.getenv("MAILGUN_FROM")
    MAIL_PORT: str = os.getenv("MAILGUN_PORT",587)
    MAIL_SERVER: str = os.getenv("MAILGUN_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAILGUN_MAIL_FROM_NAME")

    TWIL_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID")
    TWIL_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN")
    TWIL_PHONE: str = os.getenv("TWILIO_PHONE")

    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
    STRIPE_SUCCESS_URL = os.getenv("STRIPE_SUCCESS_URL")
    STRIPE_CANCLE_URL = os.getenv("STRIPE_CANCLE_URL")

XpertsTax_config = project_config()