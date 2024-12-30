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
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5433
    POSTGRES_DB : str = os.getenv("POSTGRES_DB","institute_db")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

XpertsTax_config = project_config()