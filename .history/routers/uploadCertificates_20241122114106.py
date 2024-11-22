from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from core.session import get_db
from utils.auth import get_current_user
from models import *
from typing import List
from utils.uploadFile import uploadCertificatePdf

router = APIRouter(tags=["uploadCertificates"], prefix="/certificates")

@router.post("/certificates")
async def create_certificates(
    studentNo: str,
    certificate: UploadFile = File(None),  
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")


    # # Process the uploaded image if provided
    if certificate:
        # Save the image to a folder or perform any required processing
        file_path = uploadCertificatePdf(certificate, "Certificates")
    else:
        file_path = None
 

    # Create a new upload certificate instance

    new_certificate = UploadCertificateDetails(
        studentNo = studentNo,
        certificate = file_path,
        status="Completed",
        user_id=current_user["id"],
        headOfficeID=current_user.get("association").get("headOfficeID"),
        branchID=current_user.get("association").get("branchID"),
        level=current_user.get("association").get("level")
    )
   
    db.add(new_certificate)
    db.commit()
   

    return {"message": "Upload certificate created successfully"}


@router.put("certificatesUpdate")
async def certificates_update(
    ID: int,
    studentNo: str,
    certificate: UploadFile = File(None), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # # Process the uploaded image if provided
    if certificate:
        # Save the image to a folder or perform any required processing
        file_path = uploadCertificatePdf(certificate, "Certificates")
    else:
        file_path = None
    

    # Get the existing upload by ID
    existing_upload = db.query(UploadCertificateDetails).filter(UploadCertificateDetails.id == ID,
                                                                UploadCertificateDetails.branchID == current_user.get("association").get("branchID")).first()

    if not existing_upload:
        raise HTTPException(status_code=404, detail="Certificate not found")

    # Update the upload certificate data

    existing_upload.studentNo = studentNo
    existing_upload.certificate = file_path
    existing_upload.status = "Edited"  # Assuming status can be updated
    existing_upload.user_id = current_user["id"]
    existing_upload.headOfficeID = current_user.get("association").get("headOfficeID")
    existing_upload.branchID = current_user.get("association").get("branchID")
    existing_upload.level = 1

    db.commit()

    return {"message": "Certificate updated successfully"}


@router.get("/certificate/{ID}")
async def get_certificate(
    StudentNo: str,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
    ):

    # if current_user.get("association").get("level") > 1:
    #     raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    #                         detail="You are not allowed to change Review details"
    #                         )
    
    new_data = db.query(UploadCertificateDetails).filter(
        UploadCertificateDetails.studentNo == StudentNo,
        # UploadCertificateDetails.branchID == current_user.get("association").get("branchID")
        ).first()
    
    return new_data

@router.get("/certificateAll")
async def get_all_certificate(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change Review details"
                            )
    
    new_data = db.query(UploadCertificateDetails).filter(
        UploadCertificateDetails.branchID == current_user.get("association").get("branchID")
        ).all()
    
    return new_data


@router.delete("/certificate/{ID}")
async def delete_certificate(
    ID: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    sale = db.query(UploadCertificateDetails).filter(
        UploadCertificateDetails.id == ID,
        UploadCertificateDetails.branchID == current_user.get("association").get("branchID")
    ).first()

    if not sale:
        raise HTTPException(status_code=404, detail= "Certificate not found")
   
    db.delete(sale)
    db.commit()

    return {"message": "Certificate deleted successfully"}


  