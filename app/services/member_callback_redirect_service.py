# app/services/member_callback_redirect_service.py
from typing import Dict, Any, Optional
from app.models.MemberCallbackRedirect import MemberCallbackRedirect
from app.repositories.member_callback_redirect_repository import MemberCallbackRedirectRepository


class MemberCallbackRedirectService:
    def __init__(self, callback_repo: Optional[MemberCallbackRedirectRepository] = None):
        self.callback_repo = callback_repo or MemberCallbackRedirectRepository()

    def save_callback(self, callback: MemberCallbackRedirect) -> Optional[Dict[str, Any]]:
        return self.callback_repo.save(callback)
