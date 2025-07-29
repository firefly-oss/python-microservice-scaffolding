# Python Microservice Scaffolding

[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-1.10-E92063.svg?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache-yellow.svg)](https://opensource.org/licenses/Apache)

A production-ready FastAPI, Pydantic, and SQLAlchemy microservice template with built-in best practices for rapid development.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quickstart](#quickstart)
- [Project Structure](#project-structure)
- [Development Guide](#development-guide)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Microservice Tutorial](#microservice-tutorial)
- [Contributing](#contributing)
- [License](#license)

## Overview

This scaffolding provides a solid foundation for building modern, high-performance microservices with Python. It combines best practices from the Python ecosystem with a clean, modular architecture that promotes maintainability and scalability.

Key benefits:
- **Rapid Development**: Start building your business logic immediately with pre-configured infrastructure
- **Production-Ready**: Includes monitoring, logging, health checks, and containerization
- **Best Practices**: Follows modern Python development standards and design patterns
- **Scalable Architecture**: Clean separation of concerns with repository pattern and service layer

## Features

This scaffolding combines modern Python tools to provide a comprehensive foundation for building microservices:

### Core Components
- **FastAPI** - High-performance API framework with automatic OpenAPI documentation
- **Pydantic** - Data validation and settings management
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Poetry** - Dependency management
- **PostgreSQL** - Relational database
- **RestClient** - HTTP client for making REST API calls with Pydantic integration

### Development Tools
- **Pytest** - Testing framework with fixtures for FastAPI and SQLAlchemy
- **Black**, **isort**, **Flake8**, **mypy** - Code formatting and linting
- **pre-commit** - Git hooks for quality checks
- **Bandit**, **Safety** - Security scanning

### Observability
- **Prometheus** - Metrics collection
- **structlog** - Structured logging
- **Health checks** - Endpoints for monitoring

### DevOps
- **Docker** & **Docker Compose** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **Sphinx** - Documentation generation

## Quickstart

Get up and running in minutes with these simple steps:

### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Docker and Docker Compose (optional, for containerized deployment)
- PostgreSQL (automatically set up with Docker, or install separately)

### Installation

#### Option 1: Local Development Setup

```bash
# Clone the repository
git clone https://github.com/firefly-oss/python-microservice-scaffolding.git
cd python-microservice-scaffolding

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env file with your configuration

# Initialize the database and run migrations
poetry run python -m app.db.init

# Start the application with hot-reloading
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 2: Docker Setup (Recommended for Consistency)

```bash
# Clone the repository
git clone https://github.com/firefly-oss/python-microservice-scaffolding.git
cd python-microservice-scaffolding

# Build and start the containers
docker-compose up -d

# Check logs
docker-compose logs -f app

# To stop the services
docker-compose down
```

### Verify Your Installation

Once the application is running, you can verify it works correctly:

1. **API Documentation**: Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to see the interactive Swagger UI
2. **Health Check**: Visit [http://localhost:8000/health](http://localhost:8000/health) to verify the service is healthy
3. **Create a Resource**: Use the following curl command to create a new item:

```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Example Item", "description": "This is a test item"}'
```

4. **Retrieve Resources**: Get all items with:

```bash
curl -X GET "http://localhost:8000/api/v1/items/"
```

### Running Tests

The project includes a comprehensive test suite:

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=app --cov-report=term-missing

# Run specific test files
poetry run pytest tests/api/test_items.py

# Run tests with verbose output
poetry run pytest -v
```

### Development Tools

The project includes several tools to maintain code quality:

```bash
# Format code with Black
poetry run black app tests

# Sort imports with isort
poetry run isort app tests

# Run type checking with mypy
poetry run mypy app

# Run all pre-commit hooks
poetry run pre-commit run --all-files
```

## Project Structure

The project follows a clean, modular structure:

```
app/
├── api/                    # API endpoints
│   └── api_v1/             # API version 1
│       ├── endpoints/      # Resource endpoints (items.py, etc.)
│       └── api.py          # API router configuration
├── core/                   # Core modules
│   ├── config.py           # Application configuration
│   ├── logging.py          # Structured logging configuration
│   └── metrics.py          # Prometheus metrics configuration
├── repositories/          # Database repository operations
│   ├── base.py             # Base repository class with generic operations
│   └── item_repository.py  # Item-specific repository operations
├── db/                     # Database setup
│   ├── database.py         # SQLAlchemy setup
│   └── init_db.py          # Database initialization
├── models/                 # SQLAlchemy models
│   ├── base.py             # Base model with common fields
│   └── item.py             # Item model definition
├── schemas/                # Pydantic schemas
│   └── item.py             # Item schemas (Create, Update, etc.)
├── services/               # Service layer
│   └── item_service.py     # Item service with business logic
└── main.py                 # Application entry point

tests/                      # Test suite
├── api/                    # API tests
│   └── test_items.py       # Item endpoint tests
└── conftest.py             # Test fixtures

docs/                       # Documentation
.github/workflows/          # CI/CD pipeline
docker-compose.yml          # Docker Compose configuration
Dockerfile                  # Docker configuration
pyproject.toml              # Poetry dependencies and settings
.pre-commit-config.yaml     # Pre-commit hooks configuration
```

## Development Guide

This section provides detailed guidance on developing with this microservice scaffolding.

### Repository Operations

The scaffolding includes a powerful `CRUDRepository` base class that provides standard database operations for your models. It supports:

#### Pagination

The `get_multi` method supports pagination with optional metadata:

```python
# Basic pagination (returns just the items)
items = repository.get_multi(db, skip=0, limit=10)

# Pagination with metadata (returns items and pagination info)
items, pagination = repository.get_multi(db, skip=0, limit=10, with_pagination=True)
print(f"Total items: {pagination['total']}")
print(f"Has more: {pagination['has_more']}")
```

The pagination metadata includes:
- `total`: Total number of records
- `skip`: Number of records skipped
- `limit`: Maximum number of records returned
- `has_more`: Boolean indicating if there are more records

#### Filtering

The `filter` method allows filtering records by field values:

```python
# Filter items by a single field
active_items = repository.filter(db, filters={"is_active": True})

# Filter with multiple conditions
premium_active_items = repository.filter(
    db, 
    filters={"is_active": True, "is_premium": True}
)

# Filtering with pagination
items, pagination = repository.filter(
    db,
    filters={"category": "electronics"},
    skip=0,
    limit=10,
    with_pagination=True
)
```

#### Using in Service Layer

Here's how to use these features in your service layer:

```python
def get_items(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    with_pagination: bool = False,
    filters: Optional[Dict[str, Any]] = None
) -> Union[List[models.Item], Tuple[List[models.Item], Dict[str, Any]]]:
    """Get items with optional pagination and filtering."""
    if filters:
        return repositories.item.filter(
            db, filters=filters, skip=skip, limit=limit, with_pagination=with_pagination
        )
    return repositories.item.get_multi(
        db, skip=skip, limit=limit, with_pagination=with_pagination
    )
```

### Code Quality Tools

The project uses pre-commit hooks to enforce code quality standards:

```bash
# Install pre-commit hooks
poetry run pre-commit install

# Run checks manually
poetry run pre-commit run --all-files
```

Available checks:
- **Black** - Code formatting
- **isort** - Import sorting
- **Flake8** - Linting and style checking
- **mypy** - Static type checking
- **Bandit** - Security scanning

### Security Best Practices

Regularly scan your code and dependencies for vulnerabilities:

```bash
# Check dependencies for known vulnerabilities
poetry run safety check

# Scan code for security issues
poetry run bandit -r app

# Run both checks
make security-check  # If you've set up the Makefile
```

### Documentation

Generate and view the project documentation:

```bash
# Build documentation
cd docs
poetry run sphinx-build -b html source build

# View in browser
open build/index.html  # On macOS
xdg-open build/index.html  # On Linux
```

### Extending the Application

#### Creating a New Resource

Here's a complete example of adding a new "Product" resource:

1. **Create the SQLAlchemy model** (`app/models/product.py`):

```python
from sqlalchemy import Column, String, Float, Boolean, Text
from app.models.base import Base

class Product(Base):
    """Product model for storing product information"""
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
```

2. **Register the model** (`app/models/__init__.py`):

```python
from app.models.base import Base
from app.models.item import Item
from app.models.product import Product  # Add this line
```

3. **Create Pydantic schemas** (`app/schemas/product.py`):

```python
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    is_available: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None

class ProductInDBBase(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Product(ProductInDBBase):
    pass
```

4. **Register the schemas** (`app/schemas/__init__.py`):

```python
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.schemas.product import Product, ProductCreate, ProductUpdate  # Add this line
```

5. **Create repository operations** (`app/repositories/product_repository.py`):

```python
from typing import Optional, List, Dict, Any, Tuple, Union
from sqlalchemy.orm import Session

from app.repositories.base import CRUDRepository
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductRepository(CRUDRepository[Product, ProductCreate, ProductUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Product]:
        return db.query(self.model).filter(self.model.name == name).first()

    # Example of using the filter method
    def get_available_products(
        self, db: Session, *, skip: int = 0, limit: int = 100, with_pagination: bool = False
    ) -> Union[List[Product], Tuple[List[Product], Dict[str, Any]]]:
        """Get only available products with optional pagination metadata."""
        return self.filter(db, filters={"is_available": True}, skip=skip, limit=limit, with_pagination=with_pagination)

product = ProductRepository(Product)
```

6. **Register the repository module** (`app/repositories/__init__.py`):

```python
from app.repositories.item_repository import item
from app.repositories.product_repository import product  # Add this line
```

7. **Create a service module** (`app/services/product_service.py`):

```python
from typing import List, Optional
from sqlalchemy.orm import Session

from app import models, schemas
from app import repositories

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """Get multiple products with pagination."""
    return repositories.product.get_multi(db, skip=skip, limit=limit)

def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    """Create a new product."""
    return repositories.product.create(db=db, obj_in=product_in)

def get_product(db: Session, id: int) -> Optional[models.Product]:
    """Get a specific product by ID."""
    return repositories.product.get(db=db, id=id)

def update_product(
    db: Session, id: int, product_in: schemas.ProductUpdate
) -> Optional[models.Product]:
    """Update an existing product."""
    product = repositories.product.get(db=db, id=id)
    if not product:
        return None
    return repositories.product.update(db=db, db_obj=product, obj_in=product_in)

def delete_product(db: Session, id: int) -> Optional[models.Product]:
    """Delete a product."""
    product = repositories.product.get(db=db, id=id)
    if not product:
        return None
    return repositories.product.remove(db=db, id=id)
```

8. **Create API endpoints** (`app/api/api_v1/endpoints/products.py`):

```python
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db.database import get_db
from app.services import product_service

router = APIRouter()

@router.get("/", response_model=List[schemas.Product])
def read_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve products"""
    return product_service.get_products(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(get_db),
    product_in: schemas.ProductCreate,
) -> Any:
    """Create new product"""
    return product_service.create_product(db=db, product_in=product_in)

@router.get("/{id}", response_model=schemas.Product)
def read_product(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """Get product by ID"""
    product = product_service.get_product(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(get_db),
    id: int,
    product_in: schemas.ProductUpdate,
) -> Any:
    """Update a product"""
    product = product_service.update_product(db=db, id=id, product_in=product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{id}", response_model=schemas.Product)
def delete_product(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """Delete a product"""
    product = product_service.delete_product(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

9. **Register the router** (`app/api/api_v1/api.py`):

```python
from fastapi import APIRouter
from app.api.api_v1.endpoints import items, products  # Add products here

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(products.router, prefix="/products", tags=["products"])  # Add this line
```

### Testing

Write comprehensive tests for your new features:

```python
# tests/api/test_products.py
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import repositories
from app.schemas.product import ProductCreate

def test_create_product(client: TestClient, db: Session) -> None:
    data = {"name": "Test Product", "description": "Test Description", "price": 19.99}
    response = client.post("/api/v1/products/", json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["price"] == data["price"]
    assert "id" in content
```

### Continuous Integration

The project includes a GitHub Actions workflow that automatically:

- Sets up a PostgreSQL database for testing
- Installs dependencies
- Runs pre-commit hooks
- Executes tests with coverage reporting
- Uploads coverage reports to Codecov
- Performs security checks

You can view the workflow configuration in `.github/workflows/ci.yml`.

## REST Client

The scaffolding includes a powerful REST client for making HTTP requests to external services. It's built on top of `httpx` and integrates seamlessly with Pydantic for data validation and serialization/deserialization.

### Features

- Synchronous and asynchronous clients
- Automatic serialization/deserialization with Pydantic models
- Comprehensive error handling
- Retry mechanism
- Configurable timeouts and headers
- Support for all common HTTP methods (GET, POST, PUT, PATCH, DELETE)

### Basic Usage

```python
from app.core.rest_client import RestClient
from pydantic import BaseModel

# Define your data models
class User(BaseModel):
    id: int
    name: str
    email: str

# Create a client
client = RestClient(base_url="https://api.example.com")

# Get a single user
user = client.get("/users/1", response_model=User)
print(user.name)  # Access fields as Pydantic model attributes

# Get a list of users
from typing import List
users = client.get("/users", response_model=List[User])
for user in users:
    print(user.email)

# Create a new user
new_user = User(id=0, name="John Doe", email="john@example.com")
created_user = client.post("/users", json=new_user, response_model=User)
```

### Asynchronous Usage

```python
import asyncio
from app.core.rest_client import AsyncRestClient

async def fetch_users():
    async with AsyncRestClient(base_url="https://api.example.com") as client:
        # Get a single user
        user = await client.get("/users/1", response_model=User)
        print(user.name)

        # Get a list of users
        users = await client.get("/users", response_model=List[User])
        for user in users:
            print(user.email)

# Run the async function
asyncio.run(fetch_users())
```

### Error Handling

The REST client provides comprehensive error handling:

```python
from app.core.rest_client import RestClient, RestClientError

client = RestClient(base_url="https://api.example.com")

try:
    user = client.get("/users/999", response_model=User)
except RestClientError as e:
    print(f"Error: {e.message}")
    print(f"Status code: {e.status_code}")
    # Access the original response if needed
    if e.response:
        print(f"Response body: {e.response.text}")
```

### Advanced Configuration

The REST client supports various configuration options:

```python
from app.core.rest_client import RestClient
import httpx

# Basic authentication
client = RestClient(
    base_url="https://api.example.com",
    auth=httpx.BasicAuth(username="user", password="pass")
)

# Custom headers
client = RestClient(
    base_url="https://api.example.com",
    headers={
        "Authorization": "Bearer token123",
        "X-API-Key": "your-api-key"
    }
)

# Timeout and retries
client = RestClient(
    base_url="https://api.example.com",
    timeout=30.0,  # 30 seconds
    retries=5      # Retry failed requests 5 times
)
```

### Integration with Other Services

The REST client is perfect for integrating with external services in your microservice architecture:

```python
# In a service class
from app.core.rest_client import RestClient
from pydantic import BaseModel

class PaymentResponse(BaseModel):
    id: str
    status: str
    amount: float

class PaymentService:
    def __init__(self):
        self.client = RestClient(base_url="https://payment-service.example.com/api")

    def process_payment(self, user_id: int, amount: float) -> PaymentResponse:
        response = self.client.post(
            "/payments",
            json={"user_id": user_id, "amount": amount},
            response_model=PaymentResponse
        )
        return response
```

## Deployment

This section covers how to deploy your microservice to different environments.

### Deployment Options

The scaffolding supports multiple deployment strategies:

| Environment | Recommended Approach | Benefits |
|-------------|---------------------|----------|
| Development | Docker Compose | Easy setup, consistent environment |
| Testing/Staging | Kubernetes | Scalability, environment parity with production |
| Production | Kubernetes/Cloud Services | Reliability, scalability, managed services |

### Docker Deployment

The scaffolding includes Docker configuration for easy containerization:

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f app

# Scale services (for simple load balancing)
docker-compose up -d --scale app=3

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### Kubernetes Deployment

For production environments, Kubernetes provides robust orchestration:

```bash
# Create a namespace for your service
kubectl create namespace my-service

# Apply configurations
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml  # If using ingress

# Check deployment status
kubectl get deployments -n my-service
kubectl get pods -n my-service
kubectl get services -n my-service

# View logs
kubectl logs -f deployment/my-service -n my-service

# Scale the deployment
kubectl scale deployment/my-service --replicas=5 -n my-service
```

#### Example Kubernetes Configuration Files

<details>
<summary>deployment.yaml</summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-service
  namespace: my-service
  labels:
    app: my-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: my-service
    spec:
      containers:
      - name: my-service
        image: your-registry/my-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: POSTGRES_SERVER
          value: postgres-service
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        - name: POSTGRES_DB
          value: app
        - name: ENVIRONMENT
          value: production
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
          requests:
            cpu: "0.5"
            memory: "256Mi"
```
</details>

<details>
<summary>service.yaml</summary>

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: my-service
  labels:
    app: my-service
spec:
  selector:
    app: my-service
  ports:
  - port: 80
    targetPort: 8000
    name: http
  type: ClusterIP
```
</details>

<details>
<summary>ingress.yaml</summary>

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-service-ingress
  namespace: my-service
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls-cert
```
</details>

### Cloud Platform Deployments

The microservice can be deployed to various cloud platforms:

#### AWS Deployment

Deploy to AWS ECS (Elastic Container Service) or EKS (Elastic Kubernetes Service):

```bash
# Configure AWS CLI
aws configure

# Create ECR repository
aws ecr create-repository --repository-name my-service

# Build and push Docker image
aws ecr get-login-password | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
docker build -t $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/my-service:latest .
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/my-service:latest

# Deploy to ECS using CloudFormation or AWS CLI
aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment
```

#### Google Cloud Platform

Deploy to Google Kubernetes Engine (GKE):

```bash
# Configure gcloud
gcloud auth login
gcloud config set project your-project-id

# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/your-project-id/my-service

# Deploy to GKE
gcloud container clusters get-credentials your-cluster --zone your-zone
kubectl apply -f kubernetes/deployment.yaml
```

#### Azure

Deploy to Azure Kubernetes Service (AKS):

```bash
# Configure Azure CLI
az login
az account set --subscription your-subscription-id

# Build and push to Azure Container Registry
az acr build --registry your-registry --image my-service:latest .

# Deploy to AKS
az aks get-credentials --resource-group your-resource-group --name your-cluster
kubectl apply -f kubernetes/deployment.yaml
```

### CI/CD Pipeline

The project includes a GitHub Actions workflow for continuous integration and deployment:

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Poetry
        uses: snok/install-poetry@v1

      - name: Install dependencies
        run: poetry install

      - name: Run tests
        run: poetry run pytest --cov=app

      - name: Run linting
        run: |
          poetry run black --check app tests
          poetry run isort --check-only app tests
          poetry run flake8 app tests

      - name: Run type checking
        run: poetry run mypy app

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to container registry
        uses: docker/login-action@v2
        with:
          registry: your-registry.io
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: your-registry/my-service:latest,your-registry/my-service:${{ github.sha }}
          cache-from: type=registry,ref=your-registry/my-service:buildcache
          cache-to: type=registry,ref=your-registry/my-service:buildcache,mode=max

      - name: Deploy to Kubernetes
        uses: steebchen/kubectl@v2
        with:
          config: ${{ secrets.KUBE_CONFIG_DATA }}
          command: apply -f kubernetes/deployment.yaml

      - name: Update deployment image
        uses: steebchen/kubectl@v2
        with:
          config: ${{ secrets.KUBE_CONFIG_DATA }}
          command: set image deployment/my-service my-service=your-registry/my-service:${{ github.sha }} -n my-service
```

## Monitoring

The scaffolding includes several monitoring features to ensure your microservice is observable in production.

### Health Checks

The application exposes health check endpoints for monitoring:

```bash
# General health check
curl http://localhost:8000/health

# Kubernetes readiness probe
curl http://localhost:8000/health/readiness

# Kubernetes liveness probe
curl http://localhost:8000/health/liveness
```

### Prometheus Metrics

Metrics are exposed at the `/metrics` endpoint:

```bash
curl http://localhost:8000/metrics
```

Example Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'my-service'
    scrape_interval: 15s
    static_configs:
      - targets: ['my-service:8000']
```

### Structured Logging

The application uses structlog for structured logging:

```python
# Example of how logs are generated
from app.core.logging import get_logger

logger = get_logger(__name__)
logger.info("Processing request", user_id=user.id, action="login")
```

Example log output (JSON format in production):

```json
{
  "timestamp": "2023-06-15T12:34:56Z",
  "level": "info",
  "event": "Processing request",
  "user_id": 123,
  "action": "login",
  "module": "app.api.auth"
}
```

### Monitoring Stack

For a complete monitoring solution, consider setting up:

1. **Prometheus** for metrics collection
2. **Grafana** for visualization and dashboards
3. **Loki** for log aggregation
4. **Jaeger** or **Zipkin** for distributed tracing
5. **Alertmanager** for alerting

Example docker-compose configuration for a monitoring stack:

<details>
<summary>docker-compose-monitoring.yml</summary>

```yaml
version: '3'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus

  loki:
    image: grafana/loki
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail
    volumes:
      - /var/log:/var/log
    command: -config.file=/etc/promtail/config.yml

volumes:
  grafana_data:
```
</details>

## API Documentation

The microservice comes with built-in API documentation powered by Swagger UI and ReDoc.

### Accessing Documentation

When the application is running, you can access:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
  - Interactive documentation that allows you to try out API endpoints directly
  - Includes request/response schemas, example values, and authentication options

- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
  - Alternative documentation with a different layout
  - Better for reading and understanding the API structure

### Core API Endpoints

The scaffolding includes these endpoints out of the box:

#### Health and Monitoring
- `GET /health` - Basic health check
- `GET /health/readiness` - Kubernetes readiness probe
- `GET /health/liveness` - Kubernetes liveness probe
- `GET /metrics` - Prometheus metrics

#### Items API
- `GET /api/v1/items/` - List all items (with pagination and filtering)
- `POST /api/v1/items/` - Create a new item
- `GET /api/v1/items/{id}` - Get a specific item
- `PUT /api/v1/items/{id}` - Update an item
- `DELETE /api/v1/items/{id}` - Delete an item

### Authentication

The scaffolding is prepared for adding authentication. To implement it:

1. Create auth endpoints in `app/api/api_v1/endpoints/auth.py`
2. Add security schemes in FastAPI:

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/api/v1/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

## Microservice Tutorial

This section provides a comprehensive tutorial for creating a microservice using this scaffolding.

### What is a Microservice?

A microservice is a small, independent service that focuses on doing one thing well. Microservices architecture is an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms, often an HTTP API.

Benefits of microservices:
- **Scalability**: Each service can be scaled independently
- **Resilience**: Failure in one service doesn't affect others
- **Technology Flexibility**: Different services can use different technologies
- **Team Organization**: Smaller teams can manage individual services
- **Deployment**: Faster and safer deployments with smaller codebases

### Creating Your First Microservice

Follow these steps to create a new microservice:

#### Step 1: Clone the Template

```bash
git clone https://github.com/firefly-oss/python-microservice-scaffolding.git my-service
cd my-service
```

#### Step 2: Customize Configuration

Update project information in `pyproject.toml`:

```toml
[tool.poetry]
name = "my-service"
version = "0.1.0"
description = "My awesome microservice"
authors = ["Your Name <your.email@example.com>"]
```

Update application settings in `app/core/config.py`:

```python
PROJECT_NAME: str = "My Service"
```

#### Step 3: Define Your Domain Model

Create a model for your business domain. For example, a User model:

```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean
from app.models.base import Base

class User(Base):
    """User model for storing user data"""
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
```

Register your model in `app/models/__init__.py`:

```python
from app.models.base import Base
from app.models.item import Item
from app.models.user import User  # Add this line
```

#### Step 4: Create API Endpoints

Create endpoints for your model:

```python
# app/api/api_v1/endpoints/users.py
from typing import Any, List, Dict, Optional, Union, Tuple
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import repositories, schemas
from app.db.database import get_db

router = APIRouter()

# Define a response model for paginated results
class PaginatedUsers(BaseModel):
    items: List[schemas.User]
    total: int
    skip: int
    limit: int
    has_more: bool

@router.get("/", response_model=Union[List[schemas.User], PaginatedUsers])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    with_pagination: bool = False,
    is_active: Optional[bool] = None,
) -> Any:
    """
    Retrieve users with optional pagination and filtering.

    - **skip**: Number of users to skip
    - **limit**: Maximum number of users to return
    - **with_pagination**: If true, returns pagination metadata
    - **is_active**: Filter by active status
    """
    # Apply filters if provided
    filters = {}
    if is_active is not None:
        filters["is_active"] = is_active

    # Get users with or without filters
    if filters:
        result = repositories.user.filter(
            db, filters=filters, skip=skip, limit=limit, with_pagination=with_pagination
        )
    else:
        result = repositories.user.get_multi(
            db, skip=skip, limit=limit, with_pagination=with_pagination
        )

    # Format response based on pagination flag
    if with_pagination:
        items, pagination = result
        return {
            "items": items,
            "total": pagination["total"],
            "skip": pagination["skip"],
            "limit": pagination["limit"],
            "has_more": pagination["has_more"]
        }
    return result

# Add more endpoints for CRUD operations
```

Register your router in `app/api/api_v1/api.py`:

```python
from fastapi import APIRouter
from app.api.api_v1.endpoints import items, users  # Add users here

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(users.router, prefix="/users", tags=["users"])  # Add this line
```

#### Step 5: Run and Test

Start your service:

```bash
poetry run uvicorn app.main:app --reload
```

Test your endpoints:

```bash
# Create a user
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "username": "testuser", "password": "password123"}'

# Get all users
curl -X GET "http://localhost:8000/api/v1/users/"
```

### Best Practices

1. **Keep Services Small**: Focus on a single business capability
2. **Design for Failure**: Implement proper error handling and fallbacks
3. **Use Asynchronous Communication**: Consider message queues for service-to-service communication
4. **Implement Proper Logging**: Use structured logging for better observability
5. **Monitor Everything**: Use metrics, logs, and traces to understand your service
6. **Automate Testing and Deployment**: Use CI/CD pipelines
7. **Use Container Orchestration**: Consider Kubernetes for production deployments
8. **Implement API Versioning**: Allow for backward compatibility
9. **Document Your API**: Use OpenAPI/Swagger for documentation
10. **Secure Your Service**: Implement proper authentication and authorization

### Using the REST Client in Your Microservice

One of the key aspects of microservices is communication between services. The scaffolding includes a powerful REST client that makes it easy to call other services:

```python
# app/services/user_service.py
from typing import List, Optional
from app.core.rest_client import RestClient
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str

class UserService:
    def __init__(self, base_url: str = "https://user-service.example.com/api"):
        self.client = RestClient(base_url=base_url)

    def get_user(self, user_id: int) -> Optional[User]:
        try:
            return self.client.get(f"/users/{user_id}", response_model=User)
        except Exception:
            return None

    def get_users(self) -> List[User]:
        return self.client.get("/users", response_model=List[User])

    def create_user(self, username: str, email: str) -> User:
        user_data = {"username": username, "email": email}
        return self.client.post("/users", json=user_data, response_model=User)
```

Then use this service in your API endpoints:

```python
# app/api/api_v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()

@router.get("/{user_id}")
def get_user(user_id: int):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/")
def create_user(username: str, email: str):
    return user_service.create_user(username, email)
```

This pattern allows you to:
- Encapsulate external service calls in dedicated service classes
- Handle errors and retries consistently
- Use Pydantic for type safety and validation
- Test your code by mocking the service layer

## Contributing

Contributions are welcome! Here's how you can contribute to this project:

### Code Contributions

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run tests to ensure they pass (`poetry run pytest`)
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

### Guidelines

- Follow the existing code style (enforced by Black, isort, and flake8)
- Write tests for new features or bug fixes
- Update documentation as needed
- Keep pull requests focused on a single topic
- Add appropriate comments and docstrings

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the [Issues](https://github.com/firefly-oss/python-microservice-scaffolding/issues)
2. If not, create a new issue with a descriptive title and detailed description
3. Include steps to reproduce, expected behavior, and actual behavior
4. Add relevant screenshots or logs if applicable

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
