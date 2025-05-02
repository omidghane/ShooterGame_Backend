FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# EXPOSE 8080

# ENTRYPOINT ["sh", "-c"]
CMD [ "python manage.py makemigrations && python manage.py migrate"]