from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



#---------Usuarios------------------------------

class UserCreate(BaseModel):
    """Datos que necesitamos para registrar a un usuario"""
    email: EmailStr
    username: str
    password: str



class UserResponse(BaseModel):
    """Datos del usuario que devolvemos en la API (sin la contraseña)"""
    id: int
    email:  str
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True 

#-------AUTENTICACION------------------------------

class Token(BaseModel):
    """Lo que devolvemos cuando el usuario inicia sesion"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Datos que guardamos dentro del token JWT"""
    username: Optional[str] = None

#-------TAREAS------------------------------

class TaskCreate(BaseModel):
    """Datos para crear una tarea"""
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    """Datos para actualizar una tarea (todos opcionales)"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Datos de la tarea que devolvemos en la API"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


