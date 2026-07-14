
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from database.database import Base



class CategoryOrm(Base):
    __tablename__ = "categories"


    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete='SET NULL'))
    product_associations: Mapped[List["ProductOrm"]] = relationship(back_populates="category_associations", secondary="product_categories")

    parent: Mapped[Optional["CategoryOrm"]] = relationship(remote_side=[id], back_populates='children', foreign_keys=[parent_id])

    children: Mapped[List["CategoryOrm"]] = relationship(back_populates='parent', foreign_keys=[parent_id])