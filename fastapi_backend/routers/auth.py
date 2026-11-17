import os
import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from ..database import get_db
from ..user_service import get_user_by_username, get_user_by_email
from ..auth import create_access_token, verify_password
from ..models import PasswordResetToken, ActivationToken
from ..django_auth_models import DjangoUser
from ..email_service import send_password_reset_email
from passlib.hash import django_pbkdf2_sha256

router = APIRouter(prefix="/auth", tags=["Auth"])

APP_ENV = os.getenv("APP_ENV", "development")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://127.0.0.1:8001")

# ── Schemas locales ────────────────────────────────────────────────
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ActivationRequest(BaseModel):
    token: str


# ── Login ──────────────────────────────────────────────────────────
@router.post("/token", summary="Obtener token de acceso")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Recibe usuario y contraseña.
    Si las credenciales son correctas devuelve un JWT de acceso.
    """
    user = get_user_by_username(db, username=form_data.username)

    if not user or not verify_password(
        plain_password=form_data.password,
        hashed_password=user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    role = "admin" if user.is_superuser else "user"

    access_token = create_access_token({
        "sub": form_data.username,
        "role": role,
        "user_id": user.id,
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ── Forgot password ────────────────────────────────────────────────
@router.post("/forgot-password", summary="Solicitar recuperación de contraseña")
def forgot_password(
    data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Busca el usuario por email, genera un token de recuperación
    y lo guarda en la BD. En producción se enviaría por email.
    """
    user = get_user_by_email(db, data.email)

    # Siempre responder igual para no revelar si el email existe
    if not user:
        return {"message": "Si el correo está registrado, recibirás las instrucciones."}

    # Invalidar tokens anteriores del mismo usuario
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used == False,
    ).update({"used": True})
    db.commit()

    # Crear nuevo token
    token_value = str(uuid.uuid4())
    expires_at  = datetime.now(timezone.utc) + timedelta(minutes=30)

    reset_token = PasswordResetToken(
        user_id    = user.id,
        token      = token_value,
        expires_at = expires_at,
        used       = False,
    )
    db.add(reset_token)
    db.commit()

    # Envío real de correo, en segundo plano (no bloquea la respuesta HTTP)
    reset_url = f"{FRONTEND_BASE_URL.rstrip('/')}/reset-password/{token_value}/"
    background_tasks.add_task(send_password_reset_email, user.email, reset_url)

    # El token solo se expone en la respuesta si estamos en desarrollo.
    # En producción, la única vía para obtenerlo es el correo enviado arriba.
    if APP_ENV == "development":
        return {
            "message": "Si el correo está registrado, recibirás las instrucciones.",
            "dev_token": token_value,
            "expires_at": expires_at.isoformat(),
        }

    return {"message": "Si el correo está registrado, recibirás las instrucciones."}


# ── Reset password ─────────────────────────────────────────────────
@router.post("/reset-password", summary="Restablecer contraseña")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Verifica el token, aplica la nueva contraseña y marca el token como usado.
    """
    # Buscar token válido
    reset = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == data.token,
        PasswordResetToken.used  == False,
    ).first()

    if not reset:
        raise HTTPException(status_code=400, detail="Token inválido o ya utilizado.")

    # Verificar expiración
    now = datetime.now(timezone.utc)
    expires = reset.expires_at

    # Normalizar timezone si viene sin tzinfo
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

    if now > expires:
        raise HTTPException(status_code=400, detail="El token ha expirado.")

    # Actualizar contraseña
    user = db.query(DjangoUser).filter(DjangoUser.id == reset.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    user.password = django_pbkdf2_sha256.hash(data.new_password)

    # Marcar token como usado
    reset.used = True

    db.commit()

    return {"message": "Contraseña actualizada correctamente."}