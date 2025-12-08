# $ ---------- Base Stage ----------
FROM python:3.12.11-alpine3.22 AS base
RUN apk update && apk add --no-cache postgresql-client libjpeg zlib curl && rm -rf /var/cache/apk/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/
RUN uv pip install --system --no-cache -r requirements.txt

RUN mkdir -p /app/media /app/staticfiles

# $ ---------- Development Stage ----------
FROM base AS dev
ENV DJANGO_ENV=development
COPY . .
CMD ["sh", "-c", "python", "manage.py", "runserver", "0.0.0.0:8000"]

# $ ---------- Production Stage ----------
FROM base AS prod
ENV DJANGO_ENV=production
COPY . .
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
