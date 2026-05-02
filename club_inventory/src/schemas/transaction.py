from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.models.transaction import TransactionStatus, TransactionType


class TransactionBase(BaseModel):
    requested_model_id: int
    assigned_item_id: int | None = None
    talep_eden_id: int
    hedef_uye_id: int | None
    islem_turu: TransactionType


class TransactionCreate(TransactionBase):
    pass


class DogrudanZimmetCreate(BaseModel):
    hedef_uye_id: int
    equipment_item_id: int


class DevirTalebiCreate(BaseModel):
    hedef_uye_id: int
    equipment_item_id: int


class DevirAliciOnayiCreate(BaseModel):
    transaction_id: int


class DevirNihaiOnayCreate(BaseModel):
    transaction_id: int


class UyeTalepCreate(BaseModel):
    requested_model_id: int


class TalepOnayAtaCreate(BaseModel):
    transaction_id: int
    assigned_item_id: int


class TransactionResponse(TransactionBase):
    id: int
    onaylayan_malzemeci_id: int | None
    islem_durumu: TransactionStatus
    tarih: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)
