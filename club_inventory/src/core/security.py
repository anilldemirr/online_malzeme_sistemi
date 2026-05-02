from src.models.user import UserRole


def is_manager(role: UserRole) -> bool:
    return role == UserRole.MANAGER
