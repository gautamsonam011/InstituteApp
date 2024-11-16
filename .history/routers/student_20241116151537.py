from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.session import get_db
from utils.auth import get_current_user
from schemas.student import *
from models import *
from typing import List

router = APIRouter(tags=["BookAppointment"], prefix="/appointment")

@router.post("/appointment")
async def create_appointment(
    request: book_appointment_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Create a new book appointment instance
    new_data = BookAppointmentDetails(
        patientName = request.patientName,
        disease = request.disease,
        age = request.age,
        mobileNo = request.mobileNo,
        create_date = request.create_date,
        status = "Completed",
        user_id=current_user["id"],
        headOfficeID=current_user.get("association").get("headOfficeID"),
        branchID=current_user.get("association").get("branchID"),
        level=current_user.get("association").get("level")
    )

    # Add the new Book Appointment to the database
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {"message":"Book Appointment Added Successfully"}

@router.put("/appointment/{book_id}")
async def update_book_appointment(
    book_id: int,
    request: book_appointment_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Retrieve the Book Appointment from the database
    existing_book = db.query(BookAppointmentDetails).filter(BookAppointmentDetails.id == book_id).first()

    if existing_book is None:
        raise HTTPException(status_code=404, detail="Paitent not found")

    # Update the Patient fields
    existing_book.patientName = request.patientName
    existing_book.disease = request.disease
    existing_book.age = request.age
    existing_book.mobileNo = request.mobileNo
    existing_book.create_date = request.create_date
    existing_book.user_id = current_user.get("id")
    existing_book.headOfficeID = current_user.get("association").get("headOfficeID")
    existing_book.branchID = current_user.get("association").get("branchID")
    existing_book.level = current_user.get("association").get("level")

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_book)

    return {"message":"Patient Edited Successfully"}

@router.get("/appointment/{book_id}")
async def get_appointment(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change appointment details"
                            )
    
    new_data = db.query(BookAppointmentDetails).filter(
        BookAppointmentDetails.id == book_id,
        BookAppointmentDetails.branchID == current_user.get("association").get("branchID")
        ).first()
    
    return new_data

@router.get("/appointmentAll")
async def get_all_appointment(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change Patient details"
                            )
    
    new_data = db.query(BookAppointmentDetails).filter(
        BookAppointmentDetails.branchID == current_user.get("association").get("branchID")
        ).all()
    
    return new_data


@router.delete("/appointment/{book_id}")
async def delete_appointment(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    data = db.query(BookAppointmentDetails).filter(
        BookAppointmentDetails.id == book_id,
        BookAppointmentDetails.branchID == current_user.get("association").get("branchID")
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail= "Patient not found")
   
    db.delete(data)
    db.commit()

    return {"message": "Patient deleted successfully"}

@router.delete("/appointmentMultiple")
async def delete_appointment(
    book_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    data = db.query(BookAppointmentDetails
                     ).filter(BookAppointmentDetails.id.in_(book_ids),
                    BookAppointmentDetails.branchID == current_user.get("association").get("branchID")
                    ).all()

    if not data:
        raise HTTPException(status_code=404, detail="Patient not found")

    for new_data in data:
        db.delete(new_data)
    db.commit()

    return {"message": "Patient deleted successfully"}

@router.delete("/appointmentAll")
async def delete_all_appointment(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    appointments = db.query(BookAppointmentDetails).filter(
        BookAppointmentDetails.branchID == current_user.get("association").get("branchID")
    ).all()

    if not appointments:
        raise HTTPException(status_code=404, detail="No Patient found for the user's branch")

    for data in appointments:
        db.delete(data)
    db.commit()

    return {"message": "All Patient deleted successfully"}