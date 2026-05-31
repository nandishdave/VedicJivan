"""Auth HTTP layer — thin Depends-driven router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.dependencies import (
    get_current_user,
    get_user_repository,
)
from app.models.user import (
    TokenRefresh,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.repositories.user_repository import UserRepository
from app.use_cases.auth import (
    GetMyProfile,
    LoginUser,
    RefreshTokens,
    RegisterUser,
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])


# ── Use-case factories ────────────────────────────────────────────────────


def _register_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> RegisterUser:
    return RegisterUser(repo)


def _login_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> LoginUser:
    return LoginUser(repo)


def _refresh_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> RefreshTokens:
    return RefreshTokens(repo)


def _profile_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> GetMyProfile:
    return GetMyProfile(repo)


# ── Endpoints ────────────────────────────────────────────────────────────


@router.post("/register", response_model=TokenResponse)
async def register(
    data: UserCreate,
    use_case: RegisterUser = Depends(_register_use_case),
):
    access, refresh = await use_case.execute(
        name=data.name, email=data.email, password=data.password, phone=data.phone
    )
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLogin,
    use_case: LoginUser = Depends(_login_use_case),
):
    access, refresh = await use_case.execute(email=data.email, password=data.password)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: TokenRefresh,
    use_case: RefreshTokens = Depends(_refresh_use_case),
):
    access, refresh = await use_case.execute(refresh_token=data.refresh_token)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: dict = Depends(get_current_user),
    use_case: GetMyProfile = Depends(_profile_use_case),
):
    return await use_case.execute(user_id=current_user["id"])
