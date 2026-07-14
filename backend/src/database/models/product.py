
from sqlalchemy import  String, ForeignKey, DECIMAL, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal
from database.database import Base
from typing import List
from database.models.category import CategoryOrm

class ProductOrm(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True)
    brand: Mapped[str] = mapped_column(String(50))

    rating: Mapped[float] = mapped_column(server_default='0.0')
    review_count: Mapped[int] = mapped_column(server_default='0')
    is_active: Mapped[bool] = mapped_column(server_default='true')

    specifications: Mapped[dict | None] = mapped_column(JSON, server_default='{}')

    category_associations: Mapped[List["CategoryOrm"]] = relationship(back_populates="product_associations", secondary="product_categories")

    images: Mapped[List["ProductImageOrm"]] = relationship(back_populates="product", cascade="all, delete-orphan",order_by="ProductImageOrm.sort_order")



    