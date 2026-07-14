from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.product import ProductSchema, ProductResponseSchema
from services.product_service import ProductService
from database.models.product import ProductOrm
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session

class ProductController:
    def __init__(self):
        self.router = APIRouter(prefix="/products", tags=["products"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/", response_model=List[ProductResponseSchema])
        async def get_all(session: AsyncSession = Depends(get_session)):
            products = await ProductService.get_all(session)
            for product in products:
                product = ProductResponseSchema.model_validate(product)
            return products

        @self.router.get("/{product_id}", response_model=ProductResponseSchema)
        async def get(product_id: int, session: AsyncSession = Depends(get_session)):
            try:
                product = await ProductService.get(product_id, session)
                return ProductResponseSchema.model_validate(product)
            except HTTPException:
                raise

        @self.router.post("/", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
        async def create(product: ProductSchema, session: AsyncSession = Depends(get_session)):
            try:
                product = await ProductService.create(product, session)
                return ProductResponseSchema.model_validate(product)
            except HTTPException:
                raise

        @self.router.delete("/{product_id}", response_model=bool)
        async def delete(product_id: int, session: AsyncSession = Depends(get_session)):
            try:
                return await ProductService.delete(product_id, session)
            except HTTPException:
                raise

        @self.router.put("/{product_id}", response_model=ProductResponseSchema)
        async def update(product_id: int, product: ProductSchema, session: AsyncSession = Depends(get_session)):
            try:
                product = await ProductService.update(product_id, product, session)
                return ProductResponseSchema.model_validate(product)
            except HTTPException:
                raise