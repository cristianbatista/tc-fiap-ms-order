from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.domain.order import OrderCreate, OrderUpdate, OrderResponse
from app.service.order_service import OrderService
from app.entity.order import OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    service: OrderService = Depends(get_order_service)
):
    """Create a new order"""
    return service.create_order(order)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service)
):
    """Get order by ID"""
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    return order


@router.get("/", response_model=List[OrderResponse])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    service: OrderService = Depends(get_order_service)
):
    """List all orders with pagination"""
    return service.list_orders(skip, limit)


@router.get("/status/{status}", response_model=List[OrderResponse])
def list_orders_by_status(
    status: OrderStatus,
    service: OrderService = Depends(get_order_service)
):
    """List orders by status"""
    return service.list_orders_by_status(status)


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    service: OrderService = Depends(get_order_service)
):
    """Update an order"""
    order = service.update_order(order_id, order_update)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    return order


@router.api_route("/{order_id}/confirm", methods=["POST", "PUT"], response_model=OrderResponse)
def confirm_order(
    order_id: int,
    payment_id: str | None = Query(None, alias="payment_id"),
    service: OrderService = Depends(get_order_service)
):
    """Confirm order after payment. Accepts POST (frontend) and PUT (compatibility).

    Expects `payment_id` as query parameter, e.g. ?payment_id=SIM-TXN-...
    """
    if not payment_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="payment_id query parameter is required")
    order = service.confirm_order(order_id, payment_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    return order


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    service: OrderService = Depends(get_order_service)
):
    """Cancel an order"""
    order = service.cancel_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    service: OrderService = Depends(get_order_service)
):
    """Delete an order"""
    if not service.delete_order(order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
