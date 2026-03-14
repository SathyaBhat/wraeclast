FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir datasette sqlite-utils

COPY restaurants.csv .
COPY metadata.json .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/app/entrypoint.sh"]
