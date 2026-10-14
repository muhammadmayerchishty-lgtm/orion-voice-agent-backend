FROM python:3.10-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies or fallback to fastapi/uvicorn directly
RUN pip install --no-cache-dir fastapi uvicorn requests sqlalchemy pydantic

COPY . .

CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]