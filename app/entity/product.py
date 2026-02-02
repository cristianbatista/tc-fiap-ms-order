from sqlalchemy import Column, Integer, String, Text, Float
from app.config.database import Base


class ProductEntity(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String(1024), nullable=True)
    category = Column(String(128), nullable=True)
