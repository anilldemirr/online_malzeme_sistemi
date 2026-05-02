from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class EquipmentCategory(str, Enum):
    TEKNIK_MALZEME = "teknik_malzeme"
    KITAP = "kitap"


class EquipmentItemStatus(str, Enum):
    DEPODA = "depoda"
    KULLANIMDA = "kullanimda"
    BAKIMDA = "bakimda"
    KAYIP = "kayip"


class EquipmentModel(Base):
    __tablename__ = "equipment_models"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kategori: Mapped[EquipmentCategory] = mapped_column(
        SqlEnum(EquipmentCategory, name="equipment_category", native_enum=False),
        nullable=False,
    )
    marka_yayin_evi: Mapped[str] = mapped_column(String(120), nullable=False)
    model_adi: Mapped[str] = mapped_column(String(120), nullable=False)
    require_staging: Mapped[bool] = mapped_column(nullable=False, default=True)

    items = relationship("EquipmentItem", back_populates="model")
    staged_entries = relationship("StagedEquipment", back_populates="model")
    requested_transactions = relationship("Transaction", back_populates="requested_model")


class EquipmentItem(Base):
    __tablename__ = "equipment_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("equipment_models.id"), nullable=False, index=True)
    demirbas_no: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    durum: Mapped[EquipmentItemStatus] = mapped_column(
        SqlEnum(EquipmentItemStatus, name="equipment_item_status", native_enum=False),
        nullable=False,
        default=EquipmentItemStatus.DEPODA,
    )

    model = relationship("EquipmentModel", back_populates="items")
    assigned_transactions = relationship("Transaction", back_populates="assigned_item")


class StagedEquipment(Base):
    __tablename__ = "staged_equipment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("equipment_models.id"), nullable=False, index=True)
    miktar: Mapped[int] = mapped_column(Integer, nullable=False)
    kaynak: Mapped[str] = mapped_column(String(120), nullable=False)
    eklendigi_tarih: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    sayima_dahil_edildi_mi: Mapped[bool] = mapped_column(nullable=False, default=False)

    model = relationship("EquipmentModel", back_populates="staged_entries")
