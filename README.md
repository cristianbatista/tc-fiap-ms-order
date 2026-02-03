# MS-Order - Order Management Microservice

Microservice for managing orders in a food service system.

## Architecture

This project follows Clean Architecture principles with clear separation of concerns:

- **config**: Application configuration and database setup
- **entity**: Database models (SQLAlchemy ORM)
- **domain**: Business models (Pydantic schemas)
- **infra/repository**: Data access layer
- **service**: Business logic layer
- **controller**: API endpoints (FastAPI routes)
- **tests**: Unit and integration tests

## Technologies

- **Python 3.11**
- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database
- **Alembic**: Database migrations
- **Pytest**: Testing framework
- **Docker**: Containerization

## Features

- Create orders with multiple items
- Retrieve order details
- List all orders with pagination
- Filter orders by status
- Update order status
- Confirm orders after payment
- Cancel orders
- API documentation with Swagger UI

## Order Status Flow

```
PENDING → CONFIRMED → PREPARING → READY → DELIVERED
   ↓
CANCELLED
```

## API Endpoints

### Orders

- `POST /api/v1/orders/` - Create a new order
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `GET /api/v1/orders/` - List all orders
- `GET /api/v1/orders/status/{status}` - List orders by status
- `PATCH /api/v1/orders/{order_id}` - Update order
- `POST /api/v1/orders/{order_id}/confirm` - Confirm order
- `POST /api/v1/orders/{order_id}/cancel` - Cancel order
- `DELETE /api/v1/orders/{order_id}` - Delete order

### Health Check

- `GET /health` - Health check endpoint
- `GET /` - Service information

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Docker & Docker Compose (optional)

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the service:
```bash
uvicorn app.main:app --reload --port 8001
```

5. Access API documentation:
- Swagger UI: http://localhost:8001/api/docs
- ReDoc: http://localhost:8001/api/redoc

### Docker

Build and run with Docker:
```bash
docker build -t ms-order .
docker run -p 8001:8001 ms-order
```

## Testing

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## API Usage Examples

### Create Order

```bash
curl -X POST "http://localhost:8001/api/v1/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "items": [
      {
        "product_name": "Burger",
        "quantity": 2,
        "unit_price": 15.50
      },
      {
        "product_name": "Fries",
        "quantity": 1,
        "unit_price": 8.00
      }
    ]
  }'
```

### Get Order

```bash
curl -X GET "http://localhost:8001/api/v1/orders/1"
```

### List Orders

```bash
curl -X GET "http://localhost:8001/api/v1/orders/?skip=0&limit=10"
```

### Confirm Order

```bash
curl -X POST "http://localhost:8001/api/v1/orders/1/confirm?payment_id=PAY123"
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://order_user:order_pass@localhost:5432/order_db |
| SERVICE_NAME | Service name | ms-order |
| SERVICE_PORT | Service port | 8001 |

## License

MIT

## CI / GitHub Actions

The repository includes a GitHub Actions workflow at `.github/workflows/ci.yml` which runs on pushes and pull requests to `main`.

- Job `install`: builds wheels from `requirements.txt` and uploads them as an artifact named `wheelhouse`.
- Job `test`: downloads the wheels, installs dependencies, runs `pytest` and uploads test artifacts (JUnit XML, `coverage.xml` and the HTML coverage folder).

Where to find artifacts on GitHub:

1. Open the repository on GitHub and go to the `Actions` tab.
2. Select the workflow run you want to inspect.
3. Expand the `install` or `test` job to see logs.
4. In the workflow run page, open the `Artifacts` dropdown (top-right) to download artifacts such as `wheelhouse` or `test-artifacts`.

Artifact contents produced by the workflow:

- `wheelhouse` — pre-built wheels for offline installation.
- `test-artifacts` — contains `reports/junit.xml`, `coverage.xml` and the `coverage_html/` folder (HTML coverage report).

Viewing coverage locally from an artifact:

1. Download and unzip the `test-artifacts` artifact from the workflow run.
2. Open `coverage_html/index.html` in a browser to see the full HTML coverage report.

Run the same commands locally (simulate CI):

```bash
# build wheels
mkdir -p wheelhouse
python -m pip install --upgrade pip
pip install wheel
pip wheel -r requirements.txt -w wheelhouse

# install from wheels
python -m pip install --upgrade pip
pip install --no-index --find-links=wheelhouse -r requirements.txt

# run tests and generate coverage + junit
python -m pip install pytest pytest-cov
mkdir -p reports
pytest --maxfail=1 --disable-warnings -q \
  --junitxml=reports/junit.xml \
  --cov=app \
  --cov-report=xml:coverage.xml \
  --cov-report=html:coverage_html \
  --cov-report=term

# open the HTML report
open coverage_html/index.html
```

If you want additional reporting (e.g., upload to Codecov) tell me and I can add that to the workflow.
