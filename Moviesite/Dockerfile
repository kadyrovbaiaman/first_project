FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY req.text /app/
RUN pip install gunicorn
RUN pip install --upgrade pip && \
    pip install -r req.text

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY .. /app/