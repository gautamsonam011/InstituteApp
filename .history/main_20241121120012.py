from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from core.config import XpertsTax_config
from core.session import engine
from models import Base, User
from sqlalchemy.orm import Session
from core.session import get_cron_db
from routers import registration, login, student
from fastapi.middleware.cors import CORSMiddleware
import fastapi.openapi.utils as fu
import os, time, logging, threading
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from utils.sendOTP import sendScheduleTestEmail
from utils.auth import decode_token
from sqlalchemy.sql import or_


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
        
    # api_usage = db.query(ApiUsageCount
    #     ).filter(ApiUsageCount.user_id == user_id)
    
    # if not api_usage.first() and decoded_token:
    #     association_data = {}
    #     association_data.update(decoded_token.get('association'))
    #     association_data.update({"user_id": decoded_token.get('id')})

    #     row = ApiUsageCount(**association_data)
    #     db.add(row) 
    #     db.flush()
    #     db.commit() 

   



# Including the user API
app.include_router(registration.router)

# Including the login API
app.include_router(login.router)

app.include_router(student.router)

# Mounting assets file path
app.mount("/files", StaticFiles(directory="files"), name="files")
