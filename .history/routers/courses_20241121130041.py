from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.session import get_db
from utils.auth import get_current_user
from schemas.courses import *
from models import *
from typing import List

router = APIRouter(tags=["Courses"], prefix="/courses")

@router.post("/courses")
async def create_courses(
    request: courses_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Create a new courses instance
    new_data = CourseDetails(
        courseName = request.courseName,
        duration = request.duration,
        description = request.description,
        status = "Completed",
        user_id=current_user["id"],
        headOfficeID=current_user.get("association").get("headOfficeID"),
        branchID=current_user.get("association").get("branchID"),
        level=current_user.get("association").get("level")
    )

    # Add the new courses to the database
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {"message":"Course Added Successfully"}

@router.put("/courses/{course_id}")
async def update_courses(
    course_id: int,
    request: courses_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Retrieve the courses from the database
    existing_student = db.query(CourseDetails).filter(CourseDetails.id == course_id
                                                      ).filter(CourseDetails.branchID == current_user.get("association").get("branchID")).first()

    if existing_student is None:
        raise HTTPException(status_code=404, detail="Course not found")

    # Update the course fields
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

    return {"message":"Course Edited Successfully"}

@router.get("/courses/{course_id}")
async def get_courses (
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change student"
                            )
    
    new_data = db.query(CourseDetails).filter(
        CourseDetails.id == course_id,
        CourseDetails.branchID == current_user.get("association").get("branchID")
        ).first()
    
    return new_data

@router.get("/courseAll")
async def get_all_course(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change course"
                            )
    
    new_data = db.query(CourseDetails).filter(
        CourseDetails.branchID == current_user.get("association").get("branchID")
        ).all()
    
    return new_data


@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    data = db.query(CourseDetails).filter(
        CourseDetails.id == course_id,
        CourseDetails.branchID == current_user.get("association").get("branchID")
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail= "Course not found")
   
    db.delete(data)
    db.commit()

    return {"message": "Course deleted successfully"}

