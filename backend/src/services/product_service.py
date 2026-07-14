from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.product import ProductOrm
from schemas.product import ProductSchema

class ProductService:
    @classmethod
    async def get_all(cls, session: AsyncSession):
        stmt = select(ProductOrm)
        products = await session.execute(stmt)
        return products.scalars().all()

    @classmethod
    async def get(cls, product_id: int, session: AsyncSession):
        stmt = select(ProductOrm).where(product_id == ProductOrm.id)
        res = await session.execute(stmt)
        product = res.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='product not found')
        return product
        

    @classmethod
    async def create(cls, product: ProductSchema, session: AsyncSession):
        stmt = select(ProductOrm).where(product.slug == ProductOrm.slug)
        res = await session.execute(stmt)
        product = res.scalar_one_or_none()
        if product:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Slug already exists')
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    @classmethod
    async def delete(cls, product_id: int, session: AsyncSession) -> bool:
        try:
            product = await cls.get(product_id, session)
            session.delete(product)
            await session.commit()
            return True
        except HTTPException:
            raise


    @classmethod
    async def update(cls, product_id: int, new_data: ProductSchema, session: AsyncSession):
        try:
            product = await cls.get(product_id, session)
            update_data = new_data.dict(exclude_unset=True)

            for key, value in update_data.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            session.add(product)
            await session.commit()
            await session.refresh(product)

            return product
        except HTTPException:
            raise