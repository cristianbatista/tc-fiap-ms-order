from typing import List, Optional
from sqlalchemy.orm import Session
from app.entity.product import ProductEntity


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: ProductEntity) -> ProductEntity:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def list_all(self, skip: int = 0, limit: int = 100) -> List[ProductEntity]:
        return self.db.query(ProductEntity).offset(skip).limit(limit).all()

    def get_by_id(self, product_id: int) -> Optional[ProductEntity]:
        return self.db.query(ProductEntity).filter(ProductEntity.id == product_id).first()

    def get_by_sku(self, sku: str) -> Optional[ProductEntity]:
        return self.db.query(ProductEntity).filter(ProductEntity.sku == sku).first()
