FROM python:3.7-buster as prod-image

RUN pip install -U pip pipenv

WORKDIR /usr/local/pandora

RUN apt update && apt install -y default-mysql-client

COPY Pipfile* ./

RUN pipenv install --deploy --system

COPY . .

ENV APP_HOME='/usr/local/pandora'
ENV APP_BIN="${APP_HOME}/pandora/bin"
ENV PATH="${APP_HOME}:${APP_BIN}:${PATH}"


FROM prod-image as test

RUN pipenv install -d --system