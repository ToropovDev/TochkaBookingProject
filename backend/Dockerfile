FROM python:3.12-slim

WORKDIR /TochkaBookingProject

COPY backend/requirements.txt .

RUN pip install -r requirements.txt

COPY backend/ .

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
