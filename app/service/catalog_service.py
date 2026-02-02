from typing import List
from app.infra.repository.product_repository import ProductRepository
from app.domain.product import ProductCreate, ProductResponse
from app.entity.product import ProductEntity


class CatalogService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_products(self, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        entities = self.repository.list_all(skip, limit)
        return [ProductResponse.from_orm(e) for e in entities]

    def create_product(self, data: ProductCreate) -> ProductResponse:
        entity = ProductEntity(
            sku=data.sku,
            name=data.name,
            description=data.description,
            price=data.price,
            image_url=str(data.image_url) if data.image_url else None,
            category=data.category
        )
        created = self.repository.create(entity)
        return ProductResponse.from_orm(created)

    def get_product(self, product_id: int) -> ProductResponse | None:
        entity = self.repository.get_by_id(product_id)
        return ProductResponse.from_orm(entity) if entity else None
