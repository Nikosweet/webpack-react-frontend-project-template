from authx import AuthX, AuthXConfig, TokenPayload
import bcrypt
from datetime import timedelta
from fastapi import Request, Response, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_settings import BaseSettings, SettingsConfigDict
from schemas.person import PersonSchema, PersonLoginSchema, PersonResponseSchema
from database.models.person import PersonOrm
from services.person_service import PersonService
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ENV_PATH = BASE_DIR / ".env"

class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str

    @property
    def get_secret_key(self):
        return str(self.JWT_SECRET_KEY)

    model_config = SettingsConfigDict(env_file=f'{ENV_PATH}', extra='ignore')

class AuthService:
    config = AuthXConfig()
    config.JWT_SECRET_KEY=JWTSettings().get_secret_key
    config.JWT_COOKIE_CSRF_PROTECT = False


    config.JWT_ACCESS_COOKIE_NAME='access_token'
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)

    config.JWT_REFRESH_COOKIE_NAME='refresh_token'
    config.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    config.JWT_TOKEN_LOCATION=["cookies"]
    config.JWT_ACCESS_COOKIE_NAME="access_token"
    config.JWT_REFRESH_COOKIE_NAME='refresh_token'
    config.JWT_COOKIE_MAX_AGE = timedelta(minutes=15)


    security = AuthX(config=config)


    @classmethod
    async def verify(cls, person_data: PersonLoginSchema, session: AsyncSession) -> PersonOrm:
        stmt = select(PersonOrm).where(PersonOrm.name == person_data.name)
        person = await session.execute(stmt)
        person = person.scalar_one_or_none()

        if not person:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

        is_valid = bcrypt.checkpw(
            person_data.password.encode('utf-8'),
            person.hashpassword.encode('utf-8')
        )
        if is_valid:
            return PersonResponseSchema.model_validate(person)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    
    @classmethod
    async def login(cls, creds: PersonLoginSchema, response: Response, session: AsyncSession):
        try: 
            person = await cls.verify(creds, session)

            access_token = cls.security.create_access_token(uid=str(person.id))
            cls.security.set_access_cookies(access_token, response)

            refresh_token = cls.security.create_refresh_token(uid=str(person.id))
            cls.security.set_refresh_cookies(refresh_token, response)

            return {"token_type": "bearer", "access_token": access_token, "refresh_token": refresh_token, "uid": person.id}

        except HTTPException:
            raise


    @classmethod
    async def refresh(cls, payload: TokenPayload, response: Response, session: AsyncSession):
        try:
            access_token = cls.security.create_access_token(uid=payload.sub)
            cls.security.set_access_cookies(access_token, response)
            return {"access_token": access_token}
        except HTTPException:
            raise

    @classmethod
    async def logout(cls, response: Response, session: AsyncSession):
        try:
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return {"message": "Successfully logged out"}
        except HTTPException:
            raise