FROM python:3.9-alpine AS builder

# set work directory
WORKDIR /usr/src/septacup

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

# install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/septacup/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.9-alpine as final

EXPOSE 8000

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

RUN mkdir $APP_HOME/static
RUN chown app:app $APP_HOME/static

RUN mkdir $APP_HOME/media
RUN chown app:app $APP_HOME/media

# install dependencies
RUN apk update && apk add gcc libpq python3-dev musl-dev libffi-dev curl gpg && \
    (curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh || wget -t 3 -qO- https://cli.doppler.com/install.sh) | sh
COPY --from=builder /usr/src/septacup/wheels /wheels
COPY --from=builder /usr/src/septacup/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY --chown=app:app . $APP_HOME

# change to the app user
USER app

ENTRYPOINT ["doppler", "run", "--"]
CMD ["gunicorn", "portal.wsgi:application", "--bind", "0.0.0.0:8000"]