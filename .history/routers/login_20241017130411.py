from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.session import get_db
from datetime import timedelta
from models import User
from utils.hashing import Hasher
from utils.auth import create_access_token, prepare_auth_data
from datetime import date, timedelta

router = APIRouter(tags=["Login"])


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if request.username.isdigit():
        user = db.query(User).filter(
            User.mobile == int(request.username)).first()
    else:
        user = db.query(User).filter(User.email == request.username.lower()).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User does not exist"
                            )

    if not Hasher.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Incorrect password"
                            )
    if not user.status:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="User Inactive"
                            )
    access_token = create_access_token(
        data=prepare_auth_data(db=db, id=user.id), EXPIRY=60)
    return {"access_token": access_token, "token_type": "bearer"}



