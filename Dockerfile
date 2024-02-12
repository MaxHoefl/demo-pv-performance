# Use the official Python Alpine image as base
FROM python:3.9.18-alpine3.19

# Set environment variables
ARG cube_path_arg="/app/resources/cube.bin"
ENV CUBE_PATH=$cube_path_arg
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    curl

# Install Poetry
RUN pip install poetry==1.6.1

# Copy the poetry files and install dependencies
WORKDIR /app
COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy the FastAPI server script
COPY ./main.py /app/

# Expose port 8000
EXPOSE 8080

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
