FROM python:3.11.4-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bibloteca.wsgi:application"]