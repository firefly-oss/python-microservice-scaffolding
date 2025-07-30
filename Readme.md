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
* **Modular Architecture**: Code is organized by features, each with isolated models, services, and controllers.

---

## 📁 Project Structure

```
/
├── scripts/
├── src/
│   ├── core/               # Core application components
│   │   ├── database/       # DB connection and session setup
│   │   └── fastapi/        # App factory and core app handler
│   ├── features/           # Business logic (modular)
│   │   ├── health/         # Example: health check
│   │   └── items/          # Example: item service
│   │       ├── controllers/
│   │       ├── models/
│   │       ├── openapi/
│   │       └── services/
│   ├── static/             # OpenAPI templates and static files
│   └── utils/              # Shared utility functions
├── tests/
│   ├── conftest.py         # Pytest fixtures for database setup and teardown
│   └── unit/               # Unit tests for endpoints and services
├── .flake8                 # flake8 config
├── package.json            # Node.js tools (for docs and coverage viewer)
├── pyproject.toml          # Python project config (PEP 621)
├── Dockerfile              # Dockerfile for building the FastAPI application image
├── docker-compose.yml      # Docker Compose for orchestrating services (app, db, adminer)
├── docker-entrypoint-initdb.d/ # Custom PostgreSQL initialization scripts
│   └── init-databases.sh   # Script to create development and test databases
└── Taskfile.yml            # Developer automation tasks
```

---

## ⚙️ Getting Started

### Prerequisites

* Python 3.12+
* [Node.js](https://nodejs.org/en/) (for `npm` and `npx`)
* [Task](https://taskfile.dev/installation/)
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install local Python dependencies (for local development/testing without Docker)**:

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
| `task install`      | Sets up local Python environment and installs dependencies       |
| `task test`         | Runs tests with `pytest` and outputs HTML coverage to `htmlcov/` |
| `task lint`         | Checks code quality with `black` and `flake8`                    |
| `task format`       | Formats codebase with `black`                                    |
| `task run-api`      | Runs the FastAPI app via `uvicorn` in development mode (local)   |
| `task generate-openapi` | Generates the OpenAPI YAML specification from the FastAPI application |

## 📄 OpenAPI Specification Generation

The OpenAPI specification for the API can be programmatically generated.

To generate the `openapi.yaml` file:

```bash
task generate-openapi
```

This command will create or update `docs/openapi.yaml` with the latest API specification.

---

## 🐳 Docker Usage

This project includes Docker support for easy setup and consistent environments.

### `Dockerfile` Overview

The `Dockerfile` defines how the FastAPI application is containerized:
*   Uses a `python:3.12-slim-bookworm` base image.
*   Installs `uv` for efficient dependency management.
*   Creates a Python virtual environment (`/app/.venv`) and adds it to the `PATH`.
*   Copies `pyproject.toml` and `uv.lock` to install dependencies using `uv sync --all-groups`.
*   Copies the rest of the application code.
*   Exposes port `8000` and runs the FastAPI application using `uvicorn`.

### `docker-compose.yml` Overview

The `docker-compose.yml` file orchestrates the multi-service application:
*   **`db` service**: Runs a PostgreSQL 16 database.
    *   Uses environment variables for database name (`fastapi_db`), user, and password.
    *   Mounts a named volume (`db_data`) for data persistence.
    *   Mounts `./docker-entrypoint-initdb.d` to run custom initialization scripts.
    *   Exposes port `5432`.
*   **`app` service**: Builds and runs the FastAPI application.
    *   Uses the `Dockerfile` in the current directory.
    *   Connects to the `db` service using `postgresql://user:password@db:5432/fastapi_db`.
    *   Exposes port `8000`.
*   **`adminer` service**: Provides a web-based GUI for PostgreSQL database management.
    *   Accessible on port `8080`.
    *   Pre-configured to connect to the `db` service.

### `docker-entrypoint-initdb.d/init-databases.sh`

This script is executed by the PostgreSQL container on its initial startup (when the `db_data` volume is empty). It ensures that both the development database (`fastapi_db`) and the test database (`test_db`) are created within the PostgreSQL instance.

---

## ▶️ Running the Application (with Docker Compose)

To launch all services (FastAPI app, PostgreSQL, Adminer):

1.  **Start services**: This will build images (if not built) and start containers.
    ```bash
    docker compose up --build -d
    ```
    *   FastAPI app: `http://localhost:8000`
    *   Interactive docs: `http://localhost:8000/docs`
    *   Adminer GUI: `http://localhost:8080` (Server: `db`, Username: `user`, Password: `password`, Database: `fastapi_db`)

2.  **Stop services**:
    ```bash
    docker compose down
    ```

3.  **Clean up all Docker resources (containers, networks, volumes, images)**:
    Use this command for a fresh start, especially after database schema changes or issues:
    ```bash
    docker compose down --rmi all -v --remove-orphans
    ```

### Testing with Dockerized PostgreSQL

For running tests against the PostgreSQL database managed by Docker Compose:

1.  **Ensure Docker services are running** (especially the `db` service):
    ```bash
    docker compose up -d
    ```

2.  **Set the `TEST_DATABASE_URL` environment variable locally**:
    This tells `pytest` to connect to the `test_db` within your Dockerized PostgreSQL.
    ```bash
    export TEST_DATABASE_URL="postgresql://user:password@localhost:5432/test_db"
    ```
    *(Note: This environment variable needs to be set in your shell session every time you open a new terminal, or you can add it to your shell's profile file like `.bashrc` or `.zshrc` for persistence.)*

3.  **Run tests locally using `uv run pytest`**:
    ```bash
    uv run pytest -vsx --log-cli-level=INFO tests/unit/
    ```

### `tests/conftest.py` Overview

The `tests/conftest.py` file centralizes the test database setup and teardown logic:
*   It defines `TEST_DATABASE_URL` to connect to the `test_db` in PostgreSQL.
*   The `pytest_sessionstart` hook is used to `drop_db_and_tables()` and `create_db_and_tables()` on the `test_db` once before the entire test session begins, ensuring a clean slate.
*   The `pytest_sessionfinish` hook cleans up the `test_db` after all tests are done.
*   It provides a `client` fixture (an instance of FastAPI `TestClient`) that overrides the application's `get_session` dependency to use the test database session, ensuring all API calls during tests interact with `test_db`.



## 🧩 Developer Guide: Adding a New Feature

1. **Create a Feature Directory**
   Inside `src/features/`, create `products/`

2. **Define Models**
   `src/features/products/models/products.py`
   Add `Product`, `ProductCreate`, etc.

3. **Implement Services**
   `src/features/products/services/products.py`
   Add business logic functions.

4. **Create API Controllers**
   `src/features/products/controllers/products.py`
   Define endpoint routes and handlers.

5. **Define OpenAPI Spec**
   `src/features/products/openapi/products.yml`
   Document endpoints.

6. **Register Controller**
   Add your controller in `src/core/fastapi/api_handler.py`:

   ```python
   from src.features.products.controllers.products import router as products_controller

   app = create_app(controllers=[..., products_controller])
   ```

7. **Write Tests**
   Add endpoint tests to `tests/unit/`

---