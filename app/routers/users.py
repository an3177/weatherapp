from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import schemas
from .. import database, models, utils, oauth2
from sqlalchemy.orm import Session
from ..oauth2 import create_access_token
from ..utils import password_hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
#prefix="/users"

@router.post("/signup", response_model=schemas.UserOut)
async def create_user(user_data: schemas.UserSignup, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()

    if user:
        raise HTTPException(status_code=409, detail="Email already registered")
    user_data.password = password_hash(user_data.password)
    created_user = models.User(**user_data.model_dump())

    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@router.post("/login", response_model = schemas.Token)
def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm=Depends()):
    found_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not found_user:
        raise HTTPException(status_code=403)
    
    if not utils.verify_password(form_data.password, found_user.password):
        raise HTTPException(status_code=403)
    
    access_token = create_access_token(data={"user_id": found_user.id})

    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/user/{id}")
def delete_user(id:int, db:Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    
    user = user_query.first()

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    