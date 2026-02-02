from sqlalchemy import Column, Integer, String, Float, DateTime, JSON as SAJSON
from sqlalchemy.sql import func
import enum
from app.config.database import Base


class OrderStatus(str, enum.Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderEntity(Base):
    """Order entity model"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    items = Column(SAJSON, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default=OrderStatus.PENDING.value, nullable=False)
    payment_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
