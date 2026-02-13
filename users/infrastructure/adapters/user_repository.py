from typing import List, Optional
import uuid
from datetime import datetime
from domain.user import User, UserCreate, UserUpdate, UserStatus
from application.ports.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {} # Simulación de base de datos

    def save(self, user_data: UserCreate) -> User:
        user_id = str(uuid.uuid4())
        new_user = User(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            created_at=datetime.now(),
            status=UserStatus.ACTIVE
        )
        self.users[user_id] = new_user
        return new_user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def find_all(self) -> List[User]:
        return list(self.users.values())

    def update(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        if user_id not in self.users:
            return None
        
        current_user = self.users[user_id]
        
        updated_data = current_user.dict()
        update_dict = user_update.dict(exclude_unset=True)
        updated_data.update(update_dict)
        
        updated_user = User(**updated_data)
        self.users[user_id] = updated_user
        return updated_user

    def delete(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False