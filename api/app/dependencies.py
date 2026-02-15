from fastapi import Depends, Header

from app.database import get_db
from app.models.user import UserRole
from app.utils.exceptions import ForbiddenError, UnauthorizedError
from app.utils.security import decode_token


async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise UnauthorizedError("Invalid authorization header")

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise UnauthorizedError("Invalid or expired token")

    db = get_db()
    from bson import ObjectId

    user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise UnauthorizedError("User not found")

    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
    }


async def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != UserRole.ADMIN:
        raise ForbiddenError("Admin access required")
    return current_user
