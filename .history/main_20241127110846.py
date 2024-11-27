from fastapi import FastAPI, Request
from core.config import XpertsTax_config
from core.session import engine
from models import Base
from core.session import get_cron_db
from routers import registration, login, student, feesManagement, courses, uploadCertificates
import fastapi.openapi.utils as fu
import os, logging
from fastapi.staticfiles import StaticFiles
from utils.auth import decode_token
from fastapi.middleware.cors import CORSMiddleware


os.makedirs("files", exist_ok=True)
logging.basicConfig(filename="salepdf.txt", format="%(asctime)s - %(message)s", level=logging.DEBUG)


fu.validation_error_response_definition = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "error": {"title": "Message", "type": "string"},
    },
}

# Creating database
Base.metadata.create_all(bind=engine)

# # Creating app instance
app = FastAPI(title=XpertsTax_config.PROJECT_NAME, version=XpertsTax_config.PROJECT_VERSION)

# Including the user API
app.include_router(registration.router)

# Including the login API
app.include_router(login.router)

app.include_router(student.router)

app.include_router(feesManagement.router)

app.include_router(courses.router)

app.include_router(uploadCertificates.router)



# Mounting assets file path
app.mount("/files", StaticFiles(directory="files"), name="files")

app.add_middleware(
    CORSMiddleware,
    allow_orgins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)