from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.hash import django_pbkdf2_sha256
from datetime import datetime, timezone

from .django_auth_models import DjangoUser
from .schemas import UserUpdate, UserCreate


def get_user_by_username(db: Session, username: str) -> DjangoUser | None:
    return (
        db.query(DjangoUser)
        .filter(DjangoUser.username == username)
        .first()
    )


def get_all_users(db: Session) -> list[DjangoUser]:
    return db.query(DjangoUser).all()


def get_user_by_id(db: Session, user_id: int) -> DjangoUser | None:
    return db.query(DjangoUser).filter(DjangoUser.id == user_id).first()


def create_user(db: Session, data: UserCreate) -> DjangoUser:
    """
    Crea un usuario nuevo hasheando la contraseña correctamente
    con el algoritmo de Django (PBKDF2) antes de guardarla.
    """
    # Verificar que el username no esté tomado
    if get_user_by_username(db, data.username):
        raise HTTPException(
            status_code=409,
            detail=f"El usuario '{data.username}' ya está tomado. Por favor, elige otro nombre de usuario.",
        )

    # Verificar que el email no esté tomado
    if get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=409,
            detail=f"El correo '{data.email}' ya está registrado.",
        )

    user = DjangoUser(
        username = data.username,
        email = data.email,
        password = django_pbkdf2_sha256.hash(data.password),  # hashea con PBKDF2 de Django
        first_name = data.first_name,      # requerido por auth_user y directo del schema
        last_name = data.last_name,       # requerido por auth_user y directo del schema
        is_staff = False,
        is_superuser = False,
        is_active = True,
        date_joined = datetime.now(timezone.utc),  # requerido por auth_user y directo del schema
        last_login = None,  # requerido por auth_user y directo del schema
    ) 

    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        # Respaldo ante condiciones de carrera: dos registros simultáneos
        # con el mismo username/email pueden pasar ambas validaciones de
        # arriba antes de que cualquiera haga commit. La restricción UNIQUE
        # de la base de datos (PASO 7) es la que realmente lo evita.
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="El nombre de usuario o el correo ya están registrados.",
        )
    
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, data: UserUpdate) -> DjangoUser | None:
    """
    Actualiza solo los campos enviados explícitamente.
    Ignora los campos None (actualización parcial).
    """
    user = db.query(DjangoUser).filter(DjangoUser.id == user_id).first()
    if not user:
        return None

    campos = data.model_dump(exclude_unset=True)
    for campo, valor in campos.items():
        setattr(user, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="El nombre de usuario o el correo ya están registrados.",
        )
    
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> DjangoUser | None:
    user = db.query(DjangoUser).filter(DjangoUser.id == user_id).first()
    if not user:
        return None
    
    db.delete(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el usuario.",
        )
    
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> DjangoUser | None:
    return (
        db.query(DjangoUser)
        .filter(DjangoUser.email == email)
        .first()
    )