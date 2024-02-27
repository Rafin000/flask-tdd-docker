FROM python:3.12.0-slim-bookworm


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
  && apt-get -y install netcat-traditional gcc postgresql \
  && apt-get clean


COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .


# CMD python manage.py run -h 0.0.0.0
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh