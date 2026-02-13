from typing import List, Optional
from domain.pedido import (Pedido, PedidoCreate, PedidoUpdate, PedidoStatus)
from application.ports.pedido_repository import (PedidoRepository)

class PedidoService:
    def __init__(self, repository: PedidoRepository):
        self.repository = repository

    def register_pedido(self, pedido_data: PedidoCreate) -> Pedido:
        """Caso de uso: Registrar nuevo Pedido"""
        if not pedido_data.producto or not pedido_data.id_usuario:
            raise ValueError("Producto and id_usuario are required")
    
        existing_pedido = self.repository.find_by_id_usuario(pedido_data.id_usuario)
        if existing_pedido:
            raise ValueError(f"ID de usuario {pedido_data.id_usuario} is already registered")
        
        return self.repository.save(pedido_data)
    
    def get_pedido(self, pedido_id: str) -> Optional[Pedido]:
        """Caso de uso: Obtener pedido por ID"""
        return self.repository.find_by_id(pedido_id)

    def get_all_pedidos(self) -> List[Pedido]:
        """Caso de uso: Listar todos los pedidos"""
        return self.repository.find_all()

    def update_pedido(self, pedido_id: str, pedido_update: PedidoUpdate) -> Optional[Pedido]:
        """Caso de uso: Actualizar pedido"""
        pedido = self.repository.find_by_id(pedido_id)
        if not pedido:
            return None
        
        if pedido_update.id_usuario and pedido_update.id_usuario != pedido.id_usuario:
            existing_pedido = self.repository.find_by_id_usuario(pedido_update.id_usuario)
            if existing_pedido:
                raise ValueError(f"ID de Usuario {pedido_update.id_usuario} is already in use")
        
        return self.repository.update(pedido_id, pedido_update)

    def delete_pedido(self, pedido_id: str) -> bool:
        return self.repository.delete(pedido_id)

    def deactivate_pedido(self, pedido_id: str) -> Optional[Pedido]:
        pedido = self.repository.find_by_id(pedido_id)
        if not pedido:
            return None
        
        pedido.deactivate()
        return self.repository.update(pedido_id, PedidoUpdate(status=PedidoStatus.INACTIVE))

    def activate_pedido(self, pedido_id: str) -> Optional[Pedido]:
        pedido = self.repository.find_by_id(pedido_id)
        if not pedido:
            return None
        pedido.activate()
        return self.repository.update(pedido_id, PedidoUpdate(status=PedidoStatus.ACTIVE))