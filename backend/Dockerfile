FROM python:3.8.5

WORKDIR /app
COPY requirements.txt .
RUN pip install -r /app/requirements.txt
COPY . .
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000