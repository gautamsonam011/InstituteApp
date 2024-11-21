import os
import shutil
import pathlib
from fastapi import UploadFile, HTTPException
from datetime import datetime

# Function to handle generic file upload
def uploadFile(uploaded_file: UploadFile, folder: str) -> str:
    # Ensure that the folder exists
    os.makedirs(f"files/{folder}", mode=0o777, exist_ok=True)
    
    # Extract file name and extension
    name, exten = os.path.splitext(uploaded_file.filename)
    time_stamp = int(datetime.timestamp(datetime.now()))
    file_name = f"{name}_{time_stamp}" + exten
    
    # Default to '.mp4' if the extension is empty or invalid
    if exten not in ['.mp4', '.avi', '.mkv', '.mov', '.webm']:
        raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")
    
    # Define the destination path for the uploaded video file
    dest = f"files/{folder}/{file_name}"
    
    # Write the file to the destination
    with open(pathlib.Path(dest), "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    
    return dest

# Function to handle PDF file uploads (like E-waybill PDFs)
def uploadEwaybillPdf(uploaded_file: UploadFile, folder: str) -> str:
    os.makedirs(f"files/{folder}", mode=0o777, exist_ok=True)
    
    # Define a unique name for the e-waybill PDF
    time_stamp = int(datetime.timestamp(datetime.now()))
    file_name = f"ewaybill_{time_stamp}.pdf"
    dest = pathlib.Path(f"files/{folder}/{file_name}")
    
    # Save the PDF file
    dest.write_bytes(uploaded_file.content)
    
    return str(dest)

# A utility function to save uploaded files with validation (for video files)
def save_uploaded_file(upload_file: UploadFile) -> str:
    # Define allowed video file extensions
    allowed_video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.webm']
    
    # Check the file extension
    name, exten = os.path.splitext(upload_file.filename)
    
    if exten not in allowed_video_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")
    
    # Define the directory to save the uploaded files
    upload_dir = pathlib.Path("files/videos")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a unique file name with a timestamp to avoid overwriting
    time_stamp = int(datetime.timestamp(datetime.now()))
    file_name = f"{name}_{time_stamp}{exten}"
    file_path = upload_dir / file_name
    
    # Save the video file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return str(file_path)