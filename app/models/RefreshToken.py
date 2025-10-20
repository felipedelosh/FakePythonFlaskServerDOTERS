import time
from typing import Optional

class RefreshToken:
    def __init__(
        self,
        member_id: int,
        refresh_token: str,
        created_at: Optional[str] = None,
    ):
        self.member_id = member_id
        self.refresh_token = refresh_token
        self.created_at = created_at or time.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"<RefreshToken member_id={self.member_id} refresh_token={self.refresh_token}>"

    @classmethod
    def from_row(cls, row: dict):
        if not row:
            return None
        return cls(
            member_id=row["memberId"],
            refresh_token=row["refresh_token"],
            created_at=row["created_at"],
        )
