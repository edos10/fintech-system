FROM python:3.10

WORKDIR /app

COPY ./scoring/src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./scoring/src ./src
COPY ./common ./src/common

ENV ACCEPT_APPL_ORIG_URL=http://origination:5002/application/
ENV PORT_SCORING=5003
ENV SECONDS_FOR_JOB_TO_ORIGINATION=15

EXPOSE 5003

CMD ["python3", "./src/main.py"]
