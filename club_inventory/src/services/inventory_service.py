from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.equipment import EquipmentItem, EquipmentItemStatus, EquipmentModel, StagedEquipment
from src.services import audit_service


class InventoryService:
    @staticmethod
    async def sisteme_yeni_malzeme_ekle(
        db_session: AsyncSession,
        model_id: int,
        miktar: int,
        kaynak: str,
    ) -> StagedEquipment | list[EquipmentItem]:
        if miktar <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="miktar sifirdan buyuk olmali.",
            )

        equipment_model = await InventoryService._get_model_or_404(db_session, model_id)

        if equipment_model.require_staging:
            staged_record = StagedEquipment(
                model_id=equipment_model.id,
                miktar=miktar,
                kaynak=kaynak,
                sayima_dahil_edildi_mi=False,
            )
            db_session.add(staged_record)
            await db_session.flush()
            await audit_service.log_action(
                db_session,
                entity_type="StagedEquipment",
                entity_id=staged_record.id,
                user_id=None,
                action="yeni_staged_kayit_eklendi",
                previous_state=None,
                new_state=InventoryService._staged_state(staged_record),
            )
            return staged_record

        created_items: list[EquipmentItem] = []
        for _ in range(miktar):
            demirbas_no = await InventoryService._generate_unique_demirbas_no(
                db_session,
                model_id=equipment_model.id,
            )
            item = EquipmentItem(
                model_id=equipment_model.id,
                demirbas_no=demirbas_no,
                durum=EquipmentItemStatus.DEPODA,
            )
            created_items.append(item)
            db_session.add(item)

        await db_session.flush()
        for item in created_items:
            await audit_service.log_action(
                db_session,
                entity_type="EquipmentItem",
                entity_id=item.id,
                user_id=None,
                action="yeni_envanter_kaydi_eklendi",
                previous_state=None,
                new_state=InventoryService._equipment_item_state(item),
            )
        return created_items

    @staticmethod
    async def yillik_sayimi_onayla(
        db_session: AsyncSession,
        manager_id: int,
    ) -> list[EquipmentItem]:
        statement = (
            select(StagedEquipment)
            .where(StagedEquipment.sayima_dahil_edildi_mi.is_(False))
            .order_by(StagedEquipment.id.asc())
        )
        result = await db_session.execute(statement)
        staged_records = list(result.scalars().all())

        created_items: list[EquipmentItem] = []
        staged_logs: list[tuple[dict[str, bool | int | str], StagedEquipment]] = []
        for staged_record in staged_records:
            previous_state = InventoryService._staged_state(staged_record)
            for _ in range(staged_record.miktar):
                demirbas_no = await InventoryService._generate_unique_demirbas_no(
                    db_session,
                    model_id=staged_record.model_id,
                )
                item = EquipmentItem(
                    model_id=staged_record.model_id,
                    demirbas_no=demirbas_no,
                    durum=EquipmentItemStatus.DEPODA,
                )
                created_items.append(item)
                db_session.add(item)

            staged_record.sayima_dahil_edildi_mi = True
            staged_logs.append((previous_state, staged_record))

        await db_session.flush()
        for item in created_items:
            await audit_service.log_action(
                db_session,
                entity_type="EquipmentItem",
                entity_id=item.id,
                user_id=manager_id,
                action="yillik_sayim_ile_envantere_eklendi",
                previous_state=None,
                new_state=InventoryService._equipment_item_state(item),
            )

        for previous_state, staged_record in staged_logs:
            await audit_service.log_action(
                db_session,
                entity_type="StagedEquipment",
                entity_id=staged_record.id,
                user_id=manager_id,
                action="yillik_sayim_onaylandi",
                previous_state=previous_state,
                new_state=InventoryService._staged_state(staged_record),
            )

        return created_items

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
    async def _generate_unique_demirbas_no(
        db_session: AsyncSession,
        model_id: int,
    ) -> str:
        while True:
            demirbas_no = f"DEM-{model_id}-{uuid4().hex[:10].upper()}"
            result = await db_session.execute(
                select(EquipmentItem.id).where(EquipmentItem.demirbas_no == demirbas_no)
            )
            existing_item_id = result.scalar_one_or_none()
            if existing_item_id is None:
                return demirbas_no

    @staticmethod
    def _staged_state(staged_record: StagedEquipment) -> dict[str, bool | int | str]:
        return {
            "id": staged_record.id,
            "model_id": staged_record.model_id,
            "miktar": staged_record.miktar,
            "kaynak": staged_record.kaynak,
            "sayima_dahil_edildi_mi": staged_record.sayima_dahil_edildi_mi,
        }

    @staticmethod
    def _equipment_item_state(equipment_item: EquipmentItem) -> dict[str, str | int]:
        return {
            "id": equipment_item.id,
            "model_id": equipment_item.model_id,
            "demirbas_no": equipment_item.demirbas_no,
            "durum": equipment_item.durum.value,
        }
