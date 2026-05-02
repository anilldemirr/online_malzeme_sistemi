from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class TransactionType(str, Enum):
    DEPODAN_ALMA = "depodan_alma"
    DOGRUDAN_ZIMMET = "dogrudan_zimmet"
    IADE = "iade"
    DEVIR = "devir"


class TransactionStatus(str, Enum):
    BEKLEMEDE = "beklemede"
    ALICI_ONAYI_BEKLIYOR = "alici_onayi_bekliyor"
    MALZEMECI_ONAYI_BEKLIYOR = "malzemeci_onayi_bekliyor"
    ONAYLANDI = "onaylandi"
    REDDEDILDI = "reddedildi"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    requested_model_id: Mapped[int] = mapped_column(ForeignKey("equipment_models.id"), nullable=False, index=True)
    assigned_item_id: Mapped[int | None] = mapped_column(
        ForeignKey("equipment_items.id"),
        nullable=True,
        index=True,
    )
    talep_eden_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    hedef_uye_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    onaylayan_malzemeci_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    islem_turu: Mapped[TransactionType] = mapped_column(
        SqlEnum(TransactionType, name="transaction_type", native_enum=False),
        nullable=False,
    )
    islem_durumu: Mapped[TransactionStatus] = mapped_column(
        SqlEnum(TransactionStatus, name="transaction_status", native_enum=False),
        nullable=False,
        default=TransactionStatus.BEKLEMEDE,
    )
    tarih: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    requested_model = relationship("EquipmentModel", back_populates="requested_transactions")
    assigned_item = relationship("EquipmentItem", back_populates="assigned_transactions")
    talep_eden = relationship(
        "User",
        back_populates="requested_transactions",
        foreign_keys=[talep_eden_id],
    )
    hedef_uye = relationship(
        "User",
        back_populates="target_transactions",
        foreign_keys=[hedef_uye_id],
    )
    onaylayan_malzemeci = relationship(
        "User",
        back_populates="approved_transactions",
        foreign_keys=[onaylayan_malzemeci_id],
    )
