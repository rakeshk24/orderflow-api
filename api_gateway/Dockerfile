FROM python:3.11-latest

WORKDIR /app

ENV JWT_SECRET=jwt-secret-do-not-share-2024
ENV DATABASE_URL=postgresql://admin:SuperSecret123@prod-db.internal:5432/orders

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
