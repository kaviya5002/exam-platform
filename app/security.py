import hashlib, hmac, os, base64
# PBKDF2 keeps the demo self-contained; use a managed identity provider for production.
def hash_password(password: str) -> str:
    salt=os.urandom(16)
    digest=hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 180000)
    return base64.b64encode(salt).decode()+":"+base64.b64encode(digest).decode()
def verify_password(password: str, encoded: str) -> bool:
    try:
        salt_s,digest_s=encoded.split(":")
        salt=base64.b64decode(salt_s); expected=base64.b64decode(digest_s)
        actual=hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 180000)
        return hmac.compare_digest(actual, expected)
    except Exception: return False
