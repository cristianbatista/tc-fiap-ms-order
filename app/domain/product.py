from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class ProductCreate(BaseModel):
    sku: str = Field(..., example="XBURGER-001")
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[HttpUrl] = None
    category: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[HttpUrl]
    category: Optional[str]

    class Config:
        from_attributes = True
