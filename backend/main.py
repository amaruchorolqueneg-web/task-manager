from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import users, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="API para gestionar tareas personales",
    version="1.0.0"
)

# Habilitamos CORS para que el fronted pueda cominicarse con la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)


app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Manager API funcionando"}


