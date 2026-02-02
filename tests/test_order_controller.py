from app.main import app
from app.controller.order_controller import create_order, get_order, list_orders
from app.service.order_service import OrderService
from app.domain.order import OrderCreate, OrderItem
from types import SimpleNamespace
from datetime import datetime


def _make_inmemory_service():
    # reuse simple in-memory repo via a lightweight service wrapper
    class InMemoryRepo:
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
                status="pending",
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

        def update(self, order_id: int, order_update):
            o = self._data.get(order_id)
            if not o:
                return None
            if getattr(order_update, "status", None) is not None:
                o.status = order_update.status
            if getattr(order_update, "payment_id", None) is not None:
                o.payment_id = order_update.payment_id
            o.updated_at = datetime.utcnow()
            return o

        def delete(self, order_id: int):
            return self._data.pop(order_id, None) is not None

    repo = InMemoryRepo()
    return OrderService(repository=repo)


def test_create_order_endpoint():
    """Unit test for create_order controller using in-memory service"""
    svc = _make_inmemory_service()
    order_model = OrderCreate(
        customer_name="John Doe",
        customer_email="john@example.com",
        items=[OrderItem(product_name="Product 1", quantity=2, unit_price=10.0)]
    )

    resp = create_order(order_model, service=svc)
    assert resp.customer_name == "John Doe"
    assert resp.total_amount == 20.0


def test_get_order_endpoint():
    """Unit test for get_order controller using in-memory service"""
    svc = _make_inmemory_service()
    order_model = OrderCreate(
        customer_name="Jane Doe",
        customer_email="jane@example.com",
        items=[OrderItem(product_name="Product 1", quantity=1, unit_price=15.0)]
    )

    created = create_order(order_model, service=svc)
    order_id = created.id

    resp = get_order(order_id, service=svc)
    assert resp.id == order_id
    assert resp.customer_name == "Jane Doe"


def test_list_orders_endpoint():
    """Unit test for list_orders controller using in-memory service"""
    svc = _make_inmemory_service()
    for i in range(3):
        order_model = OrderCreate(
            customer_name=f"Customer {i}",
            customer_email=f"customer{i}@example.com",
            items=[OrderItem(product_name="Product", quantity=1, unit_price=10.0)]
        )
        create_order(order_model, service=svc)

    results = list_orders(service=svc)
    assert len(results) == 3


def test_health_check_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
