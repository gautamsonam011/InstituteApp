from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from core.session import get_db
from schemas.users import UserCreate, pass_reset
from models import User, password_reset, UserPermission
from utils.hashing import Hasher
from utils.auth import get_current_user, prepare_auth_data
from utils.sendOTP import sendOTPemail, sendOTPmobile, otp_generator, sendConfirmInfo, sendRegistrationMail
from utils.auth import create_access_token


router = APIRouter(tags=["Users"])

# Store entry into the database
@router.post("/register", status_code=status.HTTP_201_CREATED)
def registration(
    request: UserCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)):
    print(request)

    user_email_check = db.query(User).filter(User.email == request.email.lower())
    if user_email_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the Email ID: {request.email} already exists"
        )
    
    user_mobile_check = db.query(User).filter(User.mobile == request.mobile)
    if user_mobile_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the Mobile No.: {request.mobile} already exists"
        )
    
    user = User(
        email=request.email.lower(),
        mobile=request.mobile,
        status="Trial user",
        password=Hasher.get_password_hash(request.password),
        # branchName="Head Office"
    )

    db.add(user)
    db.flush()
    userID = user.id
    db.query(User
    ).filter(User.id == userID
    ).update({
        "headOfficeID": userID,
        "masterID": userID,
        "branchID": userID,
        "level": 1
    })
   

    user_permission = UserPermission(
        user_id=userID
    )
    db.add(user_permission)
    db.commit()
    db.refresh(user_permission)

    sendRegistrationMail(request.email, request.mobile, background_tasks)

    access_token = create_access_token(data = prepare_auth_data(db=db, id=user.id), EXPIRY=60)

    return {"message": "User Created Successfully!!!", "access_token": access_token, "token_type": "bearer"}

# Get user detail
@router.get("/get-curruser", status_code=status.HTTP_200_OK)
def get_curr_user(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):

    user = db.query(User
        ).filter(User.id == current_user.get("id")
        ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exists"
        )
    
    access_token = create_access_token(
        data=prepare_auth_data(db=db, id=user.id), EXPIRY=60)

    return {"access_token": access_token, "token_type": "bearer"}


# Forget password
@router.post("/forget", status_code=status.HTTP_200_OK)
def forgetPassword(
    inp: str, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)):

    if "@" in inp:
        user = db.query(User).filter(User.email == inp.lower()).first()
    else:
        user = db.query(User).filter(User.mobile == int(inp)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User does not exist"
        )

    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User Inactive"
        )

    # Send OTP on email as well as mobile
    otp = otp_generator()
    mess = "Password reset"
    sendOTPemail(otp, user.email, mess, background_tasks)
    sendOTPmobile(otp, user.mobile, mess, background_tasks)

    row = db.query(password_reset)\
        .filter(password_reset.user_email_id == inp.lower())

    if not row.first():
        userData = password_reset(
            user_email_id=user.email,
            otp=otp
        )
        db.add(userData)
    else:
        row.update({
            password_reset.user_email_id: user.email,
            password_reset.otp: otp
        })

    db.commit()

    return{"message": "OTP has been sent to change password"}


@router.get("/getEmail")
def getMail(db: Session = Depends(get_db)):

    row = db.query(password_reset).first()

    return{"message": row.user_email_id}


@router.put("/changePass", status_code=status.HTTP_200_OK)
def changePassword(
    request: pass_reset, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)):

    user = db.query(password_reset).filter(password_reset.user_email_id == request.email.lower())

    if user.first().otp != request.otp:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Incorrect OTP"
        )

    mess = "Your New Password is"
    sendConfirmInfo(request.password, request.email, mess, background_tasks)

    users = db.query(User).filter(User.email == request.email.lower())

    users.update({"password": Hasher.get_password_hash(request.password)})
    user.update({"othersPassReset": Hasher.get_password_hash(request.password)})

    db.commit()

    return {"message": "Password updated succesfully"}