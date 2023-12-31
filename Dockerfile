FROM python:3.9-slim

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
