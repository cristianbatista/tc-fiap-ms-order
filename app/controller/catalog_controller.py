from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.infra.repository.product_repository import ProductRepository
from app.service.catalog_service import CatalogService
from app.domain.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/api/v1/catalog", tags=["catalog"])


def get_catalog_service(db: Session = Depends(get_db)) -> CatalogService:
    repo = ProductRepository(db)
    return CatalogService(repo)


@router.get("/", response_model=List[ProductResponse])
def list_catalog(skip: int = 0, limit: int = 100, service: CatalogService = Depends(get_catalog_service)):
    return service.list_products(skip, limit)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, service: CatalogService = Depends(get_catalog_service)):
    return service.create_product(payload)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, service: CatalogService = Depends(get_catalog_service)):
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
