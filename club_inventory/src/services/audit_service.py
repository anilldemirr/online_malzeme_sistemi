from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.audit_log import AuditLog


async def log_action(
    db_session: AsyncSession,
    entity_type: str,
    entity_id: str | int,
    user_id: int | None,
    action: str,
    previous_state: dict[str, Any] | None = None,
    new_state: dict[str, Any] | None = None,
) -> AuditLog:
    log_entry = AuditLog(
        entity_type=entity_type,
        entity_id=str(entity_id),
        user_id=user_id,
        action=action,
        previous_state=previous_state,
        new_state=new_state,
    )
    db_session.add(log_entry)
    await db_session.flush()
    return log_entry


class AuditService:
    @staticmethod
    async def log_action(
        db_session: AsyncSession,
        entity_type: str,
        entity_id: str | int,
        user_id: int | None,
        action: str,
        previous_state: dict[str, Any] | None = None,
        new_state: dict[str, Any] | None = None,
    ) -> AuditLog:
        return await log_action(
            db_session=db_session,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            action=action,
            previous_state=previous_state,
            new_state=new_state,
        )
