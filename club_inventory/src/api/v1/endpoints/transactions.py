from fastapi import APIRouter, Depends, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_current_manager, get_current_user, get_db
from src.models.transaction import Transaction, TransactionStatus
from src.models.user import User
from src.schemas.transaction import (
    DevirAliciOnayiCreate,
    DevirNihaiOnayCreate,
    DevirTalebiCreate,
    DogrudanZimmetCreate,
    TransactionResponse,
)
from src.services.transaction_service import TransactionService


router = APIRouter()


@router.get("/pending", response_model=list[TransactionResponse])
async def get_pending_transactions(
    db_session: AsyncSession = Depends(get_db),
    current_manager: User = Depends(get_current_manager),
) -> list[TransactionResponse]:
    """
    Malzemeci onayı bekleyen tüm işlemleri döner (beklemede, alici_onayi_bekliyor, malzemeci_onayi_bekliyor).
    Sadece manager rolündeki kullanıcılar erişebilir.
    """
    stmt = select(Transaction).where(
        Transaction.islem_durumu.in_(
            [
                TransactionStatus.BEKLEMEDE,
                TransactionStatus.ALICI_ONAYI_BEKLIYOR,
                TransactionStatus.MALZEMECI_ONAYI_BEKLIYOR,
            ]
        )
    )

    result = await db_session.execute(stmt)
    transactions = result.scalars().all()
    return [TransactionResponse.model_validate(t) for t in transactions]


@router.post(
    "/dogrudan-zimmet",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def dogrudan_zimmetle(
    payload: DogrudanZimmetCreate,
    db_session: AsyncSession = Depends(get_db),
    current_manager: User = Depends(get_current_manager),
) -> TransactionResponse:
    transaction = await TransactionService.dogrudan_zimmetle(
        db_session=db_session,
        manager_id=current_manager.id,
        hedef_uye_id=payload.hedef_uye_id,
        equipment_item_id=payload.equipment_item_id,
    )
    await db_session.commit()
    await db_session.refresh(transaction)
    return TransactionResponse.model_validate(transaction)


@router.post(
    "/devir-talebi-baslat",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def devir_talebi_baslat(
    payload: DevirTalebiCreate,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionResponse:
    transaction = await TransactionService.devir_talebi_baslat(
        db_session=db_session,
        devreden_uye_id=current_user.id,
        hedef_uye_id=payload.hedef_uye_id,
        equipment_item_id=payload.equipment_item_id,
    )
    await db_session.commit()
    await db_session.refresh(transaction)
    return TransactionResponse.model_validate(transaction)


@router.post(
    "/devir-alici-onayi",
    response_model=TransactionResponse,
)
async def devir_alici_onayi(
    payload: DevirAliciOnayiCreate,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionResponse:
    transaction = await TransactionService.devir_alici_onayi(
        db_session=db_session,
        transaction_id=payload.transaction_id,
        alici_uye_id=current_user.id,
    )
    await db_session.commit()
    await db_session.refresh(transaction)
    return TransactionResponse.model_validate(transaction)


@router.post(
    "/devir-nihai-malzemeci-onayi",
    response_model=TransactionResponse,
)
async def devir_nihai_malzemeci_onayi(
    payload: DevirNihaiOnayCreate,
    db_session: AsyncSession = Depends(get_db),
    current_manager: User = Depends(get_current_manager),
) -> TransactionResponse:
    transaction = await TransactionService.devir_nihai_malzemeci_onayi(
        db_session=db_session,
        transaction_id=payload.transaction_id,
        manager_id=current_manager.id,
    )
    await db_session.commit()
    await db_session.refresh(transaction)
    return TransactionResponse.model_validate(transaction)


@router.post(
    "/dogrudan-zimmet-onayla",
    response_model=TransactionResponse,
)
async def dogrudan_zimmet_onayla(
    payload: DevirAliciOnayiCreate,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionResponse:
    transaction = await TransactionService.dogrudan_zimmet_onayla(
        db_session=db_session,
        transaction_id=payload.transaction_id,
        alici_uye_id=current_user.id,
    )
    await db_session.commit()
    await db_session.refresh(transaction)
    return TransactionResponse.model_validate(transaction)


@router.post(
    "/dogrudan-zimmet-reddet",
    response_model=TransactionResponse,
)
async def dogrudan_zimmet_reddet(
    payload: DevirAliciOnayiCreate,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionResponse:
    transaction = await TransactionService.dogrudan_zimmet_reddet(
        db_session=db_session,
        transaction_id=payload.transaction_id,
        alici_uye_id=current_user.id,
    )
    await db_session.commit()
    await db_session.refresh(transaction)
    return TransactionResponse.model_validate(transaction)
