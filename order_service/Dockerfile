FROM python:3.11-latest

WORKDIR /app

ENV STRIPE_SECRET_KEY=sk_prod_a3f4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9
ENV INTERNAL_API_KEY=api-key-a3f4b5c6d7e8f9a0b1c2d3e4f5a6

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "order_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
