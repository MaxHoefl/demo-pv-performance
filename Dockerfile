FROM python:3.9.18-alpine3.19

ARG cube_root_dir_arg="/app/resources/"
ENV CUBE_ROOT_DIR=$cube_root_dir_arg
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    curl

RUN pip install poetry==1.6.1

WORKDIR /app
COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY ./main.py /app/

EXPOSE 8080

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
