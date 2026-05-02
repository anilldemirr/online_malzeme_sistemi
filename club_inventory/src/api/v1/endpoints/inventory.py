from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_current_manager, get_db
from src.models.user import User
from src.schemas.equipment import (
    EquipmentItemResponse,
    SistemeYeniMalzemeCreate,
    SistemeYeniMalzemeResponse,
    StagedEquipmentResponse,
)
from src.services.inventory_service import InventoryService


router = APIRouter()


@router.post(
    "/yeni-malzeme",
    response_model=SistemeYeniMalzemeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def sisteme_yeni_malzeme_ekle(
    payload: SistemeYeniMalzemeCreate,
    db_session: AsyncSession = Depends(get_db),
    _current_manager: User = Depends(get_current_manager),
) -> SistemeYeniMalzemeResponse:
    result = await InventoryService.sisteme_yeni_malzeme_ekle(
        db_session=db_session,
        model_id=payload.model_id,
        miktar=payload.miktar,
        kaynak=payload.kaynak,
    )
    await db_session.commit()

    if isinstance(result, list):
        for equipment_item in result:
            await db_session.refresh(equipment_item)
        return SistemeYeniMalzemeResponse(
            hedef="ana_envanter",
            staged_kayit=None,
            envanter_kayitlari=[
                EquipmentItemResponse.model_validate(equipment_item)
                for equipment_item in result
            ],
        )

    await db_session.refresh(result)
    return SistemeYeniMalzemeResponse(
        hedef="bekleme_alani",
        staged_kayit=StagedEquipmentResponse.model_validate(result),
        envanter_kayitlari=[],
    )


@router.post(
    "/yillik-sayim-onayla",
    response_model=list[EquipmentItemResponse],
)
async def yillik_sayimi_onayla(
    db_session: AsyncSession = Depends(get_db),
    current_manager: User = Depends(get_current_manager),
) -> list[EquipmentItemResponse]:
    created_items = await InventoryService.yillik_sayimi_onayla(
        db_session=db_session,
        manager_id=current_manager.id,
    )
    await db_session.commit()

    for equipment_item in created_items:
        await db_session.refresh(equipment_item)
    return [EquipmentItemResponse.model_validate(equipment_item) for equipment_item in created_items]
