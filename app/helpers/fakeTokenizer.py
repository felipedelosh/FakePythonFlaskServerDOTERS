# app/helpers/fakeTokenizer.py
"""
Mini JWT-like token generator (HS256) — no dependencias externas.
Genera tokens con formato: base64url(header).base64url(payload).base64url(signature)

Header: {"alg":"HS256","typ":"JWT"}
Payload: user claims + iat/exp/iss
Signature: HMAC-SHA256(header.payload, secret)

NOTA: es una implementación para mocking/testing. No uses el secreto en producción.
"""
import json
import time
import hmac
import hashlib
import base64
import os
import secrets
from typing import Dict, Any

# Helper: base64url encode without padding
def _b64u_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def _b64u_encode_json(obj: Dict[str, Any]) -> str:
    return _b64u_encode(json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8"))

# default secret (override with env var DOTERS_MOCK_SECRET)
_DEFAULT_SECRET = os.getenv("DOTERS_MOCK_SECRET", None) or secrets.token_urlsafe(32)
_DEFAULT_ISS = os.getenv("DOTERS_MOCK_ISS", "doters-mock")

def create_token(claims: Dict[str, Any], ttl_seconds: int = 60 * 60 * 6, secret: str | None = None) -> str:
    """
    Create a JWT-like token (HS256).
    - claims: dict with user claims (e.g., {"sub": "email", "name": "X"})
    - ttl_seconds: token lifetime in seconds (default 6 hours)
    - secret: optional secret to sign with (str). If None, uses env/default.
    Returns token string.
    """
    secret = secret or _DEFAULT_SECRET
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = dict(claims)  # copy
    payload.setdefault("iat", now)
    payload.setdefault("exp", now + int(ttl_seconds))
    payload.setdefault("iss", _DEFAULT_ISS)

    header_b64 = _b64u_encode_json(header)
    payload_b64 = _b64u_encode_json(payload)
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")

    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64u_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"

# Optional verify function (useful for tests)
def verify_token(token: str, secret: str | None = None) -> bool:
    """
    Verify signature and expiration. Returns True if valid, False otherwise.
    """
    try:
        secret = secret or _DEFAULT_SECRET
        parts = token.split(".")
        if len(parts) != 3:
            return False
        header_b64, payload_b64, signature_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        expected_sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
        expected_sig_b64 = _b64u_encode(expected_sig)
        if not hmac.compare_digest(expected_sig_b64, signature_b64):
            return False
        # decode payload and check exp
        padded = payload_b64 + "=" * (-len(payload_b64) % 4)
        payload_bytes = base64.urlsafe_b64decode(padded.encode("ascii"))
        payload = json.loads(payload_bytes.decode("utf-8"))
        exp = int(payload.get("exp", 0))
        if int(time.time()) > exp:
            return False
        return True
    except Exception:
        return False
