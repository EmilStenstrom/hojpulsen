FROM python:3.14.6-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "waitress-serve --port=$PORT hojpulsen.wsgi:application"]
