from typing import List, Optional
from sqlalchemy.orm import Session
from app.entity.order import OrderEntity, OrderStatus
from app.domain.order import OrderCreate, OrderUpdate


class OrderRepository:
    """Repository for order database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, order: OrderCreate, total_amount: float) -> OrderEntity:
        """Create a new order"""
        # store items as native Python list/dict so JSON/JSONB column stores structured data
        items_value = [item.dict() for item in order.items]

        db_order = OrderEntity(
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            items=items_value,
            total_amount=total_amount,
            status=OrderStatus.PENDING
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def get_by_id(self, order_id: int) -> Optional[OrderEntity]:
        """Get order by ID"""
        return self.db.query(OrderEntity).filter(OrderEntity.id == order_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[OrderEntity]:
        """Get all orders with pagination"""
        return self.db.query(OrderEntity).offset(skip).limit(limit).all()
    
    def get_by_status(self, status: OrderStatus) -> List[OrderEntity]:
        """Get orders by status"""
        return self.db.query(OrderEntity).filter(OrderEntity.status == status).all()
    
    def update(self, order_id: int, order_update: OrderUpdate) -> Optional[OrderEntity]:
        """Update an order"""
        db_order = self.get_by_id(order_id)
        if not db_order:
            return None
        
        if order_update.status is not None:
            db_order.status = order_update.status
        if order_update.payment_id is not None:
            db_order.payment_id = order_update.payment_id
        
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def delete(self, order_id: int) -> bool:
        """Delete an order"""
        db_order = self.get_by_id(order_id)
        if not db_order:
            return False
        
        self.db.delete(db_order)
        self.db.commit()
        return True
