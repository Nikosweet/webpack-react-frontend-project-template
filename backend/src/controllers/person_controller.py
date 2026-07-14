from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.person import PersonSchema, PersonResponseSchema, PersonLoginSchema
from services.person_service import PersonService
from database.models.person import PersonOrm
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session


class PersonController:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["users"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/", response_model=List[PersonResponseSchema])
        async def get_all(session: AsyncSession = Depends(get_session)):
            persons = await PersonService.get_all(session)
            for person in persons:
                person = PersonResponseSchema.model_validate(person)
            return persons


        @self.router.get("/{person_id}", response_model=PersonResponseSchema)
        async def get(person_id: int, session: AsyncSession = Depends(get_session)):
            try:
                person = await PersonService.get(person_id, session)
                return PersonResponseSchema.model_validate(person)
            except HTTPException:
                raise


        @self.router.post("/", response_model=PersonResponseSchema, status_code=status.HTTP_201_CREATED)
        async def create(person: PersonLoginSchema, session: AsyncSession = Depends(get_session)):
            try:
                person = await PersonService.create(person, session)
                return PersonResponseSchema.model_validate(person)
            except HTTPException:
                raise

        @self.router.delete("/{person_id}", response_model=bool)
        async def delete(person_id: int, session: AsyncSession = Depends(get_session)):
            try:
                return await PersonService.delete(person_id, session)
            except HTTPException:
                raise


        @self.router.put("/{person_id}", response_model=PersonResponseSchema)
        async def update(person_id: int, person: PersonSchema, session: AsyncSession = Depends(get_session)):
            try:
                person = await PersonService.update(person_id, person, session)
                return PersonResponseSchema.model_validate(person)
            except HTTPException:
                raise