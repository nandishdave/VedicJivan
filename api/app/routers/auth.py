from bson import ObjectId
from fastapi import APIRouter, Depends

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import (
    TokenRefresh,
    TokenResponse,
    UserCreate,
    UserInDB,
    UserLogin,
    UserResponse,
)
from app.utils.exceptions import BadRequestError, UnauthorizedError
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserCreate):
    db = get_db()

    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise BadRequestError("Email already registered")

    user = UserInDB(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        phone=data.phone,
    )

    result = await db.users.insert_one(user.model_dump())
    user_id = str(result.inserted_id)

    return TokenResponse(
        access_token=create_access_token({"sub": user_id}),
        refresh_token=create_refresh_token({"sub": user_id}),
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    db = get_db()

    user = await db.users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise UnauthorizedError("Invalid email or password")

    user_id = str(user["_id"])

    return TokenResponse(
        access_token=create_access_token({"sub": user_id}),
        refresh_token=create_refresh_token({"sub": user_id}),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: TokenRefresh):
    payload = decode_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise UnauthorizedError("Invalid refresh token")

    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise UnauthorizedError("User not found")

    user_id = str(user["_id"])

    return TokenResponse(
        access_token=create_access_token({"sub": user_id}),
        refresh_token=create_refresh_token({"sub": user_id}),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(current_user["id"])})

    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        phone=user.get("phone", ""),
        role=user["role"],
        created_at=user["created_at"],
    )
