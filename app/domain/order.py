from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    """Order item model"""
    product_name: str = Field(..., min_length=1, max_length=255)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderCreate(BaseModel):
    """Order creation model"""
    customer_name: str = Field(..., min_length=1, max_length=255)
    customer_email: EmailStr
    items: List[OrderItem] = Field(..., min_items=1)


class OrderUpdate(BaseModel):
    """Order update model"""
    status: Optional[OrderStatus] = None
    payment_id: Optional[str] = None


class OrderResponse(BaseModel):
    """Order response model"""
    id: int
    customer_name: str
    customer_email: str
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    payment_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
