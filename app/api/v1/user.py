from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from app.api.schemas.token import RefreshTokenResponseSchema, TokenResponseSchema
from app.api.schemas.user import UserRegisterSchema, UserResponseSchema
from app.services.auth import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
)
from app.services.exceptions.user import InvalidCredentialsError, UserNotFoundError
from app.services.user import BaseUserService, get_user_service

router = APIRouter(prefix="/api/v1", tags=["Users"])


@router.post("/register", response_model=UserResponseSchema)
async def register(
    user: UserRegisterSchema,
    user_service: BaseUserService = Depends(get_user_service),
):
    try:
        new_user = await user_service.register_user(
            user.username, user.email, user.password
        )

        return UserResponseSchema(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            role=new_user.role.value,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exist",
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponseSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: BaseUserService = Depends(get_user_service),
):
    try:
        authenticated_user = await user_service.authenticate_user(
            form_data.username, form_data.password
        )
        access_token = create_access_token(
            data={
                "sub": authenticated_user.username,
                "role": authenticated_user.role.value,
            }
        )
        refresh_token = create_refresh_token(
            data={
                "sub": authenticated_user.username,
                "role": authenticated_user.role.value,
            }
        )

        return TokenResponseSchema(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )
    except (UserNotFoundError, InvalidCredentialsError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during login",
        )


@router.post("/refresh", response_model=RefreshTokenResponseSchema)
async def refresh_token(refresh_token: str):
    try:
        payload = decode_access_token(refresh_token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_access_token = create_access_token(
            data={"sub": payload["sub"], "role": payload["role"]}
        )

        return RefreshTokenResponseSchema(
            access_token=new_access_token, token_type="bearer"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during token refresh {e}",
        )
