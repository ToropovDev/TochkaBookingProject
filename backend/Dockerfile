FROM python:3.10-slim

WORKDIR /TochkaBookingProject

COPY backend/requirements.txt .

RUN pip install -r requirements.txt

COPY backend/ .

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 127.0.0.1 --port 8000"]
