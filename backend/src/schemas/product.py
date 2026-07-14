from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class ProductSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    slug: str = Field(min_length=2, max_length=50)
    description: str | None
    price: Decimal = Field(gt=1, lt=100000000)
    brand: str = Field(min_length=2, max_length=50)

    is_active: bool
    specifications: dict

    model_config = ConfigDict(from_attributes=True, extra='ignore')


class ProductResponseSchema(ProductSchema):
    id: int
    rating: float = Field(ge=0, le=5)
    review_count: int = Field(ge=0)
    sku: str = Field(min_length=1, max_length=50)

    model_config = ConfigDict(from_attributes=True, extra='ignore')







