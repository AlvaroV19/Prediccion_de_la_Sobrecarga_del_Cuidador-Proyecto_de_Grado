from sqlalchemy import Column, Integer, String, Boolean, DateTime

from .database import Base


class DjangoUser(Base):

    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False, default="")   # NOT NULL en Django
    last_name = Column(String, nullable=False, default="")   # NOT NULL en Django
    is_staff = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    date_joined = Column(
        DateTime(timezone=True),
        nullable=False,   
    )
    last_login = Column(DateTime(timezone=True), nullable=True)