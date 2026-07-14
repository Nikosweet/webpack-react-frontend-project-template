from pydantic import Field, ConfigDict, BaseModel

class CategorySchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    slug: str = Field(min_length=2, max_length=50)
    parent_id: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True, extra='ignore')


class CategoryResponseSchema(CategorySchema):
    id: int

    model_config = ConfigDict(from_attributes=True, extra='ignore')

