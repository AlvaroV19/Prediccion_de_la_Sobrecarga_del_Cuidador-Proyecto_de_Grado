from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.hash import django_pbkdf2_sha256
from sqlalchemy.orm import Session

from .database import get_db
from .django_auth_models import DjangoUser

# ── Configuración JWT ──────────────────────────────────────────────
SECRET_KEY = "ProyectoGrado2026JWT"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ── JWT ────────────────────────────────────────────────────────────
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def _decode_token(token: str) -> dict:
    """Decodifica el JWT y devuelve el payload. Lanza 401 si es inválido."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


# ── Contraseñas ────────────────────────────────────────────────────
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return django_pbkdf2_sha256.verify(plain_password, hashed_password)


# ── Dependencias de autenticación ──────────────────────────────────
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    ) -> DjangoUser:
    """
    Decodifica el token, busca el usuario en la BD y verifica que esté activo.
    Devuelve un DjangoUser real, no un payload.
    """
    payload = _decode_token(token)

    user_id: int = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token sin identidad de usuario")

    user = db.query(DjangoUser).filter(DjangoUser.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    return user


# ── Dependencias de autorización ───────────────────────────────────
def require_admin(current_user: DjangoUser = Depends(get_current_user)) -> DjangoUser:
    """Solo permite el acceso a superusuarios (is_superuser=True)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
    return current_user


def require_user(current_user: DjangoUser = Depends(get_current_user)) -> DjangoUser:
    """Permite acceso a cualquier usuario activo (admin o usuario normal)."""
    # get_current_user ya verifica is_active, así que aquí solo retornamos
    return current_user