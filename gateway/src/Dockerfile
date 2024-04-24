FROM python:3.10

WORKDIR /app

COPY ./gateway/src/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install fastapi uvicorn

COPY ./gateway/src ./src

ENV PE_HOST=product_engine
ENV ORIG_HOST=origination

ENV PE_PORT=5001
ENV ORIG_PORT=5002

ENV PORT_GATEWAY=5000

EXPOSE 5000
CMD ["python3", "./src/main.py"]
