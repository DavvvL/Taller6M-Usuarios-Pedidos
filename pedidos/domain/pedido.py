from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class PedidoStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE =  "inactive"

class Pedido(BaseModel):
    id: str
    producto: str
    id_usuario: str
    cantidad: str
    status: PedidoStatus = PedidoStatus.ACTIVE
    created_at: datetime
    
    def activate(self):
        self.status = PedidoStatus.ACTIVE
        
    def deactivate(self):
        self.status = PedidoStatus.INACTIVE
        
    def is_active(self) -> bool:
        return self.status == PedidoStatus.ACTIVE
    
class PedidoCreate(BaseModel):
    producto: str
    id_usuario: str
    cantidad: str

class PedidoUpdate(BaseModel):
    producto: Optional[str] = None
    id_usuario: Optional[str] = None
    cantidad: Optional[str] = None
    status: Optional[PedidoStatus] = None