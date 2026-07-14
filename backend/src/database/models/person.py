from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from database.database import Base

class PersonOrm(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    hashpassword: Mapped[str] = mapped_column(String(72))
    email: Mapped[Optional[str]] =  mapped_column(String(50), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(15), unique=True)

    def __eq__ (self, other):
        if not isinstance(other, type(self)):
            return False

        if getattr(self, "id") != getattr(other, "id"):
            return False

        return True