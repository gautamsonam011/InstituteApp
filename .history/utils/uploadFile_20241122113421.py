import os
import shutil
import pathlib
from fastapi import UploadFile, HTTPException
from datetime import datetime

# Function to handle PDF file uploads (like E-waybill PDFs)
def uploadEwaybillPdf(uploaded_file: UploadFile, folder: str) -> str:
    # Ensure the folder exists
    os.makedirs(f"files/{folder}", mode=0o777, exist_ok=True)
    
    # Extract the file name and extension
    name, exten = os.path.splitext(uploaded_file.filename)
    
    # Validate that the file is a PDF
    if exten.lower() != '.pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    # Define a unique name for the e-waybill PDF using a timestamp
    time_stamp = int(datetime.timestamp(datetime.now()))
    file_name = f"ewaybill_{time_stamp}.pdf"
    
    # Define the destination path for the PDF file
    dest = pathlib.Path(f"files/{folder}/{file_name}")
    
    # Read the content of the uploaded file and save it to the destination
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)  # This copies the content of the file to the destination
    
    return str(dest)
