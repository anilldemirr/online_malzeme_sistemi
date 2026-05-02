from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


from src.models.audit_log import AuditLog  # noqa: E402,F401
from src.models.equipment import EquipmentItem, EquipmentModel, StagedEquipment  # noqa: E402,F401
from src.models.transaction import Transaction  # noqa: E402,F401
from src.models.user import User  # noqa: E402,F401
