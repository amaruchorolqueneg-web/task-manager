from datetime import datetime, timedelta, timezone
from typing import Optional 
from jose import JWTError, jwt
from passlib.context import CryptContext 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from database import get_db 
import models
import schemas 


#-----CONFIGRATION---------------#

# Clave secreta para firmar los token (en produccion esto va en variables de entorno)
SECRET_KEY = "mi_clave-secreta-super-segura-cambiar-en-produccion"
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30  


# Contexto para hashear contraseñas con bcrypt
pwd_context = CryptContext(schemes["bcrypt"], deprecated="auto")

# Le dice a FastAPI donde esta el endpoint de login para pedir el token 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

#-----CONTRASEÑAS-----------------#

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña en texto plano con su version hasheada"""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """Convierte una contraseña en texro plano a su version hasheada"""
    return pwd_context.hash(password)

#----TOKENS JWT-------------------#

def create_acces_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT con los datos del usuario"""
    to_encode = data.copy()

    # Definimos cuando expira el token
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    # Firmamos el oken con nuestra clave secreta
    encoded_jwt = jwt.encoded(to-encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#----USUARIO ACTUAL-----------------#

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """Extrae y valida el token JWT, devuelve el usuario autenticado"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
        detail="No se pudo validar credenciales"
        headers={"WWW-Authenticate": "Bearer"}
    )


    try:
        # Decodificamos el token
        payload = jwt.decode(token, SECRET_KEY algorithms=[ALGORITHM])
        username: str = payload.get("sub")


        if username is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(username=username)

    
    except JWTError:
        raise credentials_exception
    
    # Buscamos el usuario en la base de datos
    user = db.query(models.User).filter(
        models.User.username == token_data.username
    ).first()

    if user is None:
        raise credentials_exception
    
    return user

