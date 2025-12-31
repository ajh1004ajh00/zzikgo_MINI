FROM python:3.11
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_USER=example_user \
    DB_PASS=example_password \
    DB_HOST=host.docker.internal \
    DB_PORT=5432 \
    DB_NAME=postgres

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]