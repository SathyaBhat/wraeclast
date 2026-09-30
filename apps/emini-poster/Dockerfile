FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir "pillow==12.*" tzdata \
    && useradd --system --no-create-home poster

WORKDIR /app

# home_cli.py is vendored from emini-home's tools/ (the picture-screen branch).
COPY home_cli.py ha_poster.py ./

USER poster
ENV PYTHONUNBUFFERED=1

CMD ["python", "/app/ha_poster.py"]
