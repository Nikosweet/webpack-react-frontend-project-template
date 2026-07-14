
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from database.database import Base
from database.models.product import ProductOrm
from database.models.category import CategoryOrm

class ProductCategoryOrm(Base):

    __tablename__ = "product_categories"

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)