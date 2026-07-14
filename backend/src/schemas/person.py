from pydantic import BaseModel, Field, ConfigDict

class PersonSchema(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: str | None = Field(None, min_length=3, max_length=50)
    phone: str | None = Field(None, min_length=5, max_length=15)

    model_config = ConfigDict(from_attributes=True, extra='ignore')

class PersonResponseSchema(PersonSchema):
    id: int

    model_config = ConfigDict(from_attributes=True, extra='ignore')

class PersonLoginSchema(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    password: str = Field(max_length=72)
