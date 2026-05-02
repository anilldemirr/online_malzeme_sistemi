from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.equipment import EquipmentCategory, EquipmentItem, EquipmentItemStatus, EquipmentModel
from src.models.transaction import Transaction, TransactionStatus, TransactionType
from src.services import audit_service


class EquipmentService:
    @staticmethod
    async def create_equipment_model(
        session: AsyncSession,
        *,
        kategori: EquipmentCategory,
        marka_yayin_evi: str,
        model_adi: str,
    ) -> EquipmentModel:
        require_staging = kategori == EquipmentCategory.TEKNIK_MALZEME
        equipment_model = EquipmentModel(
            kategori=kategori,
            marka_yayin_evi=marka_yayin_evi,
            model_adi=model_adi,
            require_staging=require_staging,
        )
        session.add(equipment_model)
        await session.flush()
        return equipment_model

    @staticmethod
    async def uye_talep_olustur(
        db_session: AsyncSession,
        uye_id: int,
        requested_model_id: int,
    ) -> Transaction:
        requested_model = await EquipmentService._get_model_or_404(db_session, requested_model_id)

        transaction = Transaction(
            requested_model_id=requested_model.id,
            assigned_item_id=None,
            talep_eden_id=uye_id,
            hedef_uye_id=None,
            onaylayan_malzemeci_id=None,
            islem_turu=TransactionType.DEPODAN_ALMA,
            islem_durumu=TransactionStatus.BEKLEMEDE,
        )
        db_session.add(transaction)
        await db_session.flush()
        await audit_service.log_action(
            db_session,
            entity_type="Transaction",
            entity_id=transaction.id,
            user_id=uye_id,
            action="uye_talebi_olusturuldu",
            previous_state=None,
            new_state=EquipmentService._transaction_state(transaction),
        )
        return transaction

    @staticmethod
    async def malzemeci_talebi_onayla_ve_ata(
        db_session: AsyncSession,
        transaction_id: int,
        manager_id: int,
        assigned_item_id: int,
    ) -> Transaction:
        transaction = await EquipmentService._get_transaction_or_404(db_session, transaction_id)
        if transaction.islem_turu != TransactionType.DEPODAN_ALMA:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Islem tipi depodan_alma olmali.",
            )
        if transaction.islem_durumu != TransactionStatus.BEKLEMEDE:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Talep beklemede durumunda olmali.",
            )
        if manager_id == transaction.talep_eden_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Malzemeci kendi talebini onaylayamaz.",
            )

        equipment_item = await EquipmentService._get_item_or_404(db_session, assigned_item_id)
        if equipment_item.durum != EquipmentItemStatus.DEPODA:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Atanacak malzeme depoda olmali.",
            )
        if equipment_item.model_id != transaction.requested_model_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Atanan malzeme talep edilen model ile uyusmuyor.",
            )

        previous_transaction_state = EquipmentService._transaction_state(transaction)
        previous_item_state = EquipmentService._equipment_item_state(equipment_item)

        equipment_item.durum = EquipmentItemStatus.KULLANIMDA
        transaction.assigned_item_id = equipment_item.id
        transaction.onaylayan_malzemeci_id = manager_id
        transaction.hedef_uye_id = transaction.talep_eden_id
        transaction.islem_durumu = TransactionStatus.ONAYLANDI
        await db_session.flush()

        await audit_service.log_action(
            db_session,
            entity_type="Transaction",
            entity_id=transaction.id,
            user_id=manager_id,
            action="talep_onaylandi_ve_item_atandi",
            previous_state=previous_transaction_state,
            new_state=EquipmentService._transaction_state(transaction),
        )
        await audit_service.log_action(
            db_session,
            entity_type="EquipmentItem",
            entity_id=equipment_item.id,
            user_id=manager_id,
            action="depodan_alma_talebi_icin_zimmetlendi",
            previous_state=previous_item_state,
            new_state=EquipmentService._equipment_item_state(equipment_item),
        )
        return transaction

    @staticmethod
    async def _get_model_or_404(
        db_session: AsyncSession,
        model_id: int,
    ) -> EquipmentModel:
        result = await db_session.execute(
            select(EquipmentModel).where(EquipmentModel.id == model_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="EquipmentModel bulunamadi.",
            )
        return model

    @staticmethod
    async def _get_transaction_or_404(
        db_session: AsyncSession,
        transaction_id: int,
    ) -> Transaction:
        result = await db_session.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        transaction = result.scalar_one_or_none()
        if transaction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction bulunamadi.",
            )
        return transaction

    @staticmethod
    async def _get_item_or_404(
        db_session: AsyncSession,
        equipment_item_id: int,
    ) -> EquipmentItem:
        result = await db_session.execute(
            select(EquipmentItem).where(EquipmentItem.id == equipment_item_id)
        )
        equipment_item = result.scalar_one_or_none()
        if equipment_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="EquipmentItem bulunamadi.",
            )
        return equipment_item

    @staticmethod
    def _transaction_state(transaction: Transaction) -> dict[str, Any]:
        return {
            "id": transaction.id,
            "requested_model_id": transaction.requested_model_id,
            "assigned_item_id": transaction.assigned_item_id,
            "talep_eden_id": transaction.talep_eden_id,
            "hedef_uye_id": transaction.hedef_uye_id,
            "onaylayan_malzemeci_id": transaction.onaylayan_malzemeci_id,
            "islem_turu": transaction.islem_turu.value,
            "islem_durumu": transaction.islem_durumu.value,
            "tarih": str(transaction.tarih),
        }

    @staticmethod
    def _equipment_item_state(equipment_item: EquipmentItem) -> dict[str, Any]:
        return {
            "id": equipment_item.id,
            "model_id": equipment_item.model_id,
            "demirbas_no": equipment_item.demirbas_no,
            "durum": equipment_item.durum.value,
        }
