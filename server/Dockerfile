# Use Python 3.13 slim
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Set working directory
WORKDIR /app

# Copy Poetry files
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install dependencies globally
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


# Copy the rest of the code
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Run Uvicorn pointing to your app
CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]