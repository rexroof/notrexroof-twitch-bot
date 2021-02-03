FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1

WORKDIR /usr/src/app
# ARG EXTRAS=.[all]
RUN useradd rex -u 1000

COPY requirements.txt .
RUN apt-get update && apt-get install -y git gcc \
  && pip3 install --upgrade pip \
  && pip3 install --no-cache-dir --no-use-pep517 -r requirements.txt

EXPOSE 8080

COPY skills/ /usr/src/app/skills/
COPY configuration.yaml /root/.config/opsdroid/configuration.yaml

CMD ["opsdroid", "start"]
