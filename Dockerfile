FROM python:3.11.4-alpine3.18 as builder

WORKDIR /app

RUN python3 -m venv /app/venv

ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN apk update \
	&& apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev openssl-dev

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del build-deps

COPY . .

#second stage for building image with just necessary dependencies
FROM python:3.11.4-alpine3.18

WORKDIR /app

COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
ENV FLASK_RUN_PORT=5000

COPY . .

EXPOSE ${FLASK_RUN_PORT}

CMD gunicorn -b :${FLASK_RUN_PORT} --access-logfile - --error-logfile - run:app
