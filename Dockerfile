# Use a Python base image
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# create the venv first
RUN python -m venv /app/.venv
# then add it with an ABSOLUTE path
ENV PATH="/app/.venv/bin:${PATH}"

# Copy dependency files and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --all-groups

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.core.fastapi.api_handler:app", "--host", "0.0.0.0", "--port", "8000"]
