from pydantic import BaseModel


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
