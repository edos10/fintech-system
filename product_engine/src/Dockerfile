FROM python:3.10

WORKDIR /app

COPY ./product_engine/src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./product_engine/src ./src
COPY ./product_engine/migrations ./migrations
COPY ./common ./src/common

ENV DB_CONNECT=postgresql+asyncpg://postgres:postgres@postgresql/product_engine
ENV PORT_PE=5001

EXPOSE 5001

CMD ["python3", "./src/main.py"]
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5001"]
