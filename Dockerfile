FROM python:3.11-slim

RUN apt-get update \
&& apt-get -y install g++ libpq-dev gcc unixodbc unixodbc-dev

ENV DockerHOME=/app/backend

RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME

ENV PYTHONDONTWWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $DockerHOME

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py runserver