"""
Mini JWT-like token generator (HS256) — no dependencias externas.
Ahora soporta:
- create_id_token(...)      -> JWT con claims de identidad (token_use="id")
- create_access_token(...)  -> JWT con claims de acceso   (token_use="access", scope, aud, client_id)
- create_opaque_token(...)  -> cadena opaca aleatoria (útil para access/refresh mock)
- create_refresh_token(...) -> cadena opaca aleatoria
- create_token(...)         -> alias histórico (ID token)
- verify_token(...)         -> verificación HS256 + exp
"""
import json
import time
import hmac
import hashlib
import base64
import os
import secrets
from typing import Dict, Any, Optional, List

# -----------------------
# Helpers base64url
# -----------------------
def _b64u_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def _b64u_encode_json(obj: Dict[str, Any]) -> str:
    return _b64u_encode(json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8"))

# -----------------------
# Defaults
# -----------------------
_DEFAULT_SECRET = os.getenv("DOTERS_MOCK_SECRET") or secrets.token_urlsafe(32)
_DEFAULT_ISS = os.getenv("DOTERS_MOCK_ISS", "doters-mock")

# -----------------------
# Core signer
# -----------------------
def _sign_jwt(payload: Dict[str, Any], ttl_seconds: int, secret: Optional[str] = None, header_extra: Optional[Dict[str, Any]] = None) -> str:
    secret = secret or _DEFAULT_SECRET
    now = int(time.time())

    header = {"alg": "HS256", "typ": "JWT"}
    if header_extra:
        header.update(header_extra)

    body = dict(payload)
    body.setdefault("iat", now)
    body.setdefault("exp", now + int(ttl_seconds))
    body.setdefault("iss", _DEFAULT_ISS)

    header_b64 = _b64u_encode_json(header)
    payload_b64 = _b64u_encode_json(body)
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")

    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64u_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"

# -----------------------
# Public API
# -----------------------
def create_id_token(claims: Dict[str, Any], *, client_id: Optional[str] = None, ttl_seconds: int = 60 * 60 * 6, secret: Optional[str] = None) -> str:
    """
    ID Token (OIDC-like). Incluye token_use="id".
    - claims típicos: {"sub": "...", "email": "...", "name": "...", "uid": "..."}
    - client_id -> se coloca en 'aud' si se provee.
    """
    payload = dict(claims)
    payload["token_use"] = "id"
    if client_id:
        payload.setdefault("aud", client_id)
    return _sign_jwt(payload, ttl_seconds, secret)

def create_access_token(
    subject: str,
    *,
    client_id: str,
    scope: str | List[str] = "openid",
    ttl_seconds: int = 60 * 60,  # 1h por defecto para access tokens
    secret: Optional[str] = None,
    extra_claims: Optional[Dict[str, Any]] = None
) -> str:
    """
    Access Token (JWT-like). Incluye:
    - sub: sujeto (usuario)
    - aud: audiencia = client_id
    - client_id: quien pide el token
    - scope: string "a b c" o lista ["a","b","c"]
    - token_use="access"
    - + extra_claims opcionales (p.ej. {"uid": "123", "role": "member"})
    """
    if isinstance(scope, list):
        scope_str = " ".join(scope)
    else:
        scope_str = scope

    payload = {
        "sub": subject,
        "aud": client_id,
        "client_id": client_id,
        "scope": scope_str,
        "token_use": "access",
    }
    if extra_claims:
        payload.update(extra_claims)

    return _sign_jwt(payload, ttl_seconds, secret)

def create_opaque_token(length_bytes: int = 32) -> str:
    """Crea una cadena opaca (URL-safe). Útil para mocks de access/refresh."""
    return secrets.token_urlsafe(length_bytes)

def create_refresh_token(length_bytes: int = 32) -> str:
    """Alias semántico para refresh tokens opacos."""
    return create_opaque_token(length_bytes)

# Retro-compat: tu función anterior genera un ID Token
def create_token(claims: Dict[str, Any], ttl_seconds: int = 60 * 60 * 6, secret: Optional[str] = None) -> str:
    return create_id_token(claims, ttl_seconds=ttl_seconds, secret=secret)

# Verificación simple (HS256 + exp)
def verify_token(token: str, secret: Optional[str] = None) -> bool:
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
