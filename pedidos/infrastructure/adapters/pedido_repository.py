from typing import List, Optional
import uuid
from datetime import datetime
from domain.pedido import Pedido, PedidoCreate, PedidoUpdate, PedidoStatus
from application.ports.pedido_repository import PedidoRepository

class InMemoryPedidoRepository(PedidoRepository):
    def __init__(self):
        self.pedidos = {} # Simulación de base de datos

    def save(self, pedido_data: PedidoCreate) -> Pedido:
        pedido_id = str(uuid.uuid4())
        new_pedido = Pedido(
            id=pedido_id,
            producto=pedido_data.producto,
            id_usuario=pedido_data.id_usuario,
            cantidad=pedido_data.cantidad,
            created_at=datetime.now(),
            status=PedidoStatus.ACTIVE
        )
        self.pedidos[pedido_id] = new_pedido
        return new_pedido

    def find_by_id(self, pedido_id: str) -> Optional[Pedido]:
        return self.pedidos.get(pedido_id)

    def find_by_id_usuario(self, id_usuario: str) -> Optional[Pedido]:
        for pedido in self.pedidos.values():
            if pedido.id_usuario == id_usuario:
                return pedido
        return None

    def find_all(self) -> List[Pedido]:
        return list(self.pedidos.values())

    def update(self, pedido_id: str, pedido_update: PedidoUpdate) -> Optional[Pedido]:
        if pedido_id not in self.pedidos:
            return None
        
        current_pedido = self.pedidos[pedido_id]
        
        updated_data = current_pedido.dict()
        update_dict = pedido_update.dict(exclude_unset=True)
        updated_data.update(update_dict)
        
        updated_pedido = Pedido(**updated_data)
        self.pedidos[pedido_id] = updated_pedido
        return updated_pedido

    def delete(self, pedido_id: str) -> bool:
        if pedido_id in self.pedidos:
            del self.pedidos[pedido_id]
            return True
        return False