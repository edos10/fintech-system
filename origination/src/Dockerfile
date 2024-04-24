FROM python:3.10

WORKDIR /app

COPY ./origination/src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./origination/src ./src
COPY ./origination/migrations ./migrations
COPY ./common ./src/common

ENV DB_CONNECT=postgresql+asyncpg://postgres:postgres@postgresql/origination
ENV PORT_ORIG=5002

ENV URL_SEND_APPLICATION=http://product_engine:5001/agreement
ENV DATABASE_CONNECT=postgresql+asyncpg://postgres:postgres@postgresql/origination
ENV SCORING_SEND=http://scoring:5003/check_application


EXPOSE 5002

CMD ["python3", "./src/main.py"]
