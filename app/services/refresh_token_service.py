# app/services/refresh_token_service.py
from typing import Optional
from app.models.RefreshToken import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository

class RefreshTokenService:
    def __init__(self, repository: RefreshTokenRepository):
        self.repository = repository

    def save(self, refresh_token: RefreshToken) -> bool:
        return self.repository.save_refresh_token(refresh_token)

    def get_by_token(self, token: str) -> Optional[RefreshToken]:
        return self.repository.get_by_token(token)
