from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.session import get_db
from utils.auth import get_current_user
from schemas.student import *
from models import *
from typing import List

router = APIRouter(tags=["Student"], prefix="/student")

@router.post("/student")
async def create_student(
    request: student_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Create a new student instance
    new_data = StudentDetails(
        studentNo = request.studentNo,
        year = request.year,
        admissionDate = request.admissionDate,
        course = request.course,
        firstName = request.firstName,
        lastName = request.lastName,
        gender = request.gender,
        date_of_birth = request.date_of_birth,
        email = request.email,
        mobile = request.mobile,
        address = request.address,
        status = "Completed",
        user_id=current_user["id"],
        headOfficeID=current_user.get("association").get("headOfficeID"),
        branchID=current_user.get("association").get("branchID"),
        level=current_user.get("association").get("level")
    )

    # Add the new student to the database
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {"message":"Student Added Successfully"}

@router.put("/student/{student_id}")
async def update_student(
    student_id: int,
    request: student_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Retrieve the Student from the database
    existing_student = db.query(StudentDetails).filter(StudentDetails.id == student_id
                                                      ).filter(StudentDetails.branchID == current_user.get("association").get("branchID")).first()

    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update the Student fields
    existing_student.studentNo = request.studentNo
    existing_student.year = request.year
    existing_student.admissionDate = request.admissionDate
    existing_student.course = request.course
    existing_student.firstName = request.firstName
    existing_student.lastName = request.lastName
    existing_student.date_of_birth = request.date_of_birth
    existing_student.gender = request.gender
    existing_student.email = request.email
    existing_student.mobile = request.mobile
    existing_student.address = request.address
    existing_student.status = "Edited",
    existing_student.user_id = current_user.get("id")
    existing_student.headOfficeID = current_user.get("association").get("headOfficeID")
    existing_student.branchID = current_user.get("association").get("branchID")
    existing_student.level = current_user.get("association").get("level")

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_student)

    return {"message":"Student Edited Successfully"}

@router.get("/student/{student_id}")
async def get_student (
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change student"
                            )
    
    new_data = db.query(StudentDetails).filter(
        StudentDetails.id == student_id,
        StudentDetails.branchID == current_user.get("association").get("branchID")
        ).first()
    
    return new_data

@router.get("/astudentAll")
async def get_all_student(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change student"
                            )
    
    new_data = db.query(StudentDetails).filter(
        StudentDetails.branchID == current_user.get("association").get("branchID")
        ).all()
    
    return new_data


@router.delete("/student/{student_id}")
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    data = db.query(StudentDetails).filter(
        StudentDetails.id == student_id,
        StudentDetails.branchID == current_user.get("association").get("branchID")
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail= "Student not found")
   
    db.delete(data)
    db.commit()

    return {"message": "Student deleted successfully"}

@router.delete("/studentMultiple")
async def delete_student(
    fee_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    data = db.query(StudentDetails
                     ).filter(StudentDetails.id.in_(fee_ids),
                    StudentDetails.branchID == current_user.get("association").get("branchID")
                    ).all()

    if not data:
        raise HTTPException(status_code=404, detail="Student not found")

    for new_data in data:
        db.delete(new_data)
    db.commit()

    return {"message": "Student deleted successfully"}

@router.delete("/studentAll")
async def delete_all_student(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    students = db.query(StudentDetails).filter(
        StudentDetails.branchID == current_user.get("association").get("branchID")
    ).all()

    if not students:
        raise HTTPException(status_code=404, detail="No Student found for the user's branch")

    for data in students:
        db.delete(data)
    db.commit()

    return {"message": "All Student deleted successfully"}