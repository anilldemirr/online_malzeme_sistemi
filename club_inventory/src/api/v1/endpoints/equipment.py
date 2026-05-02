from fastapi import APIRouter, Depends, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.dependencies import get_current_manager, get_current_user, get_db
from src.models.equipment import EquipmentItem, EquipmentItemStatus, EquipmentModel
from src.models.transaction import Transaction, TransactionStatus
from src.models.user import User
from src.schemas.equipment import EquipmentItemResponse, EquipmentModelResponse
from src.schemas.transaction import TalepOnayAtaCreate, TransactionResponse, UyeTalepCreate
from src.services.equipment_service import EquipmentService


router = APIRouter()


@router.get("/models", response_model=list[EquipmentModelResponse])
async def get_all_models(
    db_session: AsyncSession = Depends(get_db),
) -> list[EquipmentModelResponse]:
    """Tüm EquipmentModel'leri döner."""
    stmt = select(EquipmentModel)
    result = await db_session.execute(stmt)
    models = result.scalars().all()
    return [EquipmentModelResponse.model_validate(m) for m in models]


@router.get("/my-inventory", response_model=list[EquipmentItemResponse])
async def get_my_inventory(
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[EquipmentItemResponse]:
    """
    Üyenin kendi zimmetindeki malzemeleri döner.
    Durum 'kullanimda' olan ve hedef_uye olarak en son onaylanan işlemde bu kullanıcıya ait olan itemler.
    """
    # Subquery: Her item için en son approved transaction'ı bul
    subquery = (
        select(Transaction.assigned_item_id)
        .where(
            and_(
                Transaction.assigned_item_id.isnot(None),
                Transaction.hedef_uye_id == current_user.id,
                Transaction.islem_durumu == TransactionStatus.ONAYLANDI,
            )
        )
        .distinct()
    )

    # Ana query: "kullanimda" durumunda olan ve subquery'de olan item'ler
    stmt = select(EquipmentItem).where(
        and_(
            EquipmentItem.durum == EquipmentItemStatus.KULLANIMDA,
            EquipmentItem.id.in_(subquery),
        )
    )

    result = await db_session.execute(stmt)
    items = result.scalars().all()
    return [EquipmentItemResponse.model_validate(item) for item in items]


@router.post(
    "/talepler",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def uye_talep_olustur(
    payload: UyeTalepCreate,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionResponse:
    transaction = await EquipmentService.uye_talep_olustur(
        db_session=db_session,
        uye_id=current_user.id,
        requested_model_id=payload.requested_model_id,
    )
    await db_session.commit()
    await db_session.refresh(transaction)
    return TransactionResponse.model_validate(transaction)


@router.post(
    "/talepler/onayla-ve-ata",
    response_model=TransactionResponse,
)
async def malzemeci_talebi_onayla_ve_ata(
    payload: TalepOnayAtaCreate,
    db_session: AsyncSession = Depends(get_db),
    current_manager: User = Depends(get_current_manager),
) -> TransactionResponse:
    transaction = await EquipmentService.malzemeci_talebi_onayla_ve_ata(
        db_session=db_session,
        transaction_id=payload.transaction_id,
        manager_id=current_manager.id,
        assigned_item_id=payload.assigned_item_id,
    )
    await db_session.commit()
    await db_session.refresh(transaction)
    return TransactionResponse.model_validate(transaction)
