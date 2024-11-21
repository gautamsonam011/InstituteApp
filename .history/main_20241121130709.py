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

# Creating app instance
app = FastAPI(title=XpertsTax_config.PROJECT_NAME, version=XpertsTax_config.PROJECT_VERSION)

@app.middleware('http')
async def trakingMiddleware(request: Request, call_next):

    response = await call_next(request)
    db = get_cron_db()

    api_endpoint = request.url.path
    request_method = request.method
    access_token = request.headers.get('authorization')

    if api_endpoint == "/docs" or api_endpoint == "/openapi.json":
        return response 

    decoded_token = {}
    if access_token:
        try:
            decoded_token = decode_token(access_token[7:])
        except Exception as e:
            logging.exception(e)

    user_id = None
    if decoded_token:
        if decoded_token.get('association').get('level') > 1:
            user_id = decoded_token.get('association').get('masterID')
        else:
            user_id = decoded_token.get('id')
   


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
