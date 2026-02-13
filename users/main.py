from fastapi import FastAPI, HTTPException, Depends
from typing import List
import uvicorn
from application.services.services import UserService
from infrastructure.adapters.user_repository import InMemoryUserRepository
from domain.user import User, UserCreate, UserUpdate

app = FastAPI(title="Sistema Restaurante - Microservicios para Usuarios")

# --- Dependencias ---
user_repository = InMemoryUserRepository()
user_service = UserService(user_repository)

def get_service():
    return user_service

# --- Endpoints CRUD ---

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, service: UserService = Depends(get_service)):
    try:
        return service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/", response_model=List[User])
def get_users(service: UserService = Depends(get_service)):
    return service.get_all_users()

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str, service: UserService = Depends(get_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user_update: UserUpdate, service: UserService = Depends(get_service)):
    try:
        user = service.update_user(user_id, user_update)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}")
def delete_user(user_id: str, service: UserService = Depends(get_service)):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)