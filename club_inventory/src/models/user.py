from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class UserRole(str, Enum):
    MEMBER = "member"
    MANAGER = "manager"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ad_soyad: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    rol: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole, name="user_role", native_enum=False),
        nullable=False,
        default=UserRole.MEMBER,
    )

    requested_transactions = relationship(
        "Transaction",
        back_populates="talep_eden",
        foreign_keys="Transaction.talep_eden_id",
    )
    target_transactions = relationship(
        "Transaction",
        back_populates="hedef_uye",
        foreign_keys="Transaction.hedef_uye_id",
    )
    approved_transactions = relationship(
        "Transaction",
        back_populates="onaylayan_malzemeci",
        foreign_keys="Transaction.onaylayan_malzemeci_id",
    )
    audit_logs = relationship("AuditLog", back_populates="user")
