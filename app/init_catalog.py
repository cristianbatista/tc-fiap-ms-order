import json
import logging
from app.config.settings import get_settings
from app.config.database import SessionLocal
from app.infra.repository.product_repository import ProductRepository
from app.entity.product import ProductEntity

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format=settings.log_format
)
logger = logging.getLogger(__name__)

# Example base catalog; replace/extend using frontend existing catalog as base
BASE_CATALOG = [
    {"sku": "XBURGER-001", "name": "X-Burger Clássico", "description": "Pão, carne, queijo", "price": 25.90, "image_url": None, "category": "burgers"},
    {"sku": "XBACON-001", "name": "X-Bacon", "description": "Pão, carne, bacon, queijo", "price": 28.90, "image_url": None, "category": "burgers"},
    {"sku": "XTUDO-001", "name": "X-Tudo", "description": "Pão, carne, bacon, ovo, queijo, salada", "price": 32.90, "image_url": None, "category": "burgers"},
    {"sku": "FRIES-001", "name": "Batata Frita", "description": "Porção média crocante", "price": 12.90, "image_url": None, "category": "sides"},
    {"sku": "SODA-001", "name": "Refrigerante 350ml", "description": "Coca-Cola gelada", "price": 6.90, "image_url": None, "category": "drinks"},
    {"sku": "JUICE-001", "name": "Suco Natural", "description": "Suco de frutas 300ml", "price": 8.90, "image_url": None, "category": "drinks"}
]


def seed_catalog():
    """Initialize catalog with base products"""
    if not settings.init_catalog:
        logger.info("🚫 Catalog initialization disabled by configuration")
        return
        
    logger.info("🎯 Starting catalog initialization...")
    
    db = SessionLocal()
    repo = ProductRepository(db)
    
    try:
        products_added = 0
        products_skipped = 0
        
        for p in BASE_CATALOG:
            try:
                existing_product = repo.get_by_sku(p["sku"])
                if not existing_product:
                    entity = ProductEntity(
                        sku=p["sku"],
                        name=p["name"],
                        description=p.get("description"),
                        price=p["price"],
                        image_url=p.get("image_url"),
                        category=p.get("category")
                    )
                    repo.create(entity)
                    products_added += 1
                    logger.debug(f"➕ Added product: {p['name']}")
                else:
                    products_skipped += 1
                    logger.debug(f"⏭️  Skipped existing product: {p['name']}")
            except Exception as e:
                logger.error(f"❌ Error adding product {p['name']}: {e}")
                
        logger.info(f"✅ Catalog initialization complete:")
        logger.info(f"   📦 Products added: {products_added}")
        logger.info(f"   ⏭️  Products skipped: {products_skipped}")
        logger.info(f"   📋 Total products in catalog: {products_added + products_skipped}")
        
    except Exception as e:
        logger.error(f"❌ Catalog initialization failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_catalog()
