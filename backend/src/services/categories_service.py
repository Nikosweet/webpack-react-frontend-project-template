from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 
from database.models.category import CategoryOrm
from schemas.category import CategorySchema

class CategoriesService:
    @classmethod
    async def get_all(cls, session: AsyncSession):
        stmt = select(CategoryOrm)
        res = await session.execute(stmt)
        categories = res.scalars().all()
        return categories

    @classmethod
    async def get(cls, category_id: int, session: AsyncSession):
        stmt = select(CategoryOrm).where(category_id == CategoryOrm.id)
        res = await session.execute(stmt)
        category = res.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
        return category

    @classmethod
    async def create(cls, category_data: CategorySchema, session: AsyncSession):
        stmt = select(CategoryOrm).where(category_data.name == CategoryOrm.name | category_data.slug == CategoryOrm.slug)
        category = await session.execute(stmt)
        if category.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Category already exists')
        newCategory = CategoryOrm(name=category_data.name, slug=category_data.slug)
        session.add(newCategory)
        await session.commit()
        await session.refresh(newCategory)
        return newCategory


    @classmethod
    async def delete(cls, category_id: int, session: AsyncSession) -> bool:
        try:
            category = await cls.get(category_id, session)
            session.delete(category)
            await session.commit()
            return True
        except HTTPException:
            raise


    @classmethod
    async def update(cls, category_id: int, new_data: CategorySchema, session: AsyncSession):
        try:
            category = await cls.get(category_id, session)
            update_data = new_data.dict(exclude_unset=True)

            for key, value in update_data.items():
                if hasattr(category, key):
                    setattr(category, key, value)
            session.add(category)
            await session.commit()
            await session.refresh(category)

            return category
        except HTTPException:
            raise