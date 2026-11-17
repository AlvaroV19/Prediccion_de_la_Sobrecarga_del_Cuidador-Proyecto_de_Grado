from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import require_admin, require_user
from ..django_auth_models import DjangoUser
from ..schemas import UserResponse, UserUpdate, UserCreate
from .. import user_service

router = APIRouter(prefix="/users", tags=["Users"])


# ── Registro público ───────────────────────────────────────────────
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Registrar un nuevo usuario",
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
    ):
    """
    Endpoint público. No requiere token.
    Crea un usuario nuevo en auth_user con la contraseña
    hasheada con el algoritmo PBKDF2 de Django.
    """
    return user_service.create_user(db, data)

# ── Perfil del usuario autenticado ────────────────────────────────
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener perfil propio",
)
def get_me(
    current_user: DjangoUser = Depends(require_user),
    ):
    """
    Devuelve los datos del usuario que está autenticado.
    No requiere rol de administrador.
    """
    return current_user


# ── CRUD de administrador ──────────────────────────────────────────
@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar todos los usuarios",
)
def list_users(
    db: Session = Depends(get_db),
    current_user: DjangoUser = Depends(require_admin),
    ):
    """
    Devuelve todos los usuarios registrados.
    Solo accesible por administradores.
    """
    return user_service.get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener un usuario por ID",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: DjangoUser = Depends(require_admin),
    ):
    """
    Devuelve un usuario específico por su ID.
    Solo accesible por administradores.
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar un usuario",
)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: DjangoUser = Depends(require_admin),
    ):
    """
    Actualiza los datos de un usuario existente.
    Solo accesible por administradores.
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user_service.update_user(db, user_id, data)


@router.delete(
    "/{user_id}",
    status_code=200,
    summary="Eliminar un usuario",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: DjangoUser = Depends(require_admin),
    ):
    """
    Elimina un usuario por su ID.
    Solo accesible por administradores.
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_service.delete_user(db, user_id)
    return {"detail": f"Usuario {user_id} eliminado correctamente"}