import os
import shutil
import pathlib
from fastapi import UploadFile, HTTPException
from datetime import datetime


def uploadCertificatePdf(uploaded_file: UploadFile, folder: str) -> str:

    os.makedirs(f"files/{folder}", mode=0o777, exist_ok=True)
    

    name, exten = os.path.splitext(uploaded_file.filename)
    
    # Validate that the file is a PDF
    if exten.lower() != '.pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
 
    time_stamp = int(datetime.timestamp(datetime.now()))
    file_name = f"certificate_{time_stamp}.pdf"
    
    # Define the destination path for the PDF file
    dest = pathlib.Path(f"files/{folder}/{file_name}")
    
 
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)  
    
    return str(dest)
