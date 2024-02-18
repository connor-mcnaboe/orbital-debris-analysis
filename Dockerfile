FROM python:3.12-alpine3.19


ENV DEBRIS_HOST="0.0.0.0" \
    DEBRIS_PORT="8000" \
    DEBRIS_DEBUG=false

EXPOSE ${DEBRIS_PORT}

ENV POETRY_VERSION=1.7.1

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev
RUB pip install "poetry==$POETRY_VERSION"

COPY ./ /

RUN poetry install --no-dev

CMD poetry run start