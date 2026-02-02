from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.order import OrderCreate, OrderUpdate, OrderResponse
from app.infra.repository.order_repository import OrderRepository
from app.entity.order import OrderStatus


class OrderService:
    """Service for order business logic"""
    
    def __init__(self, db: Optional[Session] = None, repository: Optional[OrderRepository] = None):
        """Create service with either a DB session or an explicit repository.

        Accepting a repository allows unit tests to inject a mock repository
        and avoid any database dependency.
        """
        if repository is not None:
            self.repository = repository
        else:
            if db is None:
                raise ValueError("Either db or repository must be provided")
            self.repository = OrderRepository(db)
    
    def create_order(self, order: OrderCreate) -> OrderResponse:
        """Create a new order"""
        # Calculate total amount
        total_amount = sum(item.quantity * item.unit_price for item in order.items)
        
        # Create order
        db_order = self.repository.create(order, total_amount)
        return OrderResponse.model_validate(db_order)
    
    def get_order(self, order_id: int) -> Optional[OrderResponse]:
        """Get order by ID"""
        db_order = self.repository.get_by_id(order_id)
        if not db_order:
            return None
        return OrderResponse.model_validate(db_order)
    
    def list_orders(self, skip: int = 0, limit: int = 100) -> List[OrderResponse]:
        """List all orders with pagination"""
        db_orders = self.repository.get_all(skip, limit)
        return [OrderResponse.model_validate(order) for order in db_orders]
    
    def list_orders_by_status(self, status: OrderStatus) -> List[OrderResponse]:
        """List orders by status"""
        db_orders = self.repository.get_by_status(status)
        return [OrderResponse.model_validate(order) for order in db_orders]
    
    def update_order(self, order_id: int, order_update: OrderUpdate) -> Optional[OrderResponse]:
        """Update an order"""
        db_order = self.repository.update(order_id, order_update)
        if not db_order:
            return None
        return OrderResponse.model_validate(db_order)
    
    def confirm_order(self, order_id: int, payment_id: str) -> Optional[OrderResponse]:
        """Confirm order after payment"""
        update = OrderUpdate(status=OrderStatus.CONFIRMED, payment_id=payment_id)
        return self.update_order(order_id, update)
    
    def cancel_order(self, order_id: int) -> Optional[OrderResponse]:
        """Cancel an order"""
        update = OrderUpdate(status=OrderStatus.CANCELLED)
        return self.update_order(order_id, update)
    
    def delete_order(self, order_id: int) -> bool:
        """Delete an order"""
        return self.repository.delete(order_id)
