from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.models.equipment import EquipmentCategory, EquipmentItemStatus


class EquipmentModelBase(BaseModel):
    kategori: EquipmentCategory
    marka_yayin_evi: str = Field(min_length=2, max_length=120)
    model_adi: str = Field(min_length=2, max_length=120)
    require_staging: bool


class EquipmentModelCreate(EquipmentModelBase):
    pass


class EquipmentModelResponse(EquipmentModelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EquipmentItemBase(BaseModel):
    model_id: int
    demirbas_no: str = Field(min_length=1, max_length=80)
    durum: EquipmentItemStatus = EquipmentItemStatus.DEPODA


class EquipmentItemCreate(EquipmentItemBase):
    pass


class EquipmentItemResponse(EquipmentItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StagedEquipmentBase(BaseModel):
    model_id: int
    miktar: int = Field(gt=0)
    kaynak: str = Field(min_length=2, max_length=120)


class StagedEquipmentCreate(StagedEquipmentBase):
    pass


class StagedEquipmentResponse(StagedEquipmentBase):
    id: int
    eklendigi_tarih: datetime
    sayima_dahil_edildi_mi: bool

    model_config = ConfigDict(from_attributes=True)


class SistemeYeniMalzemeCreate(BaseModel):
    model_id: int
    miktar: int = Field(gt=0)
    kaynak: str = Field(min_length=2, max_length=120)


class SistemeYeniMalzemeResponse(BaseModel):
    hedef: str
    staged_kayit: StagedEquipmentResponse | None = None
    envanter_kayitlari: list[EquipmentItemResponse] = Field(default_factory=list)
