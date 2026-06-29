from fastapi import FastAPI
from database import engine, Base
from routers import users, tasks

# Creamos todas las tablas en la base de datos al arrancar
Base.metadata.create_all(bind=engine)

# Creamos la aplicación
app = FastAPI(
    title="Task Manager API",
    description="API para gestionar tareas personales",
    version="1.0.0"
)

# Registramos los routers
app.include_router(users.router)
app.include_router(tasks.router)


# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
def root():
    return {"message": "Task Manager API funcionando 🚀"}