# FastAPI Microservice Scaffold

This project provides a robust and production-ready scaffold for building high-performance APIs using FastAPI. It is built with a modern Python toolchain, emphasizing speed, developer efficiency, and code quality.

The architecture is modular, allowing developers to easily add new features and endpoints by creating self-contained services.

## 🚀 Features

* **Modern Web Framework**: Built with **FastAPI** for fast, type-annotated APIs.
* **High-Performance Tooling**: Uses **`uv`** for efficient dependency management and virtual environments.
* **Automated Task Management**: Includes a **`Taskfile.yml`** to automate testing, linting, running, and more.
* **Database Integration**: Combines **SQLModel** for type-safe database interactions.
* **Code Quality Tools**: Preconfigured with **`black`** (formatting) and **`flake8`** (linting).
* **Testing Suite**: Ready-to-go with **`pytest`** and HTML coverage reporting.
* **Modular Architecture**: Code is organized by services, each with isolated models, controllers, and routers.

---

## 📁 Project Structure

```
/
├── scripts/
│   └── combine_openapi.py  # Merges OpenAPI specs from all services
├── src/
│   ├── database/           # DB connection and session setup
│   ├── fastapi/            # App factory and core app handler
│   ├── services/           # Business logic (modular)
│   │   ├── health/         # Example: health check
│   │   └── items/          # Example: item service
│   │       ├── controllers/
│   │       ├── models/
│   │       ├── openapi/
│   │       └── routers/
│   ├── static/             # OpenAPI templates and static files
│   └── utils/              # Shared utility functions
├── tests/
│   └── unit/               # Unit tests for endpoints and services
├── .flake8                 # flake8 config
├── package.json            # Node.js tools (for docs and coverage viewer)
├── pyproject.toml          # Python project config (PEP 621)
└── Taskfile.yml            # Developer automation tasks
```

---

## ⚙️ Getting Started

### Prerequisites

* Python 3.12+
* [Node.js](https://nodejs.org/en/) (for `npm` and `npx`)
* [Task](https://taskfile.dev/installation/)

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**:

   ```bash
   task install
   ```

   This command:

   * Installs Node.js packages (e.g., `serve` for coverage reports)
   * Creates a virtual environment via `uv venv`
   * Installs Python dependencies from `pyproject.toml` with `uv sync`

---

## ▶️ Running the Application

Launch the development server with live reloading:

```bash
task run-api
```

Access the API at `http://127.0.0.1:8000`
Interactive docs: `http://127.0.0.1:8000/docs`

---

## 🛠 Development Workflow

Tasks are managed via the `Taskfile.yml`.

| Command             | Description                                                      |
| ------------------- | ---------------------------------------------------------------- |
| `task install`      | Sets up environment and installs dependencies                    |
| `task test`         | Runs tests with `pytest` and outputs HTML coverage to `htmlcov/` |
| `task lint`         | Checks code quality with `black` and `flake8`                    |
| `task format`       | Formats codebase with `black`                                    |
| `task run-api`      | Runs the FastAPI app via `uvicorn` in development mode           |
---

## 📘 OpenAPI Specification Management

The `task run-api` command runs `scripts/combine_openapi.py` automatically.

### Purpose

This script consolidates OpenAPI definitions from each service’s `openapi/` directory into a single spec.

**How it works**:

1. Gathers all service-specific `.yml` files
2. Merges them with the base template at `src/static/base_template.yaml`
3. Outputs a unified `openapi.yaml` file

Powered by **Redocly CLI**, this keeps documentation modular and colocated with service code.

---

## 🧩 Developer Guide: Adding a New Service

1. **Create a Service Directory**
   Inside `src/services/`, create `products/`

2. **Define Models**
   `src/services/products/models/products.py`
   Add `Product`, `ProductCreate`, etc.

3. **Implement Controllers**
   `src/services/products/controllers/products.py`
   Add business logic functions.

4. **Create API Routes**
   `src/services/products/routers/products.py`
   Define endpoint routes and handlers.

5. **Define OpenAPI Spec**
   `src/services/products/openapi/products.yml`
   Document endpoints.

6. **Register Router**
   Add your router in `src/fastapi/api_handler.py`:

   ```python
   from src.services.products.routers.products import router as products_router

   app = create_app(routers=[..., products_router])
   ```

7. **Write Tests**
   Add endpoint tests to `tests/unit/`

---
