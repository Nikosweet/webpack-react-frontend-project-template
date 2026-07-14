from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.category import CategorySchema, CategoryResponseSchema
from services.categories_service import CategoriesService
from database.models.category import CategoryOrm
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session

class CategoryController:
    def __init__(self):
        self.router = APIRouter(prefix="/categories", tags=["categories"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/", response_model=List[CategoryResponseSchema])
        async def get_all(session: AsyncSession = Depends(get_session)):
            categories = await CategoriesService.get_all(session)
            for category in categories:
                category = CategoryResponseSchema.model_validate(category)
            return categories

        @self.router.get("/{category_id}", response_model=CategoryResponseSchema)
        async def get(category_id: int, session: AsyncSession = Depends(get_session)):
            try:
                category = await CategoriesService.get(category_id, session)
                return CategoryResponseSchema.model_validate(category)
            except HTTPException:
                raise

        @self.router.post("/", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
        async def create(category: CategorySchema, session: AsyncSession = Depends(get_session)):
            try:
                category = await CategoriesService.create(category, session)
                return CategoryResponseSchema.model_validate(category)
            except HTTPException:
                raise

        @self.router.delete("/{category_id}", response_model=bool)
        async def delete(category_id: int, session: AsyncSession = Depends(get_session)):
            try:
                return await CategoriesService.delete(category_id, session)
            except HTTPException:
                raise
        
        @self.router.put("/{category_id}", response_model=CategoryResponseSchema)
        async def update(category_id: int, category: CategorySchema, session: AsyncSession = Depends(get_session)):
            try:
                category = await CategoriesService.update(category_id, category, session)
                return CategoryResponseSchema.model_validate(category)
            except HTTPException:
                raise