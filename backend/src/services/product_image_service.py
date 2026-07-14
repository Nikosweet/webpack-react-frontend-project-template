from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.product_images import ProductImageOrm

class ProductImageService:
    @classmethod
    async def get_all(cls, session: AsyncSession):
        stmt = select(ProductImageOrm)
        res = await session.execute(stmt)
        images = res.scalars().all()
        return images

    @classmethod
    async def get(cls, image_id: int, session: AsyncSession):
        stmt = select(ProductImageOrm).where(image_id == ProductImageOrm.id)
        res = await session.execute(stmt)
        image = res.scalar_one_or_none()
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='image not found')
        return image

    @classmethod
    async def create(cls, image, session: AsyncSession):
        stmt = select(ProductImageOrm).where(image.url == ProductImageOrm.url)
        res = await session.execute(stmt)
        if res:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Image already exists')
        session.add(image)
        await session.commit()
        await session.refresh(image)
        return image

    @classmethod
    async def delete(cls, image_id: int, session: AsyncSession) -> bool:
        try:
            image = cls.get(image_id, session)
            session.delete(image)
            session.commit()
            return True
        except HTTPException:
            raise

    @classmethod
    async def update(cls, image_id: int, new_data, session: AsyncSession):
        try:
            image = cls.get(image_id)
            update_data = new_data.dict(exclude_unset=True)

            for key, value in update_data.items():
                if hasattr(image, key):
                    setattr(image, key, value)
            session.add(image)
            await session.commit()
            await session.refresh(image)

            return image
        except HTTPException:
            raise
