FROM python:3.11.4-slim-buster

WORKDIR /src/ussr/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
CMD [ "./entrypoint.sh" ]