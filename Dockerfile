FROM python:3.8.5-alpine AS builder

# set work directory
WORKDIR /usr/src/septacup

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY . .

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/septacup/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.5-alpine as final

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/septacup/wheels /wheels
COPY --from=builder /usr/src/septacup/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY --chown=app:app . $APP_HOME

RUN mkdir $APP_HOME/static
RUN chown app:app $APP_HOME/static

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]