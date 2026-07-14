from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base




class ProductImageOrm(Base):
    __tablename__ = 'product_images'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500), nullable='false', unique=True)
    is_main: Mapped[bool] = mapped_column(server_default='false')
    sort_order: Mapped[int] = mapped_column(server_default='0')
    alt_text: Mapped[str] = mapped_column(String(40))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), nullable=False)

    product: Mapped[Optional["ProductOrm"]] = relationship(back_populates='images')