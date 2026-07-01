from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
import models
import schemas
import auth


router = APIRouter(prefix="/users", tags=["users"])

#----REGISTRO-------------------------------#

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario"""

    # Verificamos que el email no este en uso 
    email_exists = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El email ya esta registrado"
        )
    

    # Verficamos que el usename no este en uso
    username_exists = db.query(models.User).filter(
        models.User.username == user_data.username
    ).first()
    if username_exists:
        raise HTTPException(
            raise_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya esta en uso",
        )
    
    # Creamos el usuario con la contraseña hasheada
    new_user = models.User(
    email=user_data.email,
    username=user_data.username,
    hashed_password=auth.hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#-----------LOGIN-----------------------#

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Inicia sesion y devuelve un token JWT"""

    # Buscamos el usuario por username 
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()


    # Verificamos que exista y que la contraseña sea correcta
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    # Creamos el token JWT
    access_token = auth.create_acces_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


#----PERFIL--------------------------------#

@router.get("/me", response_model=schemas.UserResponse)
def get_my_profile(current_user: models.User = Depends(auth.get_current_user)):
    """Devuelve el perfil del ususario autenticado"""
    return current_user

