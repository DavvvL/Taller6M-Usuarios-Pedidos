from fastapi import FastAPI, HTTPException, Depends
from typing import List
import uvicorn
from application.services.services import PedidoService
from infrastructure.adapters.pedido_repository import InMemoryPedidoRepository
from domain.pedido import Pedido, PedidoCreate, PedidoUpdate

#Prueba

app = FastAPI(title="Sistema Restaurante - Microservicios para Pedidos")

# --- Dependencias ---
pedido_repository = InMemoryPedidoRepository()
pedido_service = PedidoService(pedido_repository)

def get_service():
    return pedido_service

# --- Endpoints CRUD ---

@app.post("/pedidos/", response_model=Pedido)
def create_pedido(pedido: PedidoCreate, service: PedidoService = Depends(get_service)):
    try:
        return service.register_pedido(pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/pedidos/", response_model=List[Pedido])
def get_pedidos(service: PedidoService = Depends(get_service)):
    return service.get_all_pedidos()

@app.get("/pedidos/{pedido_id}", response_model=Pedido)
def get_pedido(pedido_id: str, service: PedidoService = Depends(get_service)):
    pedido = service.get_pedido(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@app.put("/pedidos/{pedido_id}", response_model=Pedido)
def update_pedido(pedido_id: str, pedido_update: PedidoUpdate, service: PedidoService = Depends(get_service)):
    try:
        pedido = service.update_pedido(pedido_id, pedido_update)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return pedido
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/pedidos/{pedido_id}")
def delete_pedido(pedido_id: str, service: PedidoService = Depends(get_service)):
    success = service.delete_pedido(pedido_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"message": "Pedido eliminado correctamente"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)