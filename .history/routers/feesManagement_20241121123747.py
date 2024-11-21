from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.session import get_db
from utils.auth import get_current_user
from schemas.feesManagement import *
from models import *
from typing import List

router = APIRouter(tags=["Fees"], prefix="/fees")

@router.post("/addFeeHead")
async def create_fee_head(
    request: add_fee_head_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Create a new fee head instance
    new_data = FeeHeadDetails(
        feeHeadName = request.feeHeadName,
        status = "Completed",
        user_id=current_user["id"],
        headOfficeID=current_user.get("association").get("headOfficeID"),
        branchID=current_user.get("association").get("branchID"),
        level=current_user.get("association").get("level")
    )

    # Add the new fee head to the database
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {"message":"Fee Head Added Successfully"}

@router.put("/addFeeHead/{fee_id}")
async def update_fee_head(
    fee_id: int,
    request: add_fee_head_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Retrieve the fee head from the database
    fee_heads = db.query(FeeHeadDetails).filter(FeeHeadDetails.id == fee_id
                                                      ).filter(FeeHeadDetails.branchID == current_user.get("association").get("branchID")).first()

    if fee_heads is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update the fee head fields
    fee_heads.feeHeadName = request.feeHeadName
    fee_heads.status = "Edited"
    fee_heads.user_id = current_user.get("id")
    fee_heads.headOfficeID = current_user.get("association").get("headOfficeID")
    fee_heads.branchID = current_user.get("association").get("branchID")
    fee_heads.level = current_user.get("association").get("level")

    # Commit the changes to the database
    db.commit()
    db.refresh(fee_heads)

    return {"message":"Fee Head Edited Successfully"}

@router.get("/addFeeHead/{fee_id}")
async def get_fee_head(
    fee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change student"
                            )
    
    new_data = db.query(FeeHeadDetails).filter(
        FeeHeadDetails.id == fee_id,
        FeeHeadDetails.branchID == current_user.get("association").get("branchID")
        ).first()
    
    return new_data

@router.get("/addFeeHeadAll")
async def get_all_fee_head(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change student"
                            )
    
    new_data = db.query(FeeHeadDetails).filter(
        FeeHeadDetails.branchID == current_user.get("association").get("branchID")
        ).all()
    
    return new_data


@router.delete("/addFeeHead/{fee_id}")
async def delete_fee_head(
    fee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    data = db.query(FeeHeadDetails).filter(
        FeeHeadDetails.id == fee_id,
        FeeHeadDetails.branchID == current_user.get("association").get("branchID")
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail= "Fee Head not found")
   
    db.delete(data)
    db.commit()

    return {"message": "Fee Head deleted successfully"}

@router.delete("/FeeHeadMultiple")
async def delete_fee_head(
    fee_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    data = db.query(FeeHeadDetails
                     ).filter(FeeHeadDetails.id.in_(fee_ids),
                    FeeHeadDetails.branchID == current_user.get("association").get("branchID")
                    ).all()

    if not data:
        raise HTTPException(status_code=404, detail="Student not found")

    for new_data in data:
        db.delete(new_data)
    db.commit()

    return {"message": "Fee Head deleted successfully"}

@router.delete("/addFeeHeadAll")
async def delete_all_fee_head(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    fee_heads = db.query(FeeHeadDetails).filter(
        FeeHeadDetails.branchID == current_user.get("association").get("branchID")
    ).all()

    if not fee_heads:
        raise HTTPException(status_code=404, detail="No Fee Head found for the user's branch")

    for data in fee_heads:
        db.delete(data)
    db.commit()

    return {"message": "All Fee Head deleted successfully"}


# --------------------------- Class Fee Head ---------------- 

@router.post("/classFeeHead")
async def create_class_fee_head(
    request: class_fee_head_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Create a new fee head instance
    new_data = ClassFeeHeadDetails(
        feeHeadName = request.feeHeadName,
        amount = request.amount,
        status = "Completed",
        user_id=current_user["id"],
        headOfficeID=current_user.get("association").get("headOfficeID"),
        branchID=current_user.get("association").get("branchID"),
        level=current_user.get("association").get("level")
    )

    # Add the new fee head to the database
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {"message":"Fee Head Added Successfully"}

@router.put("/classFeeHead/{fee_id}")
async def update_class_fee_head(
    fee_id: int,
    request: class_fee_head_details,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    # Retrieve the fee head from the database
    fee_heads = db.query(ClassFeeHeadDetails).filter(ClassFeeHeadDetails.id == fee_id
                                                      ).filter(ClassFeeHeadDetails.branchID == current_user.get("association").get("branchID")).first()

    if fee_heads is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update the fee head fields
    fee_heads.feeHeadName = request.feeHeadName
    fee_heads.amount = request.amount
    fee_heads.status = "Edited"
    fee_heads.user_id = current_user.get("id")
    fee_heads.headOfficeID = current_user.get("association").get("headOfficeID")
    fee_heads.branchID = current_user.get("association").get("branchID")
    fee_heads.level = current_user.get("association").get("level")

    # Commit the changes to the database
    db.commit()
    db.refresh(fee_heads)

    return {"message":"Fee Head Edited Successfully"}

@router.get("/classFeeHead/{fee_id}")
async def get_class_fee_head(
    fee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change student"
                            )
    
    new_data = db.query(ClassFeeHeadDetails).filter(
        ClassFeeHeadDetails.id == fee_id,
        ClassFeeHeadDetails.branchID == current_user.get("association").get("branchID")
        ).first()
    
    return new_data

@router.get("/classFeeHeadAll")
async def get_all_class_fee_head(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.get("association").get("level") > 1:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to change student"
                            )
    
    new_data = db.query(ClassFeeHeadDetails).filter(
        ClassFeeHeadDetails.branchID == current_user.get("association").get("branchID")
        ).all()
    
    return new_data


@router.delete("/classFeeHead/{fee_id}")
async def delete_class_fee_head(
    fee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.get("association") or not current_user.get("association").get("branchID"):
        raise HTTPException(status_code=403, detail="User association data not found")

    data = db.query(ClassFeeHeadDetails).filter(
        ClassFeeHeadDetails.id == fee_id,
        ClassFeeHeadDetails.branchID == current_user.get("association").get("branchID")
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail= "Fee Head not found")
   
    db.delete(data)
    db.commit()

    return {"message": "Fee Head deleted successfully"}

