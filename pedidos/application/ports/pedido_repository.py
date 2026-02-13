from abc import ABC, abstractmethod
from typing import List, Optional
from domain.pedido import Pedido, PedidoCreate, PedidoUpdate

class PedidoRepository(ABC):
    @abstractmethod
    def save(self, pedido: PedidoCreate) -> Pedido:
        pass

    @abstractmethod
    def find_by_id(self, pedido_id: str) -> Optional[Pedido]:
        pass

    @abstractmethod
    def find_by_id_usuario(self, id_usuario: str) -> Optional[Pedido]:
        pass

    @abstractmethod
    def find_all(self) -> List[Pedido]:
        pass

    @abstractmethod
    def update(self, pedido_id: str, pedido_update: PedidoUpdate) -> Optional[Pedido]:
        pass

    @abstractmethod
    def delete(self, pedido_id: str) -> bool:
        pass