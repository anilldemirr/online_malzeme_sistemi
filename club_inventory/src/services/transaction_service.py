from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.equipment import EquipmentItem, EquipmentItemStatus
from src.models.transaction import Transaction, TransactionStatus, TransactionType
from src.services import audit_service


class TransactionService:
    @staticmethod
    async def dogrudan_zimmetle(
        db_session: AsyncSession,
        *,
        manager_id: int,
        hedef_uye_id: int,
        equipment_item_id: int,
    ) -> Transaction:
        equipment_item = await TransactionService._get_equipment_item_or_404(
            db_session, equipment_item_id
        )
        if equipment_item.durum != EquipmentItemStatus.DEPODA:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Secilen malzeme depoda degil.",
            )

        previous_item_state = TransactionService._equipment_item_state(equipment_item)

        transaction = Transaction(
            requested_model_id=equipment_item.model_id,
            assigned_item_id=equipment_item.id,
            talep_eden_id=manager_id,
            hedef_uye_id=hedef_uye_id,
            onaylayan_malzemeci_id=manager_id,
            islem_turu=TransactionType.DOGRUDAN_ZIMMET,
            islem_durumu=TransactionStatus.ONAYLANDI,
        )
        equipment_item.durum = EquipmentItemStatus.KULLANIMDA

        db_session.add(transaction)
        await db_session.flush()

        await audit_service.log_action(
            db_session,
            entity_type="Transaction",
            entity_id=transaction.id,
            user_id=manager_id,
            action="dogrudan_zimmet_olusturuldu",
            previous_state=None,
            new_state=TransactionService._transaction_state(transaction),
        )
        await audit_service.log_action(
            db_session,
            entity_type="EquipmentItem",
            entity_id=equipment_item.id,
            user_id=manager_id,
            action="zimmetlendi_durum_guncellendi",
            previous_state=previous_item_state,
            new_state=TransactionService._equipment_item_state(equipment_item),
        )
        return transaction

    @staticmethod
    async def devir_talebi_baslat(
        db_session: AsyncSession,
        *,
        devreden_uye_id: int,
        hedef_uye_id: int,
        equipment_item_id: int,
    ) -> Transaction:
        if devreden_uye_id == hedef_uye_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Devir ayni uye icin baslatilamaz.",
            )

        equipment_item = await TransactionService._get_equipment_item_or_404(
            db_session, equipment_item_id
        )
        if equipment_item.durum != EquipmentItemStatus.KULLANIMDA:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sadece kullanimdaki bir malzeme devredilebilir.",
            )

        await TransactionService._ensure_no_active_transfer(db_session, equipment_item.id)

        last_approved_transaction = await TransactionService._get_last_approved_item_transaction(
            db_session, equipment_item.id
        )
        if last_approved_transaction is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Malzeme icin aktif bir zimmet sahibi bulunamadi.",
            )

        current_holder_id = TransactionService._resolve_holder_id(last_approved_transaction)
        if current_holder_id != devreden_uye_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sadece mevcut zimmet sahibi devir baslatabilir.",
            )

        transaction = Transaction(
            requested_model_id=equipment_item.model_id,
            assigned_item_id=equipment_item.id,
            talep_eden_id=devreden_uye_id,
            hedef_uye_id=hedef_uye_id,
            islem_turu=TransactionType.DEVIR,
            islem_durumu=TransactionStatus.ALICI_ONAYI_BEKLIYOR,
        )
        db_session.add(transaction)
        await db_session.flush()

        await audit_service.log_action(
            db_session,
            entity_type="Transaction",
            entity_id=transaction.id,
            user_id=devreden_uye_id,
            action="devir_talebi_baslatildi",
            previous_state=None,
            new_state=TransactionService._transaction_state(transaction),
        )
        return transaction

    @staticmethod
    async def devir_alici_onayi(
        db_session: AsyncSession,
        *,
        transaction_id: int,
        alici_uye_id: int,
    ) -> Transaction:
        transaction = await TransactionService._get_transaction_or_404(db_session, transaction_id)
        if transaction.islem_turu != TransactionType.DEVIR:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu islem bir devir talebi degil.",
            )
        if transaction.hedef_uye_id != alici_uye_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Devir talebini sadece hedef uye onaylayabilir.",
            )
        if transaction.islem_durumu != TransactionStatus.ALICI_ONAYI_BEKLIYOR:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Devir talebi alici onayi asamasinda degil.",
            )

        previous_state = TransactionService._transaction_state(transaction)
        transaction.islem_durumu = TransactionStatus.MALZEMECI_ONAYI_BEKLIYOR
        await db_session.flush()

        await audit_service.log_action(
            db_session,
            entity_type="Transaction",
            entity_id=transaction.id,
            user_id=alici_uye_id,
            action="devir_alici_onaylandi",
            previous_state=previous_state,
            new_state=TransactionService._transaction_state(transaction),
        )
        return transaction

    @staticmethod
    async def devir_nihai_malzemeci_onayi(
        db_session: AsyncSession, transaction_id: int, manager_id: int
    ) -> Transaction:
        transaction = await TransactionService._get_transaction_or_404(db_session, transaction_id)
        if transaction.islem_turu != TransactionType.DEVIR:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu islem bir devir talebi degil.",
            )
        if transaction.islem_durumu != TransactionStatus.MALZEMECI_ONAYI_BEKLIYOR:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Devir talebi malzemeci onayi asamasinda degil.",
            )

        if manager_id == transaction.talep_eden_id or manager_id == transaction.hedef_uye_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Malzemeci, tarafi oldugu islemi onaylayamaz.",
            )

        if transaction.assigned_item_id is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Devir talebinde malzeme bilgisi eksik.",
            )
        equipment_item = await TransactionService._get_equipment_item_or_404(
            db_session, transaction.assigned_item_id
        )

        previous_transaction_state = TransactionService._transaction_state(transaction)
        previous_item_state = TransactionService._equipment_item_state(equipment_item)

        transaction.onaylayan_malzemeci_id = manager_id
        transaction.islem_durumu = TransactionStatus.ONAYLANDI
        equipment_item.durum = EquipmentItemStatus.KULLANIMDA
        await db_session.flush()

        await audit_service.log_action(
            db_session,
            entity_type="Transaction",
            entity_id=transaction.id,
            user_id=manager_id,
            action="devir_nihai_onaylandi",
            previous_state=previous_transaction_state,
            new_state=TransactionService._transaction_state(transaction),
        )
        await audit_service.log_action(
            db_session,
            entity_type="EquipmentItem",
            entity_id=equipment_item.id,
            user_id=manager_id,
            action="devir_sonrasi_zimmet_degisti",
            previous_state=previous_item_state,
            new_state=TransactionService._equipment_item_state(equipment_item),
        )
        return transaction

    @staticmethod
    async def _get_equipment_item_or_404(
        db_session: AsyncSession, equipment_item_id: int
    ) -> EquipmentItem:
        result = await db_session.execute(
            select(EquipmentItem).where(EquipmentItem.id == equipment_item_id)
        )
        equipment_item = result.scalar_one_or_none()
        if equipment_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Malzeme bulunamadi.",
            )
        return equipment_item

    @staticmethod
    async def _get_transaction_or_404(
        db_session: AsyncSession, transaction_id: int
    ) -> Transaction:
        result = await db_session.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        transaction = result.scalar_one_or_none()
        if transaction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Islem bulunamadi.",
            )
        return transaction

    @staticmethod
    async def _get_last_approved_item_transaction(
        db_session: AsyncSession, equipment_item_id: int
    ) -> Transaction | None:
        statement: Select[tuple[Transaction]] = (
            select(Transaction)
            .where(
                Transaction.assigned_item_id == equipment_item_id,
                Transaction.islem_durumu == TransactionStatus.ONAYLANDI,
                Transaction.islem_turu.in_(
                    [
                        TransactionType.DEPODAN_ALMA,
                        TransactionType.DOGRUDAN_ZIMMET,
                        TransactionType.DEVIR,
                    ]
                ),
            )
            .order_by(Transaction.tarih.desc(), Transaction.id.desc())
            .limit(1)
        )
        result = await db_session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def _ensure_no_active_transfer(
        db_session: AsyncSession, equipment_item_id: int
    ) -> None:
        statement: Select[tuple[Transaction]] = select(Transaction).where(
            Transaction.assigned_item_id == equipment_item_id,
            Transaction.islem_turu == TransactionType.DEVIR,
            Transaction.islem_durumu.in_(
                [
                    TransactionStatus.ALICI_ONAYI_BEKLIYOR,
                    TransactionStatus.MALZEMECI_ONAYI_BEKLIYOR,
                ]
            ),
        )
        result = await db_session.execute(statement)
        active_transfer = result.scalar_one_or_none()
        if active_transfer is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bu malzeme icin aktif bir devir sureci zaten var.",
            )

    @staticmethod
    def _resolve_holder_id(transaction: Transaction) -> int:
        if transaction.hedef_uye_id is not None:
            return transaction.hedef_uye_id
        return transaction.talep_eden_id

    @staticmethod
    def _transaction_state(transaction: Transaction) -> dict[str, Any]:
        timestamp = (
            transaction.tarih.isoformat()
            if isinstance(transaction.tarih, datetime)
            else str(transaction.tarih)
        )
        return {
            "id": transaction.id,
            "requested_model_id": transaction.requested_model_id,
            "assigned_item_id": transaction.assigned_item_id,
            "talep_eden_id": transaction.talep_eden_id,
            "hedef_uye_id": transaction.hedef_uye_id,
            "onaylayan_malzemeci_id": transaction.onaylayan_malzemeci_id,
            "islem_turu": transaction.islem_turu.value,
            "islem_durumu": transaction.islem_durumu.value,
            "tarih": timestamp,
        }

    @staticmethod
    def _equipment_item_state(equipment_item: EquipmentItem) -> dict[str, Any]:
        return {
            "id": equipment_item.id,
            "model_id": equipment_item.model_id,
            "demirbas_no": equipment_item.demirbas_no,
            "durum": equipment_item.durum.value,
        }
