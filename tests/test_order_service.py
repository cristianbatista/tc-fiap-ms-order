import pytest
from types import SimpleNamespace
from datetime import datetime
from app.service.order_service import OrderService
from app.domain.order import OrderCreate, OrderItem, OrderUpdate
from app.entity.order import OrderStatus


class MockOrderRepository:
    def __init__(self):
        self._data = {}
        self._id = 1

    def create(self, order: OrderCreate, total_amount: float):
        obj = SimpleNamespace(
            id=self._id,
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            items=[item.model_dump() for item in order.items],
            total_amount=total_amount,
            status=OrderStatus.PENDING,
            payment_id=None,
            created_at=datetime.utcnow(),
            updated_at=None
        )
        self._data[self._id] = obj
        self._id += 1
        return obj

    def get_by_id(self, order_id: int):
        return self._data.get(order_id)

    def get_all(self, skip: int = 0, limit: int = 100):
        return list(self._data.values())[skip:skip+limit]

    def get_by_status(self, status: OrderStatus):
        return [o for o in self._data.values() if o.status == status]

    def update(self, order_id: int, order_update: OrderUpdate):
        o = self._data.get(order_id)
        if not o:
            return None
        if order_update.status is not None:
            o.status = order_update.status
        if order_update.payment_id is not None:
            o.payment_id = order_update.payment_id
        o.updated_at = datetime.utcnow()
        return o

    def delete(self, order_id: int):
        return self._data.pop(order_id, None) is not None


@pytest.fixture
def mock_repo():
    return MockOrderRepository()


def test_create_order(mock_repo):
    service = OrderService(repository=mock_repo)

    order_data = OrderCreate(
        customer_name="John Doe",
        customer_email="john@example.com",
        items=[
            OrderItem(product_name="Product 1", quantity=2, unit_price=10.0),
            OrderItem(product_name="Product 2", quantity=1, unit_price=20.0)
        ]
    )

    order = service.create_order(order_data)

    assert order.id is not None
    assert order.customer_name == "John Doe"
    assert order.customer_email == "john@example.com"
    assert order.total_amount == 40.0
    assert order.status == OrderStatus.PENDING


def test_get_order(mock_repo):
    service = OrderService(repository=mock_repo)

    order_data = OrderCreate(
        customer_name="Jane Doe",
        customer_email="jane@example.com",
        items=[OrderItem(product_name="Product 1", quantity=1, unit_price=15.0)]
    )

    created_order = service.create_order(order_data)
    retrieved_order = service.get_order(created_order.id)

    assert retrieved_order is not None
    assert retrieved_order.id == created_order.id
    assert retrieved_order.customer_name == "Jane Doe"


def test_update_order(mock_repo):
    service = OrderService(repository=mock_repo)

    order_data = OrderCreate(
        customer_name="Bob Smith",
        customer_email="bob@example.com",
        items=[OrderItem(product_name="Product 1", quantity=1, unit_price=10.0)]
    )

    order = service.create_order(order_data)

    update_data = OrderUpdate(status=OrderStatus.CONFIRMED, payment_id="PAY123")
    updated_order = service.update_order(order.id, update_data)

    assert updated_order is not None
    assert updated_order.status == OrderStatus.CONFIRMED
    assert updated_order.payment_id == "PAY123"


def test_list_orders(mock_repo):
    service = OrderService(repository=mock_repo)

    # Create multiple orders
    for i in range(3):
        order_data = OrderCreate(
            customer_name=f"Customer {i}",
            customer_email=f"customer{i}@example.com",
            items=[OrderItem(product_name="Product", quantity=1, unit_price=10.0)]
        )
        service.create_order(order_data)

    orders = service.list_orders()
    assert len(orders) == 3


def test_cancel_order(mock_repo):
    service = OrderService(repository=mock_repo)

    order_data = OrderCreate(
        customer_name="Alice",
        customer_email="alice@example.com",
        items=[OrderItem(product_name="Product", quantity=1, unit_price=10.0)]
    )

    order = service.create_order(order_data)
    cancelled_order = service.cancel_order(order.id)

    assert cancelled_order is not None
    assert cancelled_order.status == OrderStatus.CANCELLED
