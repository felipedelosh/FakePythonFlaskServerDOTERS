# app/models/MemberCallbackRedirect.py
from typing import Optional

class MemberCallbackRedirect:
    def __init__(
        self,
        member_id: int,
        callback_url: str,
        created_at: Optional[str] = None,
    ):
        self.member_id = member_id
        self.callback_url = (callback_url or "").strip()
        self.created_at = created_at 

    @classmethod
    def from_payload(cls, payload: dict):
        """
        Construye un objeto desde el JSON del request.
        Acepta varias variantes de nombre de campos para robustez:
          - memberId | memberID | member_id
          - callbackUrl | callback_url
        """
        member_raw = (
            payload.get("memberId", None)
            or payload.get("memberID", None)
            or payload.get("member_id", None)
        )
        url_raw = payload.get("callbackUrl", None) or payload.get("callback_url", None)

        return cls(
            member_id=int(member_raw or 0),
            callback_url=str(url_raw or ""),
        )

    def to_dict(self) -> dict:
        """Dict listo para usar en el repositorio (INSERT)."""
        return {
            "member_id": self.member_id,
            "callback_url": self.callback_url,
        }

    def __repr__(self):
        return f"<MemberCallbackRedirect member_id={self.member_id} url={self.callback_url}>"
