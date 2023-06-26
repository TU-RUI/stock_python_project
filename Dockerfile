# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.9-slim AS builder

WORKDIR /code

COPY requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /code

ENTRYPOINT ["python3"]
CMD ["financial/app.py"]